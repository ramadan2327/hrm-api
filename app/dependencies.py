from app.database import SessionLocal

def get_db():
    """
    Dependency injection for database session.
    Yields a session and closes it after the request is done.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()