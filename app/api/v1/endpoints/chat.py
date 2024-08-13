import json
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from app.cores.web_socket import ConnectionManager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, WebSocket
from datetime import datetime
from sqlalchemy.orm import Session  
from app.schemas.message_schema import message_schema
from app.cores.container import Container
from app.services.message_service import MessageService
from app.schemas.message_schema import  get_message
from app.services.group_service import GroupService
from app.schemas.groups_schema import get_groups

manager = ConnectionManager()

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
)
@router.websocket("/message/{group_id}")
@inject
async def websocket_endpoint(websocket: WebSocket, group_id: int, service: MessageService = Depends(Provide[Container.message_service])):
    await manager.connect(websocket, group_id)
    try:
        while True:
            data = await websocket.receive_text()
            parsed_data = json.loads(data)

            # Validate and parse data into schema
            message_info = message_schema(
                sender_id=parsed_data["client_id"],
                content=parsed_data["text"],
                group_id=group_id
            )

            # Modify the type property to 'received'
            parsed_data["type"] = "received"

            # Prepare the response
            response = {"message": json.dumps(parsed_data)}

            # Broadcast message
            status = await manager.broadcast(json.dumps(response), group_id, sender=websocket)
            
            # Save message to the database if it was successfully sent
            if status:
                service.save_message(message_info)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        try:
            await manager.send_personal_message("Bye!!!", websocket)
            await manager.broadcast(f"Client #{message_info.sender_id} has left", group_id, sender=websocket)
        except RuntimeError as e:
            print(f"Error sending message after disconnect: {e}")       
    

@router.get("/load_messages/{group_id}",response_model=List[get_message])
@inject
async def load_message(group_id: int, service: MessageService = Depends(Provide[Container.message_service])):
    return service.get_messages(group_id)


@router.get('/groups', response_model=List[get_groups])
@inject
async def groups( service: GroupService = Depends(Provide[Container.group_service])):
    return service.get_groups()
