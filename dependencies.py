from services.api_service import APIService
from services.pdf_service import PDFService
from services.card_generator_service import CardGeneratorService
from repositories.contestant_repository import ContestantRepository
from repositories.company_repository import CompanyRepository
from repositories.guest_repository import GuestRepository
from repositories.mentor_repository import MentorRepository
from repositories.organizer_repository import OrganizerRepository
from repositories.volunteer_repository import VolunteerRepository
from fastapi import Depends

def get_api_service():
    return APIService()

def get_pdf_service():
    return PDFService()

def get_card_generator_service():
    return CardGeneratorService()

def get_contestant_repository(api_service: APIService = Depends(get_api_service)):
    return ContestantRepository(api_service)

def get_company_repository(api_service: APIService = Depends(get_api_service)):
    return CompanyRepository(api_service)

def get_guest_repository():
    return GuestRepository()

def get_mentor_repository():
    return MentorRepository()

def get_organizer_repository():
    return OrganizerRepository()

def get_volunteer_repository():
    return VolunteerRepository()
