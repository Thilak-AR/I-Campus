from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Import models so that Base.metadata is aware of them
from app.db import models  # noqa: E402, F401
