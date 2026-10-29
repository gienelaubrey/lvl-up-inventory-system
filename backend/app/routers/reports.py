from datetime import date

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
)
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.supplier_report import (
    build_supplier_report_pdf,
    get_supplier_report_data,
)


router = APIRouter(
    prefix="/reports",
    tags=["Reports"],
)


@router.get(
    "/suppliers/{supplier_id}/pdf"
)
def supplier_report_pdf(
    supplier_id: int,

    start_date: date = Query(...),

    end_date: date = Query(...),

    db: Session = Depends(get_db),
):
    if end_date < start_date:
        raise HTTPException(
            status_code=400,
            detail=(
                "End date cannot be "
                "before start date"
            ),
        )

    try:
        report_data = (
            get_supplier_report_data(
                db=db,
                supplier_id=supplier_id,
                start_date=start_date,
                end_date=end_date,
            )
        )
    except ValueError:
        raise HTTPException(
            status_code=404,
            detail="Supplier not found",
        )

    pdf_buffer = (
        build_supplier_report_pdf(
            report_data
        )
    )

    filename = (
        f"supplier_report_"
        f"{supplier_id}_"
        f"{start_date}_"
        f"{end_date}.pdf"
    )

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition":
                f'attachment; '
                f'filename="{filename}"'
        },
    )