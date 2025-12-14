from typing import List, Optional
from models.organizer import Organizer
import tools

class OrganizerRepository:
    def __init__(self):
        pass

    def get_all(self) -> List[Organizer]:
        res = []
        data = tools.DataFile.get_content(Organizer._DATA_FILE, 'JSON')
        for u in data['organizers']:
            res.append(Organizer(u['name']))
        return res

    def get_by_name(self, name: str) -> Optional[Organizer]:
        data = tools.DataFile.get_content(Organizer._DATA_FILE, 'JSON')
        for u in data['organizers']:
            if u['name'] == name:
                return Organizer(u['name'])
        return None
