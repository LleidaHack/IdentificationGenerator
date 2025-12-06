from typing import List, Optional
from models.guest import Guest
import tools

class GuestRepository:
    def __init__(self):
        pass

    def get_all(self) -> List[Guest]:
        res = []
        data = tools.DataFile.get_content(Guest._DATA_FILE, 'JSON')
        for u in data['guests']:
            res.append(Guest(u['name'], u['type'], u['logo'], u['qr']))
        return res

    def get_by_name(self, name: str) -> Optional[Guest]:
        data = tools.DataFile.get_content(Guest._DATA_FILE, 'JSON')
        for u in data['guests']:
            if u['name'] == name:
                return Guest(u['name'], u['type'], u['logo'], u['qr'])
        return None
