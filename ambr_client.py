from requests import Session

from json import load, dump
from typing import Optional, Union


from constants import BASE_ROUTE, HEADERS, Lang
from aiohttp import ClientSession
from urllib.parse import urljoin


from models import (CharacterPartial, CharacterDetails)


class AMBR:
    
    def __init__(self) -> None:
        
        self.session = ClientSession()
        self.session.headers.update(HEADERS)
      
   
    def create_endpoint(self, type_ : str, lang: Lang,  id : Optional[str | int] = ""):
        """generates a endpoint for ambr.top api

        Args:
            type_ (str): type of item to fetch 
                allowed -> avatar , material, reliquary, monster, weapons, assets
            lang (Lang): Lang value
            id (Optional[str  |  int], optional): id of the item of said type. Defaults to "".

        Returns:
            endpoint url
        """
        
        allowed = {'avatar', 'material', 'reliquary', 'monster', 'weapons', 'assets'}
        
        if set([type_]).intersection(allowed) != 0:
            if id != "":
                return f"{BASE_ROUTE}{lang}/{type_}/{id}?v=34F5"
            else:
                return f"{BASE_ROUTE}{lang}/{type_}?v=34F5"
        else:
            
            raise Exception("Allowed types are (avatar, material, reliquary, monster, weapons, assets)")
        
    async def fetch_data(self, url : str) -> dict:
        """returns data from api endpoint provided

        Args:
            url (str): ambr.top api endpoint

        Returns:
            dict: _description_
        """
        
        async with self.session.get(url) as f:
            if f.status < 400:
                data = await f.json()
                if data['response'] == '200': 
                    return data
        
      
    
    
    async def get_character_details(self, character: CharacterPartial = None) -> Optional[CharacterPartial | CharacterDetails | None]:
        """gets character partial objects if no id is provided else Character object

        Args:
            character_id (str, optional): id of the character. Defaults to ''.

        Returns:
            Optional[CharacterPartial | None]: returns list of character partial objects if no id is provided else Character object
        """
        
        if isinstance(character, CharacterPartial):            
            url = self.create_endpoint('avatar', Lang.EN, character.id)
            data = self.fetch_data(url)
            if data != None:
                return CharacterDetails(**data)
            
        
        else:
            
            url = self.create_endpoint('avatar', Lang.EN)
            data = self.fetch_data(url)
            if data != None:
                return [CharacterPartial(**data['items'][item]) for item in data['items']]
                       

        
        
   