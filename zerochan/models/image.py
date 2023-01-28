from requests import get
from PIL import Image
from io import BytesIO

class  ZCImage:
    
    def __init__(self, char: str , url: str) -> None:
        
        self.url = url
        self.char = char
        self.image : Image = None
    
    @property
    def pillowobj(self) -> Image:
        
        if self.image is None:
            with get(self.url, headers={
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'cookie': 'z_theme=11; guest_id=4160438; PHPSESSID=cisf8b989m4h3l52i20lgifkbo'
        }) as f:
                self.image = Image.open(BytesIO(f.content), 'r').convert('RGBA')
                
        
        return self.image
    
    def save(self, path: str):
        
        self.pillowobj.save(path)
            

    def __repr__(self) -> str:
        return f'<Image name={self.char} url={self.url}>'