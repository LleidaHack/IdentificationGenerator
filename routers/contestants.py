from fastapi import APIRouter, Depends, HTTPException, Response
from typing import List, Dict, Any
from repositories.contestant_repository import ContestantRepository
from dependencies import get_contestant_repository, get_pdf_service, get_card_generator_service
from services.pdf_service import PDFService
from services.card_generator_service import CardGeneratorService

router = APIRouter(prefix="/contestants", tags=["contestants"])

@router.get("")
def get_contestants(repo: ContestantRepository = Depends(get_contestant_repository)) -> List[Dict[str, Any]]:
    users = repo.get_all()
    return [{"name": u.name, "id": u.id, "type": u.type} for u in users]

@router.get("/pdf")
def get_contestants_pdf(
    repo: ContestantRepository = Depends(get_contestant_repository),
    pdf_service: PDFService = Depends(get_pdf_service),
    card_service: CardGeneratorService = Depends(get_card_generator_service)
):
    users = repo.get_all()
    if not users:
        raise HTTPException(status_code=404, detail="No contestants found")
    
    try:
        images = card_service.generate_multiple_cards(users)
        pdf_bytes = pdf_service.create_pdf(images)
        return Response(content=pdf_bytes, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=contestants.pdf"})
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{user_id}/card")
def get_contestant_card(
    user_id: str,
    repo: ContestantRepository = Depends(get_contestant_repository),
    card_service: CardGeneratorService = Depends(get_card_generator_service)
):
    user = repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Contestant not found")
    
    try:
        img_bytes = card_service.generate_card_png_bytes(user)
        return Response(content=img_bytes, media_type="image/png")
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
