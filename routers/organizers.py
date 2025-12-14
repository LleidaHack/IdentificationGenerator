from fastapi import APIRouter, Depends, HTTPException, Response
from typing import List, Dict, Any
from repositories.organizer_repository import OrganizerRepository
from dependencies import get_organizer_repository, get_pdf_service, get_card_generator_service
from services.pdf_service import PDFService
from services.card_generator_service import CardGeneratorService

router = APIRouter(prefix="/organizers", tags=["organizers"])

@router.get("")
def get_organizers(repo: OrganizerRepository = Depends(get_organizer_repository)) -> List[Dict[str, Any]]:
    organizers = repo.get_all()
    return [{"name": o.name, "id": o.id, "type": o.type} for o in organizers]

@router.get("/pdf")
def get_organizers_pdf(
    repo: OrganizerRepository = Depends(get_organizer_repository),
    pdf_service: PDFService = Depends(get_pdf_service),
    card_service: CardGeneratorService = Depends(get_card_generator_service)
):
    organizers = repo.get_all()
    if not organizers:
        raise HTTPException(status_code=404, detail="No organizers found")
    
    try:
        images = card_service.generate_multiple_cards(organizers)
        pdf_bytes = pdf_service.create_pdf(images)
        return Response(content=pdf_bytes, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=organizers.pdf"})
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{name}/card")
def get_organizer_card(
    name: str,
    repo: OrganizerRepository = Depends(get_organizer_repository),
    card_service: CardGeneratorService = Depends(get_card_generator_service)
):
    organizer = repo.get_by_name(name)
    if not organizer:
        raise HTTPException(status_code=404, detail="Organizer not found")
    
    try:
        img_bytes = card_service.generate_card_png_bytes(organizer)
        return Response(content=img_bytes, media_type="image/png")
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
