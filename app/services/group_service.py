from app.repository.user_repository import UserRepository
from app.services.base_service import BaseService
from app.repository.group_repository import GroupRepository

class GroupService(BaseService):
    def __init__(self, group_repository: GroupRepository):
        self.group_repository = group_repository
        super().__init__(group_repository)
    
    def get_groups(self) :
        return self.group_repository.load_groups()
