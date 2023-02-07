from pydantic import validator, BaseModel, Field
from constants import ATTRIBUTETEXT
from models.base import MaterialPartial

class CharacterInfo(BaseModel):
    
    title: str
    description: Field(alias='detail')
    constellation : str
    cv : dict[str, str]

class Attribute(BaseModel):
    name: str = Field(alias='propType')
    value : int = Field(alias='initValue')
    curvetype: str 
    
    @validator('name', pre=True, allow_reuse=True)
    def parse_attr_name(cls, v):
        
        return ATTRIBUTETEXT.get(v, 'Unknown')


class CharacterAscensionLevel(BaseModel):
    max_level : int = Field(alias='unlockMaxLevel')
    ascension_level : int = Field(alias='promoteLevel')
    items : list[MaterialPartial] = Field(alias='costItems')
    attrs: list[Attribute] = Field(alias='addProps')
    required_rank : int = Field(alias='requiredPlayerLevel')
    mora : int = Field(alias='coinCost')
    
    @validator('items', pre=True, allow_reuse=True)
    def parse_items(cls, v):
        result = []
        for d in v:
            result.append({'amount': v[d], 'id' : int(d)})
        return [MaterialPartial(**i) for i in result]
    
    @validator('attrs', pre=True, allow_reuse=True)
    def parse_attributes(cls, v):
        
        result = []
        for d in v:
            result.append(Attribute({'propType': d, 'initValue': v[d]}))
        return result
        
        
    
    

class CharacterAscension(BaseModel):
    
    attributes : list[Attribute] = Field(alias='prop')
    ascension_levels : list[CharacterAscensionLevel] = Field(alias='promote')
    
    @validator('ascension_levels', pre=True, allow_reuse=True)
    def parse_ascension_levels(cls, v):
        
        result = []
        for d in v:
            result.append(CharacterAscensionLevel(**d))
        return result

class Namecard(BaseModel):
    id: int
    name : str
    description : str
    icon : str
    
    @validator('icon', pre=True, allow_reuse=True)
    def parse_icon_url(cls, v):
        return f"https://api.ambr.top/assets/UI/{v}"

class SpecialFood(BaseModel):
    id : int
    name : str
    rank : int
    effecticon : str
    icon : str
    
    @validator('effecticon', pre=True, allow_reuse=True)
    def parse_effect_icon(cls, v):
        return f"https://api.ambr.top/assets/UI/{v}"
    
    @validator('icon', pre=True, allow_reuse=True)
    def get_icon_url(cls, v):
        return f"https://api.ambr.top/assets/UI/{v}"
class OtherInfo(BaseModel):
    
    namecard: Namecard 
    specialfood : SpecialFood
    

class CharacterTalentLevel(BaseModel):
    level : int
    mora : int = Field(alias='coinCost')
    materials : list[MaterialPartial] = Field(alias='costItems')
    description : list[str] 
    params : list[int | float]
    
    @validator('materials', pre=True, allow_reuse=True)
    def parse_materials(cls, v):
        result = []
        if v is not None:         
            for i in v:
                result.append(MaterialPartial({'id': int(i), 'amount': v[i]}))
        return result
                
class CharacterTalent(BaseModel):
    
    type: int
    name : str
    description : str
    icon : str
    upgrade : CharacterTalentLevel = Field(alias='promote')
    
    @validator('upgrade', pre=True, allow_reuse=True)
    def parse_upgrade(cls, v):
        result = []
        for l in v:
            result.append(CharacterTalentLevel(**v[l]))
        return result
    
    @validator('icon', pre=True, allow_reuse=True)
    def get_icon_url(cls, v):
        return f"https://api.ambr.top/assets/UI/{v}"
class CharacterConstellation(BaseModel):
    
    name: str
    description : str
    icon : str
    
    @validator('icon', pre=True, allow_reuse=True)
    def get_icon_url(cls, v):
        return 

class CharacterDetails(BaseModel):
    
    element : str
    icon: str
    id : int
    weapontype: str
    birthday: list[int]
    release: int
    route : str
    info: CharacterInfo = Field(alias='fetter')
    ascension : CharacterAscension = Field(alias='upgrade')
    talent : CharacterTalent
    constellation : CharacterConstellation
    
    @validator('icon', pre=True, allow_reuse=True)
    def get_icon_url(cls, v):
        return f"https://api.ambr.top/assets/UI/{v}"
    
    @validator('ascension', pre=True, allow_reuse=True)
    def parse_ascension(cls, v):
        if len(v) != 0:
            return CharacterAscension(**v)
    
        return None
        
    @validator('talent', pre=True, allow_reuse=True)
    def parse_talent(cls, v):
        result = []
        if len(v) != 0:
            for l in v:
                result.append(CharacterTalent(**v[l]))               
            
    
        return result