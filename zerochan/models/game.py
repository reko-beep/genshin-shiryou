
from zerochan.models.character import Character

class Game:
    
    def __init__(self, data: dict) -> None:
        
        self.name = ''
        self.thumbnailUrl = ''
        self.character : list[Character] = []
        self.image = ''
        
        self.raw_data = data
        self.__parse()
    
    
    def __parse(self):
        
        self.raw_data.pop('@context', '')
        self.raw_data.pop('@type', '')
        
        for key in self.raw_data:
            self.__setattr__(key, self.raw_data[key])

        
        for c,char in enumerate(self.character):
            self.character[c] = Character(char)
            