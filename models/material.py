from pydantic import BaseModel, validator


class Source(BaseModel):
    name: str
    type : str
    
class Material(BaseModel):
    name : str
    description : str
    recipe : bool 
    mapmark : bool
    source : list[Source]
    icon: str
    route: str
    rank : int
    
    @validator("source", pre=True, allow_reuse=True)
    def parse_sources(cls, v):
        
        result = []
        if len(v) != 0:
            for s in v:
                result.append(Source(**s))
        
        return result       
    
    @validator("icon", pre=True, allow_reuse=True)
    def get_icon_url(cls, v):
        
        if v != '':
            return f"https://api.ambr.top/assets/UI/{v}"
           
    @validator("rank", pre=True)
    def parse_rank(cls, v):
        
        return v if v else 0

