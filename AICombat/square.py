import definitions

class Square():

    def __init__(self, terrain = definitions.terrain.EMPTY):
        self.terrain = terrain
        self.items = []
        self.bots = []
        
