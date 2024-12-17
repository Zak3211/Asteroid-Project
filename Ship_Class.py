import math
from Bullet_Class import Bullet

class Ship:
    def __init__(self, theta, xcoord, ycoord) -> None:
        self.theta = theta
        self.is_invincible = False
        self.is_helper = False
        self.theta %= 2 * math.pi
        self.x = xcoord
        self.y = ycoord
        self.is_alive = True
        self.omega = 0.3

    def turn_left(self, event = None) -> None:
        self.theta -= self.omega

    def turn_right(self, event = None) -> None:
        self.theta += self.omega

    def move(self, event = None) -> None:
        speed = 5
        self.x += speed * math.cos(self.theta)
        self.y += speed * math.sin(self.theta)

    def shoot(self,  event = None):
        return Bullet(self.theta, self.x + 50*math.cos(self.theta),
                       self.y + 50*math.sin(self.theta))

    def draw_ship(self, player_id):
        s = 0.75
        theta = self.theta
        x = self.x
        y = self.y

        new_coords = [x + s*50*math.cos(theta), y + s*50*math.sin(theta),
                    x + s*25*math.cos(theta + 90), y + s*25*math.sin(theta + 90),
                    x + s*15*math.cos(theta), y + s*15*math.sin(theta),
                    x + s*25*math.cos(theta - 90), y + s*25*math.sin(theta - 90)]
        canvas.coords(player_id, new_coords)