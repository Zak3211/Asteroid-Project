import math
import random

class Asteroid:
    def __init__(self, size, screen_width, screen_height, canvas = None):
        self.speed = 13
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.canvas = canvas

        self.size = size
        self.x = random.randint(0, screen_width)
        self.y = random.randint(0, screen_height)


        #assign randomly to one of the edges
        temp = random.randint(1,4)
        if temp == 1:
            self.x = 0
        elif temp == 2:
            self.x = self.screen_width
        elif temp == 3:
            self.y = 0
        else:
            self.y = self.screen_height

        if self.y > self.screen_height/2:
            self.theta = math.atan((self.screen_height/2 - self.y)/(self.screen_width/2 - self.x + 0.01))
        else:
            self.theta = math.atan((self.screen_width/2 - self.x)/(self.screen_height/2 - self.y + 0.01))
        if self.x >  self.screen_width/2:
            self.theta += math.pi
        self.theta %= 2*math.pi

    def move(self):
        speed = self.speed
        self.x += speed * math.cos(self.theta)
        self.y += speed * math.sin(self.theta)

    def draw_asteroid(self, asteroid_id):
        if not self.canvas:
            return -1
        
        s = 10
        x = self.x
        y = self.y
        if self.size == 1:
            coords = (x-s*2, y+s*1, x-s*4, y-s*1, x, y-s*1, x+s*3, y-s*3, x+s*2, y+s*1)
        elif self.size == 2:
            coords = (x,y+s*4, x-s*3,y, x, y-s*4, x+s*4,y-s*2, x+s*4, y+s*2, x, y + s*2)
        elif self.size == 3:
            coords = (x-s*5, y+s*5,x-s*7, y, x-s*3, y-s*2, x+s*3, y-s*2,
                       x+s*4, y-s*4, x+s*6, y-s*1, x+s*5, y+s*5)
        else:
            coords = (x-s*2, y+s*1, x-s*4, y-s*1, x, y-s*1, x+s*3, y-s*3, x+s*2, y+s*1)

        if asteroid_id == -1:
            return self.canvas.create_polygon(coords, outline='white')
        else:
            self.canvas.coords(asteroid_id, coords)