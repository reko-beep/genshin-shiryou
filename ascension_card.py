
def create_card_dict(rarity: int, img: str,  text: str, title: str):
    cards_bg = {
        'card_3': 'https://static.wikia.nocookie.net/gensin-impact/images/5/57/Rarity_3_background.png',
        'card_4': 'https://static.wikia.nocookie.net/gensin-impact/images/c/c9/Rarity_4_background.png',
        'card_5': 'https://static.wikia.nocookie.net/gensin-impact/images/e/ea/Rarity_5_background.png',
        'card_2': 'https://static.wikia.nocookie.net/gensin-impact/images/d/d4/Rarity_2_background.png',
        'card_1': 'https://static.wikia.nocookie.net/gensin-impact/images/6/69/Rarity_1_background.png',
        'card_0': 'https://static.wikia.nocookie.net/gensin-impact/images/6/69/Rarity_1_background.png'
    }
    
    return {
    "title": title,
    "img": img,
    "txt": text,
    "card_bg": cards_bg[f'card_{rarity}']
    }



ascension_template = {
    'talent_level_up_materials': 
        [
        {
            'rarity' : 2, 
            'amount' : 9,
        },
        
        {
            'rarity' : 3, 
            'amount' : 63,
        },
        {
            'rarity' : 4, 
            'amount' : 114,
        }
        ]
    ,
    'common_enemy_drops': [
        
        {
            'rarity' : 1, 
            'amount' : 36,
        },
        
        {
            'rarity' : 2, 
            'amount' : 96,
        },
        {
            'rarity' : 3, 
            'amount' : 129,
        }
        
    ]
    ,
    'weekly_boss_materials': [
        {
            'rarity': 5,
            'amount': 18
        }
    ],
    'common_boss_materials': [
        {
            'rarity': 4,
            'amount': 46
        }
    ],
    'ascension_gems': [
        {
            'rarity': 2,
            'amount': 1
        },
        {
            'rarity':3,
            'amount': 9
        },
        {
            'rarity':4,
            'amount': 9
        },
        {
            'rarity':5,
            'amount': 6
        }],
    'local_specialities': [
        {
            'rarity' : 0,
            'amount': 168
        }
    ],
    'common' : [
        {
            'rarity': 3,
            'name': 'mora',
            'amount': 7050*1000,
            'img': 'https://static.wikia.nocookie.net/gensin-impact/images/8/84/Item_Mora.png'
        },
        {
            'rarity': 4,
            'name' : 'heros wit',
            'amount': 419,
            'img': 'https://static.wikia.nocookie.net/gensin-impact/images/2/26/Item_Hero%27s_Wit.png'
        },
        {
            'rarity': 5,
            'name': 'crown of insight',
            'amount': 3,
            'img': 'https://static.wikia.nocookie.net/gensin-impact/images/0/04/Item_Crown_of_Insight.png'
            }
    ]
        
        
}

