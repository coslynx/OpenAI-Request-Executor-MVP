import os
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import requests
import jwt
from datetime import datetime, timedelta

from models.request import Request, Base, engine, SessionLocal
from services.openai_service import OpenAIService
from utils.logger import logger

load_dotenv()

app = FastAPI()

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency injection for database sessions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# JWT Authentication Configuration
JWT_SECRET = os.getenv("JWT_SECRET")

# API Endpoint for Processing Requests 
@app.post("/requests/")
async def create_request(request_text: str, db: Session = Depends(get_db)):
    try:
        openai_service = OpenAIService()

        # Validate user input and perform sanitization
        if not request_text or len(request_text) < 5:
            raise HTTPException(status_code=400, detail="Invalid request text")

        # Generate API call (utilize commands.json mapping if needed)
        response = await openai_service.execute_request(request_text)

        # Store request and response in database
        new_request = Request(text=request_text, status="completed", response=response)
        db.add(new_request)
        db.commit()
        db.refresh(new_request)

        return {"request_id": new_request.id, "status": "completed"}

    except Exception as e:
        logger.error(f"Error processing request: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")

# API Endpoint for Retrieving Responses 
@app.get("/responses/{request_id}")
async def get_response(request_id: int, db: Session = Depends(get_db)):
    try:
        request = db.query(Request).filter(Request.id == request_id).first()
        if not request:
            raise HTTPException(status_code=404, detail="Request not found")
        return {"response": request.response}
    except Exception as e:
        logger.error(f"Error retrieving response: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Authentication Endpoint (Example)
@app.post("/authenticate")
async def authenticate(username: str, password: str):
    try:
        # Implement actual authentication logic (database lookup, password hashing)
        if username == "user" and password == "password":
            payload = {"username": username, "exp": datetime.utcnow() + timedelta(minutes=30)}
            token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
            return {"access_token": token.decode()}
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials")
    except Exception as e:
        logger.error(f"Authentication error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Error Handling and Logging
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTP Exception: {exc}")
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)