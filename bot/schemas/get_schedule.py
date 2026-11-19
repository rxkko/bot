from pydantic import BaseModel, Field

class Base(BaseModel):
    pass

class GetScheduleByGroup(Base):
    week: str = Field(default="12", min_length=1, max_length=100)
    group: str = Field(default="21ld", min_length=1, max_length=100)

class GetScheduleByName(Base):
    week: str = Field(default="12", min_length=1, max_length=100)
    name: str = Field(min_length=1, max_length=100)