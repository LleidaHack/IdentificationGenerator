from typing import List, Optional
from models.contestant import Contestant
from services.api_service import APIService

class ContestantRepository:
    def __init__(self, api_service: APIService):
        self.api_service = api_service

    def get_all(self) -> List[Contestant]:
        usrs = self.api_service.get_accepted_hackers()
        return [Contestant(usr['id'], usr) for usr in usrs]

    def get_by_id(self, user_id: str) -> Optional[Contestant]:
        usrs = self.api_service.get_accepted_hackers()
        for usr in usrs:
            if str(usr['id']) == str(user_id):
                return Contestant(usr['id'], usr)
        return None
