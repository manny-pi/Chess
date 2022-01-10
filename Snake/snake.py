from pygame.sprite import Sprite, Group 
from pygame.sprite import spritecollideany 
from pygame.surface import Surface 
from enum import Enum

from random import randint as rint 

class Direction(Enum):  
    UP    = 1
    DOWN  = 2
    LEFT  = 3 
    RIGHT = 4


class BodySegment(Sprite): 
    DELTA = 25 
    
    def __init__(self, initPos=[0, 0]): 
        super().__init__() 
        
        self.currPos = initPos             # Current position of this body segment 
        self.prevPos = None                # Previous position of this body segment 
        
        self.x = self.currPos[0]           # Set the x-cor of the segment 
        self.y = self.currPos[1]           # Set the y-cor of the segment 

        self.next = None                   # Segment after this body segment 

        self.surface = Surface((25, 25))   # Create a surface 
        self.surface.fill((rint(0, 255), rint(0, 255), rint(0, 255)))

    def goUp(self): 
        """ Update the 'prevPos' and 'currPos' attributes """ 

        self.prevPos = [self.x, self.y]

        self.currPos[1] -= BodySegment.DELTA
        self.y = self.currPos[1]        

    def goDown(self): 
        """ Update the 'prevPos' and 'currPos' attributes """ 

        self.prevPos = [self.x, self.y]
        
        self.currPos[1] += BodySegment.DELTA
        self.y = self.currPos[1]    

    def goLeft(self): 
        """ Update the 'prevPos' and 'currPos' attributes """ 
        
        self.prevPos = [self.x, self.y]

        self.currPos[0] -= BodySegment.DELTA 
        self.x = self.currPos[0] 

    def goRight(self): 
        """ Update the 'prevPos' and 'currPos' attributes """ 

        self.prevPos = [self.x, self.y]

        self.currPos[0] += BodySegment.DELTA 
        self.x = self.currPos[0]

    def getX(self): 
        return self.currPos[0]

    def getY(self): 
        return self.currPos[1] 

    def __repr__(self): 
        return f'BodySegment(currPos={self.currPos}, prevPos={self.prevPos})'

    @classmethod 
    def setDelta(cls, delta): 
        cls.DELTA = delta


class Snake(): 
    NEXT_TAIL_POSITION = [] 

    TOP_BORDER    = 0 
    BOTTOM_BORDER = 0
    LEFT_BORDER   = 0 
    RIGHT_BORDER  = 0

    def __init__(self, initPos=[0, 0]): 
        self.head = BodySegment(initPos)
        self.head.surface.fill((255, 0, 0))

        self.tail = None

        self.iter_seg = self.head        # Used to iterate over Snake's body
        self.direction = Direction.DOWN  # Used to determine the direction Snake can move in 

        self.segments = Group() 

    def goUp(self): 
        if self.canGoUp(): 
            self.direction = Direction.UP 

    def goDown(self): 
        if self.canGoDown(): 
            self.direction = Direction.DOWN 
                            
    def goLeft(self): 
        if self.canGoLeft(): 
            self.direction = Direction.LEFT 

    def goRight(self): 
        if self.canGoRight(): 
            self.direction = Direction.RIGHT 

    def canGoUp(self):
        """ Returns True if Snake can move in the upwards direction """

        return self.direction is not Direction.DOWN

    def canGoDown(self): 
        """ Returns True if Snake can move in the downward direction """

        return self.direction is not Direction.UP 

    def canGoLeft(self): 
        """ Returns True if Snake can move in the leftward direction """

        return self.direction is not Direction.RIGHT 

    def canGoRight(self): 
        """ Returns True if Snake can move in the rightward direction """

        return self.direction is not Direction.LEFT 

    def addSegment(self): 
        """ Stores the position where the new tail will be generated """

        if self.tail is None: 
            Snake.NEXT_TAIL_POSITION.append(list(self.head.currPos))

        else: 
            Snake.NEXT_TAIL_POSITION.append(list(self.tail.currPos))

    def updateSnake(self): 
        """ Updates the positions of the body segments, and adds the tail (if applicable) """

        if self.direction == Direction.UP: 
            
            self.head.goUp() 
            
            # Execute if Snake went out of bounds / TOP_BORDER
            if self.head.y == Snake.TOP_BORDER - BodySegment.DELTA: 
                self.head.currPos = [self.head.x, Snake.BOTTOM_BORDER - BodySegment.DELTA]

                self.head.x = self.head.currPos[0]
                self.head.y = self.head.currPos[1]

        elif self.direction == Direction.DOWN: 

            self.head.goDown() 
            
            # Execute if Snake went out of bounds / BOTTOM_BORDER 
            if self.head.y == Snake.BOTTOM_BORDER: 
                self.head.currPos = [self.head.x, Snake.TOP_BORDER - BodySegment.DELTA]

                self.head.x = self.head.currPos[0]
                self.head.y = self.head.currPos[1]

        elif self.direction == Direction.LEFT: 

            self.head.goLeft() 
            
            # Execute if Snake went out of bounds / LEFT_BORDER 
            if self.head.x == Snake.LEFT_BORDER - BodySegment.DELTA:
                self.head.currPos = [Snake.RIGHT_BORDER - BodySegment.DELTA, self.head.y]
                
                self.head.x = self.head.currPos[0]
                self.head.y = self.head.currPos[1]

        elif self.direction == Direction.RIGHT: 

            self.head.goRight()  
            
            # Execute if Snake went out of bounds / RIGHT_BORDER 
            if self.head.x == Snake.RIGHT_BORDER:
                self.head.currPos = [Snake.LEFT_BORDER, self.head.y]
                
                self.head.x = self.head.currPos[0]
                self.head.y = self.head.currPos[1]
                

        self.updateSegments() 

        # Execute if we need to add a Segment to Snake
        if len(Snake.NEXT_TAIL_POSITION) > 0: 
            if self.tail is None:
                self.tail = BodySegment(initPos=Snake.NEXT_TAIL_POSITION.pop(0)) 
                self.head.next = self.tail 
    
            else: 
                if self.tail.prevPos == Snake.NEXT_TAIL_POSITION[0]: 
                    newTail = BodySegment(initPos=Snake.NEXT_TAIL_POSITION.pop(0))
                    self.tail.next = newTail 
                    self.tail = newTail

            self.segments.add(self.tail)

    def updateSegments(self): 
        """ Traverse the Snake's body and update the 'prevPos' and 'currPos' attributes """ 

        segment = self.head         
        while segment.next is not None: 
            segment.next.prevPos = segment.next.currPos
            segment.next.currPos = segment.prevPos 

            segment.next.x = segment.next.currPos[0]
            segment.next.y = segment.next.currPos[1]
            
            segment = segment.next 

    def bitHerself(self): 
        return spritecollideany(self.head, self.segments, collided=Snake.collisionMethod)

    def __repr__(self): 
        retval = 'Snake(\n'
        for seg in self: 
            if seg is self.head: 
                retval += f'\thead={seg}\n'
            elif seg is self.tail: 
                retval += f'\ttail={seg}\n'
            else: 
                retval += f'\tsegm={seg}\n'

        retval += ')'
        return retval

    def __iter__(self): 
        return self 

    def __next__(self): 
        if self.iter_seg is None: 
            self.iter_seg = self.head 
            raise StopIteration 

        else:
            retval = self.iter_seg 
            self.iter_seg = self.iter_seg.next 

            return retval 

    @staticmethod
    def collisionMethod(segment1, segment2):
        """ Returns True if two segments of Snake's body are in the same place """

        if segment1.getX() == segment2.getX() and segment1.getY() == segment2.getY(): 
            return True 

        return False  

    @classmethod 
    def setBoundaries(cls, *args): 
        cls.LEFT_BORDER   = args[0] 
        cls.RIGHT_BORDER  = args[1]
        cls.TOP_BORDER    = args[2]
        cls.BOTTOM_BORDER = args[3]
        
