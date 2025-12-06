from typing import List, Optional
from models.mentor import Mentor
import tools

class MentorRepository:
    def __init__(self):
        pass

    def get_all(self) -> List[Mentor]:
        res = []
        data = tools.DataFile.get_content(Mentor._DATA_FILE, 'JSON')
        for u in data['mentors']:
            res.append(Mentor(u['name']))
        return res

    def get_by_name(self, name: str) -> Optional[Mentor]:
        data = tools.DataFile.get_content(Mentor._DATA_FILE, 'JSON')
        for u in data['mentors']:
            if u['name'] == name:
                return Mentor(u['name'])
        return None
