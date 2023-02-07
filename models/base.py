from pydantic import BaseModel, validator, Field
from constants import HEADERS


class CharacterPartial(BaseModel):
    
    id : int
    name : str
    route : str
    rank : int
    release: int = Field(default=0)
    element: str
    birthday : list[int]
    url : str = Field(default='')
    class Config:
        validate_assignment = True
    
    @validator('id', pre=True, allow_reuse=True)
    def id_check(cls, v):
        
        if not str(v).isdigit():
            
            return int(v.split('-')[0])
        
        else:
            
            return v
    
    @validator('birthday', pre=True, allow_reuse=True)
    def birthday_check(cls, v):        

        return v or [0,0]
      
    @validator('release', pre=True, allow_reuse=True)
    def release_check(cls, v):        
        if v:
            return v 
        else:
            return 0
      
    @validator('url', pre=True, allow_reuse=True)
    def create_url(cls, v):        
        if isinstance(cls.id, int):
            return f"https://api.ambr.top/v2/en/{cls.id}?v=34F5"
        
class MaterialPartial(BaseModel):
    
    id : int
    name : str
    route : str
    rank : int
    mapmark: bool
    icon: str
    type : str
    recipe : bool
    amount : int = 0
    
    class Config:
        validate_assignment = True
        
    @validator("icon", pre=True, allow_reuse=True)
    def get_icon_url(cls, v):
        return f"https://api.ambr.top/assets/UI/{v}"
    
    @validator("amount", pre=True, allow_reuse=True)
    def parse_amount(cls, v):
        
        if v != None:
            return v
        return 0
            
    
class WeaponPartial(BaseModel):
    
    id : int
    name : str
    type : str
    rank : int
    icon: str
    route: str
    
    class Config:
        validate_assignment = True
        
    @validator("icon", pre=True, allow_reuse=True)
    def get_icon_url(cls, v):
        return f"https://api.ambr.top/assets/UI/{v}"

class ReliquaryPartial(BaseModel):
    
    id : int
    name : str
    levellist : list[int]
    affixlist  : dict
    mapmark: bool
    icon: str
    route: str
    sortorder : int
    
    class Config:
        validate_assignment = True
        
    @validator("icon", pre=True, allow_reuse=True)
    def get_icon_url(cls, v):
        return f"https://api.ambr.top/assets/UI/{v}"

class FoodPartial(BaseModel):
    
    id : int
    name : str
    type : str
    recipe : bool
    mapmark : bool
    icon : str
    rank : int 
    route : str
    effecticon : str
    
    class Config:
        validate_assignment = True
        
    @validator("icon", pre=True, allow_reuse=True)
    def get_icon_url(cls, v):
        return f"https://api.ambr.top/assets/UI/{v}"

    @validator("effecticon", pre=True, allow_reuse=True)
    def get_effecticon_url(cls, v):
        return f"https://api.ambr.top/assets/UI/{v}"