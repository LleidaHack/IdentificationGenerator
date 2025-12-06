from fastapi import APIRouter, Depends, HTTPException, Response
from typing import List, Dict, Any
from repositories.company_repository import CompanyRepository
from dependencies import get_company_repository, get_pdf_service, get_card_generator_service
from services.pdf_service import PDFService
from services.card_generator_service import CardGeneratorService

router = APIRouter(prefix="/companies", tags=["companies"])

@router.get("")
def get_companies(repo: CompanyRepository = Depends(get_company_repository)) -> List[Dict[str, Any]]:
    companies = repo.get_all()
    return [{"name": c.name, "id": c.id, "type": c.type} for c in companies]

@router.get("/pdf")
def get_companies_pdf(
    repo: CompanyRepository = Depends(get_company_repository),
    pdf_service: PDFService = Depends(get_pdf_service),
    card_service: CardGeneratorService = Depends(get_card_generator_service)
):
    companies = repo.get_all()
    if not companies:
        raise HTTPException(status_code=404, detail="No companies found")
    
    try:
        images = card_service.generate_multiple_cards(companies)
        pdf_bytes = pdf_service.create_pdf(images)
        return Response(content=pdf_bytes, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=companies.pdf"})
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
