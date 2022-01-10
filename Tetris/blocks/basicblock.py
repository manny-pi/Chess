from pygame import sprite, Surface

class BasicBlock(sprite.Sprite): 
    
    # Block Dimensions
    BLOCK_WIDTH = BLOCK_HEIGHT = 50

    def __init__(self, color, x, y, speed): 
        super().__init__()  

        self.color = color.value 
        self.x = x 
        self.y = y 

        self.surface = Surface((50, 50))
        self.rect = self.surface.get_rect(topleft=(x, y))

        self.speed = speed 

        self.surface = Surface((BasicBlock.BLOCK_WIDTH, BasicBlock.BLOCK_HEIGHT))
        self.surface.fill(self.color)
    
    def bottom(self): 
        return self.y + 50
    
    def top(self): 
        return self.y

    def update_pos(self, pressed_keys): 
        pass 

    def __repr__(self): 
        return f"BasicBlock({self.x}, {self.y}, {self.color})"
