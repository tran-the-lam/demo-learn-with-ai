from sqlalchemy import create_engine  
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import sessionmaker 
from sqlalchemy import inspect
import types
import json
from typing import Any, Optional
import os

# URL kết nối cơ sở dữ liệu (thay đổi theo cấu hình của bạn)  
# example = "postgresql://user:password@localhost/dbname" 
# example = "sqlite:///webui.db" 
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///webui.db")
print("DATABASE_URL", DATABASE_URL)

engine = create_engine(DATABASE_URL)  

def log_all_tables():  
    inspector = inspect(engine)  # Use SQLAlchemy's inspector  
    tables = inspector.get_table_names()  # Get all table names  
    print("Tables in the database:")  
    for table in tables:  
        print(f"- {table}")
        
log_all_tables()

# Tạo session  
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  

# Base class để định nghĩa các model  
Base = declarative_base()  


# if "sqlite" in SQLALCHEMY_DATABASE_URL:
#     engine = create_engine(
#         SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
#     )
# else:
#     if DATABASE_POOL_SIZE > 0:
#         engine = create_engine(
#             SQLALCHEMY_DATABASE_URL,
#             pool_size=DATABASE_POOL_SIZE,
#             max_overflow=DATABASE_POOL_MAX_OVERFLOW,
#             pool_timeout=DATABASE_POOL_TIMEOUT,
#             pool_recycle=DATABASE_POOL_RECYCLE,
#             pool_pre_ping=True,
#             poolclass=QueuePool,
#         )
#     else:
#         engine = create_engine(
#             SQLALCHEMY_DATABASE_URL, pool_pre_ping=True, poolclass=NullPool
#         )


SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, expire_on_commit=False
)
Base = declarative_base()

def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# class JSONField(types.TypeDecorator):
#     impl = types.Text
#     cache_ok = True

#     def process_bind_param(self, value: Optional[_T], dialect: Dialect) -> Any:
#         return json.dumps(value)

#     def process_result_value(self, value: Optional[_T], dialect: Dialect) -> Any:
#         if value is not None:
#             return json.loads(value)

#     def copy(self, **kw: Any) -> Self:
#         return JSONField(self.impl.length)

#     def db_value(self, value):
#         return json.dumps(value)

    # def python_value(self, value):
    #     if value is not None:
    #         return json.loads(value)