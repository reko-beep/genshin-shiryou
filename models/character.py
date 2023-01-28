from pydantic import validator, BaseModel, Field
from constants import ATTRIBUTETEXT


class CharaterInfo(BaseModel):
    
    title: str
    description: Field(alias='detail')
    constellation : str
    cv : dict[str, str]

class CharacterDetails(BaseModel):
    
    element : str
    icon: str
    id : int
    weapontype: str
    birthday: list[int]
    release: int
    route : str
    info: CharaterInfo = Field(alias='fetter')
    

class Attribute(BaseModel):
    name: str = Field(alias='propType')
    value : int = Field(alias='initValue')
    curvetype: str 
    
    @validator('name', pre=True, allow_reuse=True)
    def parse_attr_name(cls, v):
        
        return ATTRIBUTETEXT.get(v, 'Unknown')


