
from contextlib import AbstractContextManager
from typing import Callable, Optional,Dict,List
from app.cores.exceptions import DuplicatedError, NotFoundError


from sqlalchemy.orm import Session


from app.repository.base_repository import BaseRepository
from sqlmodel import select,Session
from app.schemas.message_schema import message_schema
from sqlalchemy.exc import IntegrityError
from app.models.groups import Groups

class GroupRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory
        super().__init__(session_factory, Groups)


    def load_groups(self) -> List[Dict]:
        with self.session_factory() as session:
            print(1)
            query = session.query(self.model)
            print(2)
            groups = query.all()
            print(3)
           
            return groups

    