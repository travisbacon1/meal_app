from sqlmodel import Field, SQLModel, JSON, Column
from typing import Optional, Dict, Pattern, Literal
import re
import json


class InvalidDateFormat(Exception):
    """Custom exception for invalid date formats"""
    pass


class MissingIngredientType(Exception):
    """Custom exception when Ingredient objects are not passed a Type attribute"""
    pass


class TestTable(SQLModel, table=True):
    __table_args__ = {'extend_existing': True}
    __tablename__ = "TestTable"
    Name: str = Field(primary_key=True)
    Staple: str
    Book: Optional[str] = None
    Page: Optional[str] = None
    website: Optional[str] = None
    Fresh_Ingredients: Dict = Field(default={}, sa_column=Column(JSON))
    Dairy_Ingredients: Dict = Field(default={}, sa_column=Column(JSON))
    Dry_Ingredients: Dict = Field(default={}, sa_column=Column(JSON))
    Tinned_Ingredients: Dict = Field(default={}, sa_column=Column(JSON))
    Last_Made:  Pattern[str]
    Spring_Summer: Optional[int] = None
    Autumn_Winter: Optional[int] = None
    Quick_Easy: Optional[int] = None
    Special: Optional[int] = None


    def __new__(cls, *args, **kwargs):
        if kwargs.get('Last_Made') is None:
            return super(TestTable, cls).__new__(cls, *args, **kwargs)
        elif not re.match(r'[\d]{4}-[\d]{2}-[\d]{2}', kwargs['Last_Made']):
            raise InvalidDateFormat('Invalid date format')
        else:
            return super(TestTable, cls).__new__(cls, *args, **kwargs)


    def __repr__(self):
        return json.dumps(self.dict(), indent=4, ensure_ascii=False)

    # Needed for Column(JSON)
    class Config:
        arbitrary_types_allowed = True


class IngredientsTestTable(SQLModel, table=True):
    __table_args__ = {'extend_existing': True}
    __tablename__ = "IngredientsTestTable"
    Name: str = Field(primary_key=True)
    Unit: Optional[str] = None
    Type: str


    def __new__(cls, *args, **kwargs):
        if kwargs.get('Type') not in ["Fresh", "Dairy", "Dry", "Tinned"]:
            raise MissingIngredientType('Invalid ingredient type, must be one of: Fresh, Dairy, Dry or Tinned')
        else:
            return super(IngredientsTestTable, cls).__new__(cls, *args, **kwargs)


    def __repr__(self):
        return json.dumps(self.dict(), indent=4, ensure_ascii=False)