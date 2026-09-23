import os
import sys

# Ensure backend can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.rag.knowledge_base import get_knowledge_base
from backend.rag.seed_data import SEED_REGULATIONS
from backend.database.session import init_db, SessionLocal
from backend.database.models import RegulatoryDoc


def initialize_rag():
    print("=" * 60)
    print("Initializing LexGuard Sovereign Regulatory Vector Store")
    print("=" * 60)

    # 1. Initialize DB tables
    print("1. Initializing database schema...")
    init_db()
    print("   Database tables and subsidiary pillars verified.")

    # 2. Vectorize and seed Knowledge Base
    print("2. Indexing Nigerian Regulatory Frameworks into FAISS...")
    kb = get_knowledge_base()

    # Reset metadata and index if re-seeding
    if kb.index.ntotal == 0:
        added = kb.add_chunks(SEED_REGULATIONS)
        print(f"   Indexed {added} regulatory clauses into local FAISS vector store.")
    else:
        print(f"   FAISS store already contains {kb.index.ntotal} active regulatory clauses.")

    # 3. Synchronize with regulatory_docs table
    db = SessionLocal()
    try:
        frameworks = {}
        for r in SEED_REGULATIONS:
            f = r["framework"]
            if f not in frameworks:
                frameworks[f] = {"category": r["category"], "count": 0}
            frameworks[f]["count"] += 1

        for title, info in frameworks.items():
            existing = db.query(RegulatoryDoc).filter(RegulatoryDoc.title == title).first()
            if not existing:
                doc = RegulatoryDoc(
                    title=title,
                    category=info["category"],
                    chunk_count=info["count"],
                    source_filename="seed_regulations.py"
                )
                db.add(doc)
        db.commit()
        print("   Regulatory document catalog synchronized in database.")
    finally:
        db.close()

    # 4. Run test query
    print("3. Running verification similarity query...")
    test_results = kb.search("data protection biometrics cross border cloud", category="GovTech", k=1)
    if test_results:
        top = test_results[0]
        print(f"   Matched: [{top.get('framework')}] - {top.get('title')}")
        print(f"   Citation: {top.get('citation')}")
        print(f"   Similarity: {top.get('similarity_score', 0):.4f}")
    else:
        print("   Warning: Test search returned 0 results.")

    print("=" * 60)
    print("LexGuard Vector Store setup complete! Sovereign readiness confirmed.")
    print("=" * 60)


if __name__ == "__main__":
    initialize_rag()
