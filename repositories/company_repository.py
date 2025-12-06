from typing import List
from models.company import Company
from services.api_service import APIService
import Config

class CompanyRepository:
    def __init__(self, api_service: APIService):
        self.api_service = api_service

    def get_all(self) -> List[Company]:
        res = []
        tiers_config = [(1, 8), (2, 5), (3, 5)]
        
        for tier_num, count in tiers_config:
            comps = self.api_service.get_companies_by_tier(tier_num)
            for comp in comps:
                for _ in range(count):
                    res.append(Company(comp['name'], comp['image']))
                    if Config.TEST:
                        break
                if Config.TEST:
                    break
        return res
