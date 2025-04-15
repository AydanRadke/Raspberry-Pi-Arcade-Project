# This will be a dictionary that imports all of our rooms, so we can just import a dictionary when we need
# to access the rooms, but also have the modularity of giving each room its own file
from .normal import aydannormal2, aydannormal1
from .hub import aydanhub1
from .spawn import aydanspawn1
from .treasure import treasure_setup
from .shop import shop_setup
from .boss import boss_setup

config = {
    'hub': {
        'aydanhub1':aydanhub1.aydanhub1_setup,
    },
    'normal':{
        "aydannormal2": aydannormal2.aydannormal2_setup,
        "aydannormal1": aydannormal1.aydannormal1_setup
    },
    'spawn': {
        'aydanspawn1': aydanspawn1.aydanspawn1_setup
    },
    'shop': shop_setup,
    'treasure': treasure_setup,
    'boss': boss_setup
}
