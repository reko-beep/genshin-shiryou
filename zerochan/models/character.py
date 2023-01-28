from requests import get
from bs4 import BeautifulSoup
from json import loads
from zerochan.models.image import ZCImage

class Character:
    
    def __init__(self, data: dict) -> None:
        
        self.name = ''
        self.pages = 0
        self.images : list[ZCImage] = []
        
        self.raw_data = data
        self.__parse()
    
    
    def __parse(self):
        
        self.raw_data.pop('@context', '')
        self.raw_data.pop('@type', '')
        
        for key in self.raw_data:
            self.__setattr__(key, self.raw_data[key])
        
   
    def get_images(self, number : int = -1):
        if number == -1:
            self.__getpages()
        else:
            self.__getpages(number)

        
    def __getpages(self, number: int = 100):        
        for pg in range(1, number+ 1, 1):
            url = f"https://zerochan.net/{self.name.replace(' ','+', 99)}?p={pg}"
            print(url)
            src = get(url, headers={
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'cookie': 'z_theme=11; guest_id=4160438; PHPSESSID=cisf8b989m4h3l52i20lgifkbo'
        }).content
            bs = BeautifulSoup(src, 'lxml')
            body = bs.find('div', {'id': 'body'})           
         
            if body is not None:
                scripts = body.find_all('script', {'type': 'application/ld+json'})
                print(len(scripts))
                if len(scripts) < 2:
                    
                    self.images = [ZCImage(self.name, f) for f in self.images]                    
                      
                
                for script in scripts:
                    data = loads(script.text)    
                    print(data, data.get('@type', None) )
                    if data.get('@type', None) == 'ItemList':
                        __ = [item['url'] for item in data['itemListElement']]
                        
                        if len(__) == 0:                     
                            break   
                     
                        self.images += [ZCImage(self.name, f) for f in __]
                        print('found', len(__), 'images')
                        
                           
            else:
                break
    
  
    def __repr__(self) -> str:
        return f'<Character name={self.name} images_count={len(self.images)}, pages={self.pages}>'