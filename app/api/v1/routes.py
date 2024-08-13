from fastapi import APIRouter

from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.chat import router as chat_router
# from app.api.v1.endpoints.groups import router as groups_router
routers = APIRouter()
router_list = [auth_router,chat_router]

for router in router_list:
    router.tags = routers.tags.append("v1")
    routers.include_router(router)  
