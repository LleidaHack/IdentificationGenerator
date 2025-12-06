from typing import List, Optional
from models.volunteer import Volunteer
import tools

class VolunteerRepository:
    def __init__(self):
        pass

    def get_all(self) -> List[Volunteer]:
        res = []
        data = tools.DataFile.get_content(Volunteer._DATA_FILE, 'JSON')
        for u in data['volunteers']:
            res.append(Volunteer(u['name']))
        return res

    def get_by_name(self, name: str) -> Optional[Volunteer]:
        data = tools.DataFile.get_content(Volunteer._DATA_FILE, 'JSON')
        for u in data['volunteers']:
            if u['name'] == name:
                return Volunteer(u['name'])
        return None
