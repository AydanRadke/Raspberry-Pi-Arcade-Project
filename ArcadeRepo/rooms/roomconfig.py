# This will be a dictionary that imports all of our rooms, so we can just import a dictionary when we need
# to access the rooms, but also have the modularity of giving each room its own file
import normal.aydannormal2
import normal.adamnormal1
import hub.aydanhub1
import spawn.aydanspawn1
import treasure
import shop

config = {
    'hub': {
        'aydanhub1':hub.aydanhub1.aydanhub1_setup,
    },
    'normal':{
        "aydannormal2": normal.aydannormal2.aydannormal2_setup,
        "adamnormal1": normal.adamnormal1.adamnormal1_setup
    },
    'spawn': {
        'aydanspawn1': spawn.aydanspawn1.aydanspawn1_setup
    },
    'shop': shop.shop_setup,
    'treasure': treasure.treasure_setup
}

x = 1