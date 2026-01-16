from fastapi import FastAPI, HTTPException, Depends, status, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import os
import secrets

from app.database.db import db
from config import config

app = FastAPI(title="SmplWAF")
security = HTTPBasic()

#авторизация
def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, config.ADMIN_USERNAME)
    correct_password = secrets.compare_digest(credentials.password, config.ADMIN_PASSWORD)

    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверные учётные данные",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.on_event("startup")
async def startup():
    await db.connect()

@app.on_event("shutdown")
async def shutdown():
    await db.close()

@app.get("/")
async def index(username: str = Depends(get_current_username)):
    return FileResponse(os.path.join(static_dir, "index.html"))

@app.get("/api/sessions")
async def get_sessions(username: str = Depends(get_current_username)):
    try:
        #потом сделать пагинацию, а не рендерить на одной странице разом
        user_sessions_rows = await db.fetch_all("SELECT * FROM user_sessions ORDER BY last_activity_time DESC LIMIT 50")
        user_sessions = [dict(row) for row in user_sessions_rows]

        for us in user_sessions:
            streams_rows = await db.fetch_all(
                "SELECT * FROM tcp_streams WHERE user_session_id = ? ORDER BY start_time ASC",
                (us['id'],)
            )
            streams = [dict(row) for row in streams_rows]

            us_tags = set()
            for stream in streams:
                msgs_rows = await db.fetch_all(
                    "SELECT id, type, method, url, status_code, tags, headers, body, timestamp FROM messages WHERE tcp_stream_id = ? ORDER BY timestamp ASC",
                    (stream['id'],)
                )
                stream['messages'] = []
                for m in msgs_rows:
                    msg_dict = dict(m)
                    if isinstance(msg_dict.get('body'), bytes):
                        try:
                            msg_dict['body'] = msg_dict['body'].decode('utf-8', errors='replace')
                        except:
                            msg_dict['body'] = "[Binary Data]"

                    #теги
                    if msg_dict.get('tags'):
                        try:
                            import json
                            tags_list = json.loads(msg_dict['tags'])
                            for t in tags_list:
                                us_tags.add(t)
                        except:
                            pass

                    stream['messages'].append(msg_dict)

            us['streams'] = streams
            us['tags'] = list(us_tags)

        return JSONResponse(content=user_sessions)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/api/stream/{stream_id}")
async def get_stream_details(stream_id: int, username: str = Depends(get_current_username)):
    stream = await db.fetch_all("SELECT * FROM tcp_streams WHERE id = ?", (stream_id,))
    if not stream:
        return JSONResponse(status_code=404, content={"error": "Поток не найден"})

    messages = await db.fetch_all("SELECT * FROM messages WHERE tcp_stream_id = ?", (stream_id,))

    result = dict(stream[0])
    result['messages'] = []
    for m in messages:
        msg_dict = dict(m)
        if isinstance(msg_dict.get('body'), bytes):
            try:
                msg_dict['body'] = msg_dict['body'].decode('utf-8', errors='replace')
            except:
                msg_dict['body'] = "[Binary Data]"
        result['messages'].append(msg_dict)

    return JSONResponse(content=result)

@app.post("/api/rules/block_ip")
async def block_ip(request: Request, username: str = Depends(get_current_username)):
    try:
        data = await request.json()
        ip = data.get("ip")
        if not ip:
            raise HTTPException(status_code=400, detail="Нужно указать IP")

        rule_content = f"if request.client_ip == '{ip}': action.drop()"


        if hasattr(app.state, 'rule_engine'):
            success = app.state.rule_engine.add_rule(f"block_{ip.replace('.', '_')}", rule_content)
            if success:
                return JSONResponse(content={"status": "ok", "message": f"IP {ip} заблокирован"})
            else:
                return JSONResponse(status_code=500, content={"error": "Не удалось добавить правило"})
        else:
            return JSONResponse(status_code=503, content={"error": "Движок правил недоступен"})

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# ниже управление правилами

RULES_ROOT = "rules"

def validate_rule_path(path: str):

    abs_root = os.path.abspath(RULES_ROOT)
    abs_path = os.path.abspath(os.path.join(RULES_ROOT, path))
    if not abs_path.startswith(abs_root):
        raise HTTPException(status_code=403, detail="Правила нужно писать только в текущей директории, не пытайтесь выйти за её пределы.")
    return abs_path

@app.get("/api/rules/list")
async def list_rules(username: str = Depends(get_current_username)):
    files_list = []
    if not os.path.exists(RULES_ROOT):
        return JSONResponse(content=[])

    for root, dirs, files in os.walk(RULES_ROOT):
        for file in files:
            if file.endswith(".rule") or file.endswith(".rule.disabled"):
                rel_path = os.path.relpath(os.path.join(root, file), RULES_ROOT)
                files_list.append({
                    "path": rel_path,
                    "enabled": file.endswith(".rule")
                })

    files_list.sort(key=lambda x: x["path"])
    return JSONResponse(content=files_list)

@app.post("/api/rules/toggle")
async def toggle_rule(request: Request, username: str = Depends(get_current_username)):
    try:
        data = await request.json()
        path = data.get("path")
        if not path:
            raise HTTPException(status_code=400, detail="Путь к файлу необходим")

        full_path = validate_rule_path(path)

        # расширение для выключения правил
        if path.endswith(".rule"):
            new_path = full_path + ".disabled"
        elif path.endswith(".rule.disabled"):
            new_path = full_path[:-9] 
        else:
            raise HTTPException(status_code=400, detail="Неверный формат файла")

        if not os.path.exists(full_path):
             raise HTTPException(status_code=404, detail="Не найден файл")

        os.rename(full_path, new_path)

        # рестарт движка
        if hasattr(app.state, 'rule_engine'):
            app.state.rule_engine.reload_rules()

        return JSONResponse(content={"status": "ok", "message": "Состояние правила изменено"})
    except HTTPException as he:
        raise he
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/api/rules/delete")
async def delete_rule(request: Request, username: str = Depends(get_current_username)):
    try:
        data = await request.json()
        path = data.get("path")
        if not path:
            raise HTTPException(status_code=400, detail="Путь к файлу необходим")

        full_path = validate_rule_path(path)
        if not os.path.exists(full_path):
             raise HTTPException(status_code=404, detail="Не найден файл")

        os.remove(full_path)

        if hasattr(app.state, 'rule_engine'):
            app.state.rule_engine.reload_rules()

        return JSONResponse(content={"status": "ok", "message": "Правило удалено"})
    except HTTPException as he:
        raise he
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/api/rules/rename")
async def rename_rule(request: Request, username: str = Depends(get_current_username)):
    try:
        data = await request.json()
        old_path = data.get("old_path")
        new_path = data.get("new_path")

        if not old_path or not new_path:
            raise HTTPException(status_code=400, detail="Старый и новый пути необходимы")

        full_old_path = validate_rule_path(old_path)
        full_new_path = validate_rule_path(new_path)

        if not os.path.exists(full_old_path):
             raise HTTPException(status_code=404, detail="Файл не найден")

        if os.path.exists(full_new_path):
            raise HTTPException(status_code=400, detail="Такой путь уже существует")


        os.makedirs(os.path.dirname(full_new_path), exist_ok=True)

        os.rename(full_old_path, full_new_path)

        if hasattr(app.state, 'rule_engine'):
            app.state.rule_engine.reload_rules()

        return JSONResponse(content={"status": "ok", "message": "Правило переименовано"})
    except HTTPException as he:
        raise he
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/api/rules/file")
async def get_rule_content(path: str, username: str = Depends(get_current_username)):
    try:
        full_path = validate_rule_path(path)
        if not os.path.exists(full_path):
            raise HTTPException(status_code=404, detail="Файл не найден")

        with open(full_path, "r") as f:
            content = f.read()
        return JSONResponse(content={"path": path, "content": content})
    except HTTPException as he:
        raise he
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/api/rules/file")
async def save_rule_content(request: Request, username: str = Depends(get_current_username)):
    try:
        data = await request.json()
        path = data.get("path")
        content = data.get("content")

        if not path or content is None:
            raise HTTPException(status_code=400, detail="Путь и содержимое необходимы")

        full_path = validate_rule_path(path)


        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        with open(full_path, "w") as f:
            f.write(content)

        return JSONResponse(content={"status": "ok", "message": "Правило сохранено"})
    except HTTPException as he:
        raise he
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/api/rules/reload")
async def reload_rules_endpoint(username: str = Depends(get_current_username)):
    if hasattr(app.state, 'rule_engine'):
        try:
            app.state.rule_engine.reload_rules()
            return JSONResponse(content={"status": "ok", "message": "Движок правил перезагружен, правила обновлены"})
        except Exception as e:
            return JSONResponse(status_code=500, content={"error": str(e)})
    else:
        return JSONResponse(status_code=503, content={"error": "Движок правил недоступен"})
