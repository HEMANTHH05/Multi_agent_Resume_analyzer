import asyncio
import os
import uuid
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, UploadFile, File, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import json

from orchestrator import Orchestrator

app = FastAPI(title="Resume Modifier API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory session storage: session_id → context dict
sessions: dict[str, dict] = {}
# Orchestrator instances keyed by session_id
orchestrators: dict[str, Orchestrator] = {}


@app.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    """Accept resume file, store bytes + extension, return session_id."""
    file_bytes = await file.read()
    file_extension = Path(file.filename).suffix if file.filename else ".pdf"

    session_id = str(uuid.uuid4())
    sessions[session_id] = {
        "resume_bytes": file_bytes,
        "file_extension": file_extension,
        "session_id": session_id,
    }

    return {
        "session_id": session_id,
        "filename": file.filename,
        "size": len(file_bytes),
    }


@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await websocket.accept()

    context = sessions.get(session_id)
    if not context:
        await websocket.send_text(json.dumps({
            "type": "PIPELINE_ERROR",
            "message": "Session not found. Please re-upload your resume."
        }))
        await websocket.close()
        return

    async def ws_send(message: str):
        try:
            await websocket.send_text(message)
        except Exception:
            pass

    orchestrator = Orchestrator(ws_send=ws_send, context=context)
    orchestrators[session_id] = orchestrator

    # Wait for START message with JD text
    try:
        raw = await websocket.receive_text()
        msg = json.loads(raw)

        if msg.get("type") != "START":
            await ws_send(json.dumps({
                "type": "PIPELINE_ERROR",
                "message": "Expected START message first."
            }))
            return

        context["jd_text"] = msg.get("jd_text", "")

        # Run pipeline in background, while main loop handles USER_REPLY messages
        pipeline_task = asyncio.create_task(orchestrator.run())

        # Listen for user replies while pipeline is running
        while not pipeline_task.done():
            try:
                raw = await asyncio.wait_for(websocket.receive_text(), timeout=0.5)
                msg = json.loads(raw)
                if msg.get("type") == "USER_REPLY":
                    await orchestrator.receive_user_reply(msg.get("text", ""))
            except asyncio.TimeoutError:
                continue
            except WebSocketDisconnect:
                pipeline_task.cancel()
                break
            except Exception:
                break

        # Ensure pipeline completes
        if not pipeline_task.cancelled():
            await pipeline_task

    except WebSocketDisconnect:
        pass
    except Exception as e:
        await ws_send(json.dumps({
            "type": "PIPELINE_ERROR",
            "message": str(e),
        }))
    finally:
        orchestrators.pop(session_id, None)


@app.get("/download/{session_id}")
async def download_resume(session_id: str):
    """Serve the generated .docx file."""
    docx_path = f"/tmp/{session_id}_resume.docx"
    if not os.path.exists(docx_path):
        return {"error": "File not found"}
    return FileResponse(
        path=docx_path,
        filename="tailored_resume.docx",
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )


@app.get("/health")
async def health():
    return {"status": "ok"}
