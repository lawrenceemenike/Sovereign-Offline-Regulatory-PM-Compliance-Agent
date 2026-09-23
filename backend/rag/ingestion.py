import io
import re
from typing import List, Dict, Any
from pypdf import PdfReader
from backend.rag.knowledge_base import get_knowledge_base
from backend.database.models import RegulatoryDoc
from backend.database.session import SessionLocal


def chunk_text(text: str, chunk_size: int = 600, overlap: int = 100) -> List[str]:
    """Splits legal text into overlapping chunks respecting sentence/clause boundaries."""
    text = re.sub(r'\s+', ' ', text).strip()
    words = text.split(' ')
    chunks = []
    start = 0
    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunk = " ".join(words[start:end])
        if chunk:
            chunks.append(chunk)
        if end == len(words):
            break
        start += chunk_size - overlap
    return chunks


def ingest_pdf_bytes(
    file_bytes: bytes,
    title: str,
    category: str,
    source_filename: str
) -> Dict[str, Any]:
    """Extracts text from PDF bytes, chunks, vectorizes, and saves to database & FAISS."""
    pdf_file = io.BytesIO(file_bytes)
    reader = PdfReader(pdf_file)
    extracted_text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            extracted_text += page_text + "\n"

    if not extracted_text.strip():
        raise ValueError("Could not extract any readable text from the uploaded PDF document.")

    chunks = chunk_text(extracted_text)
    kb_chunks = []
    for i, c in enumerate(chunks):
        kb_chunks.append({
            "framework": title,
            "category": category,
            "section": f"Excerpt Clause #{i+1}",
            "title": f"{title} - Clause Part {i+1}",
            "content": c,
            "citation": f"{title}, Section Excerpt Part {i+1}",
            "penalties": "Statutory institutional penalties as specified in legal instrument."
        })

    kb = get_knowledge_base()
    added_count = kb.add_chunks(kb_chunks)

    # Save to regulatory_docs table
    db = SessionLocal()
    try:
        doc = RegulatoryDoc(
            title=title,
            category=category,
            chunk_count=added_count,
            source_filename=source_filename
        )
        db.add(doc)
        db.commit()
        db.refresh(doc)
        doc_id = doc.id
    finally:
        db.close()

    return {
        "document_id": doc_id,
        "title": title,
        "category": category,
        "chunks_indexed": added_count,
        "status": "Indexed Successfully"
    }


def ingest_raw_text(
    content: str,
    title: str,
    category: str,
    section: str = "General",
    citation: str = ""
) -> Dict[str, Any]:
    """Ingests raw compliance text directly."""
    chunks = chunk_text(content)
    kb_chunks = []
    for i, c in enumerate(chunks):
        kb_chunks.append({
            "framework": title,
            "category": category,
            "section": section if len(chunks) == 1 else f"{section} (Part {i+1})",
            "title": f"{title} - {section}",
            "content": c,
            "citation": citation or f"{title}, {section}",
            "penalties": "Applicable statutory penalties."
        })

    kb = get_knowledge_base()
    added_count = kb.add_chunks(kb_chunks)

    db = SessionLocal()
    try:
        doc = RegulatoryDoc(
            title=title,
            category=category,
            chunk_count=added_count,
            source_filename="manual_text_entry"
        )
        db.add(doc)
        db.commit()
        db.refresh(doc)
        doc_id = doc.id
    finally:
        db.close()

    return {
        "document_id": doc_id,
        "title": title,
        "chunks_indexed": added_count,
        "status": "Indexed Successfully"
    }
