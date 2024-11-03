import pytest
import pytest_cov
import pytest_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from models.request import Request, Base, engine
from dotenv import load_dotenv

pytest_dotenv.load_dotenv()

# Database Setup
engine = create_engine(os.getenv("DATABASE_URL"))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database session for each test function."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class TestRequest:

    def test_request_creation(self, db_session):
        """Test creating a new Request object."""
        new_request = Request(text="Write a poem about a cat", status="pending")
        db_session.add(new_request)
        db_session.commit()
        db_session.refresh(new_request)
        assert new_request.text == "Write a poem about a cat"
        assert new_request.status == "pending"

    def test_request_update(self, db_session):
        """Test updating an existing Request object."""
        new_request = Request(text="Write a story about a dog", status="pending")
        db_session.add(new_request)
        db_session.commit()
        db_session.refresh(new_request)
        new_request.status = "completed"
        db_session.commit()
        db_session.refresh(new_request)
        assert new_request.status == "completed"

    def test_request_deletion(self, db_session):
        """Test deleting an existing Request object."""
        new_request = Request(text="Write a song about a bird", status="pending")
        db_session.add(new_request)
        db_session.commit()
        db_session.refresh(new_request)
        db_session.delete(new_request)
        db_session.commit()
        assert db_session.query(Request).filter(Request.id == new_request.id).first() is None

    def test_request_validation_errors(self, db_session):
        """Test validation errors when creating a Request."""
        with pytest.raises(ValueError):
            Request(text="short", status="invalid")  # Invalid status

        with pytest.raises(ValueError):
            Request(text="", status="pending")  # Empty text