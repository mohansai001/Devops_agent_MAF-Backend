from fastapi import APIRouter, WebSocket, WebSocketDisconnect #type: ignore

from fastapi.middleware.cors import CORSMiddleware #type: ignore

import asyncio

from typing import List

router = APIRouter()

# Allow React frontend connection

# router.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Replace with frontend URL in production
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
 
 
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def send_log(self, message: str):
        disconnected_clients = []
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                disconnected_clients.append(connection)
        for conn in disconnected_clients:
            self.disconnect(conn)
 
manager = ConnectionManager()
 
 
# WebSocket endpoint

@router.websocket("/ws/logs")
async def websocket_logs(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
 
 
# Example API endpoint to trigger logs

@router.get("/start-process")
async def start_process():
    async def generate_logs():
        for i in range(1, 11):
            log_message = f"Processing step {i}/10"
            print(log_message)
            await manager.send_log(log_message)
            await asyncio.sleep(1)
        await manager.send_log("Process completed successfully")
    asyncio.create_task(generate_logs())
 
    return {"message": "Process started"}
 