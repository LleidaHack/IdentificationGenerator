from fastapi import APIRouter, Depends, HTTPException, Response
from typing import List, Dict, Any
from repositories.volunteer_repository import VolunteerRepository
from dependencies import get_volunteer_repository, get_pdf_service, get_card_generator_service
from services.pdf_service import PDFService
from services.card_generator_service import CardGeneratorService

router = APIRouter(prefix="/volunteers", tags=["volunteers"])

@router.get("")
def get_volunteers(repo: VolunteerRepository = Depends(get_volunteer_repository)) -> List[Dict[str, Any]]:
    volunteers = repo.get_all()
    return [{"name": v.name, "id": v.id, "type": v.type} for v in volunteers]

@router.get("/pdf")
def get_volunteers_pdf(
    repo: VolunteerRepository = Depends(get_volunteer_repository),
    pdf_service: PDFService = Depends(get_pdf_service),
    card_service: CardGeneratorService = Depends(get_card_generator_service)
):
    volunteers = repo.get_all()
    if not volunteers:
        raise HTTPException(status_code=404, detail="No volunteers found")
    
    try:
        images = card_service.generate_multiple_cards(volunteers)
        pdf_bytes = pdf_service.create_pdf(images)
        return Response(content=pdf_bytes, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=volunteers.pdf"})
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{name}/card")
def get_volunteer_card(
    name: str,
    repo: VolunteerRepository = Depends(get_volunteer_repository),
    card_service: CardGeneratorService = Depends(get_card_generator_service)
):
    volunteer = repo.get_by_name(name)
    if not volunteer:
        raise HTTPException(status_code=404, detail="Volunteer not found")
    
    try:
        img_bytes = card_service.generate_card_png_bytes(volunteer)
        return Response(content=img_bytes, media_type="image/png")
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
