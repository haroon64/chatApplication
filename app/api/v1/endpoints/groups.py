# from dependency_injector.wiring import Provide, inject
# from fastapi import APIRouter, Depends

# from app.cores.container import Container
# from app.services.group_service import GroupService
# from app.schemas.groups_schema import get_groups
# from typing import List


# router = APIRouter(
#     prefix="/groups",
#     tags=["groups"],
# )

# @router.get('/groups', response_model=List[get_groups])
# @inject
# async def groups( service: GroupService = Depends(Provide[Container.group_service])):
#     return service.get_groups()
