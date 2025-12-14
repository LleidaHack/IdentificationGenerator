from fastapi import APIRouter, Depends, HTTPException, Response
from typing import List, Dict, Any
from repositories.mentor_repository import MentorRepository
from dependencies import get_mentor_repository, get_pdf_service, get_card_generator_service
from services.pdf_service import PDFService
from services.card_generator_service import CardGeneratorService

router = APIRouter(prefix="/mentors", tags=["mentors"])

@router.get("")
def get_mentors(repo: MentorRepository = Depends(get_mentor_repository)) -> List[Dict[str, Any]]:
    mentors = repo.get_all()
    return [{"name": m.name, "id": m.id, "type": m.type} for m in mentors]

@router.get("/pdf")
def get_mentors_pdf(
    repo: MentorRepository = Depends(get_mentor_repository),
    pdf_service: PDFService = Depends(get_pdf_service),
    card_service: CardGeneratorService = Depends(get_card_generator_service)
):
    mentors = repo.get_all()
    if not mentors:
        raise HTTPException(status_code=404, detail="No mentors found")
    
    try:
        images = card_service.generate_multiple_cards(mentors)
        pdf_bytes = pdf_service.create_pdf(images)
        return Response(content=pdf_bytes, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=mentors.pdf"})
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{name}/card")
def get_mentor_card(
    name: str,
    repo: MentorRepository = Depends(get_mentor_repository),
    card_service: CardGeneratorService = Depends(get_card_generator_service)
):
    mentor = repo.get_by_name(name)
    if not mentor:
        raise HTTPException(status_code=404, detail="Mentor not found")
    
    try:
        img_bytes = card_service.generate_card_png_bytes(mentor)
        return Response(content=img_bytes, media_type="image/png")
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
