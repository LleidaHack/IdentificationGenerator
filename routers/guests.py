from fastapi import APIRouter, Depends, HTTPException, Response
from typing import List, Dict, Any
from repositories.guest_repository import GuestRepository
from dependencies import get_guest_repository, get_pdf_service, get_card_generator_service
from services.pdf_service import PDFService
from services.card_generator_service import CardGeneratorService

router = APIRouter(prefix="/guests", tags=["guests"])

@router.get("")
def get_guests(repo: GuestRepository = Depends(get_guest_repository)) -> List[Dict[str, Any]]:
    guests = repo.get_all()
    return [{"name": g.name, "id": g.id, "type": g.type} for g in guests]

@router.get("/pdf")
def get_guests_pdf(
    repo: GuestRepository = Depends(get_guest_repository),
    pdf_service: PDFService = Depends(get_pdf_service),
    card_service: CardGeneratorService = Depends(get_card_generator_service)
):
    guests = repo.get_all()
    if not guests:
        raise HTTPException(status_code=404, detail="No guests found")
    
    try:
        images = card_service.generate_multiple_cards(guests)
        pdf_bytes = pdf_service.create_pdf(images)
        return Response(content=pdf_bytes, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=guests.pdf"})
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{name}/card")
def get_guest_card(
    name: str,
    repo: GuestRepository = Depends(get_guest_repository),
    card_service: CardGeneratorService = Depends(get_card_generator_service)
):
    guest = repo.get_by_name(name)
    if not guest:
        raise HTTPException(status_code=404, detail="Guest not found")
    
    try:
        img_bytes = card_service.generate_card_png_bytes(guest)
        return Response(content=img_bytes, media_type="image/png")
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
