from fastapi import FastAPI, Depends, HTTPException  
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app import model  
from app import schema 
from db.connect import SessionLocal
from fastapi.middleware.cors import CORSMiddleware

from datetime import datetime

print()
app = FastAPI() 

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

def get_db():  
    db = SessionLocal()  
    try:  
        yield db  
    finally:  
        db.close() 
        
@app.get("/histories", response_model=list[schema.ChatResponse])  
def get_histories(
    emails: str= "", skip: int = 0, limit: int = 10, 
    start_time: int = 0, end_time: int = int(datetime.now().timestamp()), 
    db: Session = Depends(get_db)
):  
    if len(emails) == 0:
        raise HTTPException(status_code=400, detail="Emails is empty")
    
    e = emails.split(",")
    users = db.query(model.User).filter(model.User.email.in_(e)).all()
    if len(users) == 0:
        raise HTTPException(status_code=400, detail="User not found")
    
    mapInfo = {}
    userIds = []
    for u in users:
        userIds.append(u.id)
        mapInfo[u.id] = {
            "name": u.name,
            "email": u.email,
        }
    
    # print("start_time", start_time)
    # print("end_time", end_time)
    items = db.query(model.Chat).filter(
        model.Chat.user_id.in_(userIds),
        model.Chat.updated_at > start_time,
        model.Chat.updated_at < end_time,
    ).order_by(desc(model.Chat.updated_at)).offset(skip).limit(limit).all()
    
    # format the response
    for item in items:
        item.email = mapInfo[item.user_id]["email"]
        item.user_name = mapInfo[item.user_id]["name"]
        
    return items

@app.get("/histories/count", response_model=int)
def get_histories_count(
    emails: str= "", start_time: int = 0, end_time: int = int(datetime.now().timestamp()), 
    db: Session = Depends(get_db)
):  
    e = emails.split(",")
    users = db.query(model.User).filter(model.User.email.in_(e)).all()
    if len(users) == 0:
        raise HTTPException(status_code=400, detail="User not found")
    
    userIds = [ u.id for u in users ]
        
    return db.query(model.Chat).filter(
        model.Chat.user_id.in_(userIds),
        model.Chat.updated_at > start_time,
        model.Chat.updated_at < end_time,
    ).count()

    