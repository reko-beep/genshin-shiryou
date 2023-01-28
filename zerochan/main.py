from json import load, dump, loads
from bs4 import BeautifulSoup
from requests import Session

from zerochan.models.game import Game


class Zerochan:
    
    def __init__(self):
        
        
        self.url = "https://www.zerochan.net/{path}"       
        self.session = Session()
        self.session.headers.update({
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'cookie': 'z_theme=11; guest_id=4160438; PHPSESSID=cisf8b989m4h3l52i20lgifkbo'
        })
    
    def __url(self, path):
        
        return self.url.format(path=path.replace(' ','+',99))
    
    def get_characters(self) -> Game:
        src = self.session.get(self.__url('Genshin Impact')).content
        
        bs = BeautifulSoup(src, 'lxml')        
        body = bs.find('div', {'id': 'body'})
        scripts = body.find_all('script', {'type': 'application/ld+json'})
        
        for script in scripts:
            
            data = loads(script.text)
            if data.get('@type', None) == 'Game':
                
                return Game(data)
        
        