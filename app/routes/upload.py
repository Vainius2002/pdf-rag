# we import Uploadfile, because we are trying to receive html's form data which is not sent via json, rather a form-encoded data
#   and since fastapi defaults to expecing json data, so we use UploadFile = "this argument is a FILE from a form" and
#   Form = "this argument is a regular INPUT from form"
# Also for using Form we have to first tell python what type is it, so f.e question : str = Form()
# Also we use async, to tell python this function is pausable, so that we can then use await = pause this function so it doesnt block servers requests from other users

from fastapi import APIRouter, UploadFile, Depends, HTTPException
from app.services.pdf import extract_pdf
from app.services.chunker import chunker
from app.services.embeddings import embed
from app.services.storage import save_document
from app.dependencies import get_current_user
from app.models import User

router = APIRouter()


@router.post("/upload")
async def upload(pdf: UploadFile, user: User = Depends(get_current_user)):
    # Guard: must be a PDF
    if pdf.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="File must be a PDF")

    chunks_with_embeddings = []

    pdf_data = await pdf.read()

    # Guard: catch parse errors from corrupt PDFs (PyMuPDF raises here)
    try:
        pdf_polished = extract_pdf(pdf_data)
    except Exception:
        raise HTTPException(status_code=400, detail="Could not parse PDF")

    # Guard: image-only or empty PDFs extract to empty text
    if not pdf_polished or not pdf_polished.strip():
        raise HTTPException(status_code=400, detail="PDF contains no extractable text")

    chunks = chunker(pdf_polished)
    if not chunks:
        raise HTTPException(status_code=400, detail="PDF had no content to chunk")

    for chunk in chunks:
        embedded = embed(chunk)
        chunks_with_embeddings.append((chunk, embedded))

    document_id = save_document(
        filename=pdf.filename,
        chunks_with_embeddings=chunks_with_embeddings,
        user_id=user.id,
    )
    return {"document_id": document_id}
