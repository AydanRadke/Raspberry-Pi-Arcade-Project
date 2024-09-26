# This is just a proof of concept. The idea is that the rooms will be 2d lists, and each tile
# of the room will have a certain value to decide what gets generated there. Each value could be a list or
# dict to generate another asset on top of a different one? 

aydannormal2_setup = {
    'layout':
    [['wall','wall','floor','wall','wall'],
    ['wall','floor','floor','floor','wall'],
    ['wall','floor','floor','floor','wall'],
    ['wall','floor','floor','floor','wall'],
    ['wall','wall','floor','wall','wall']],
    "special_features":{
        'test_feature':[(1,1)]
    }
}
