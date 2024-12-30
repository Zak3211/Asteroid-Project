import math
from Bullet_Class import Bullet
from ShipNet import ShipNet
class Ship:
    def __init__(self, theta, xcoord, ycoord, master,  canvas = None) -> None:
        self.master  = master

        self.theta = theta
        self.theta %= 2 * math.pi
        self.omega = 0.4

        self.x = xcoord
        self.y = ycoord
        self.is_alive = True
        self.canvas = canvas

        self.score = 0
        self.brain = ShipNet()

    def turn_left(self, event = None) -> None:
        self.theta -= self.omega

    def turn_right(self, event = None) -> None:
        self.theta += self.omega

    def move(self, event = None) -> None:
        speed = 5
        self.x += speed * math.cos(self.theta)
        self.y += speed * math.sin(self.theta)

    def shoot(self,  event = None):
        if self.canvas:
            bullet_id = self.canvas.create_oval(self.x - 3, self.y - 3,
                                    self.x + 3, self.y + 3, fill='red')
        else:
            bullet_id = -1
        self.master.bullets.append([Bullet(self.theta, self.x + 50*math.cos(self.theta),
                       self.y + 50*math.sin(self.theta), canvas = self.canvas), bullet_id])

    def action(self, inputs):
        res = self.brain.action(inputs)

        if res == 0:
            self.turn_left()
        elif res == 1:
            self.turn_right()
        elif res == 2:
            self.shoot()
        elif res == 3:
            self.move()

    def draw_ship(self, player_id):
        if not self.canvas:
            return
        
        s = 0.75
        theta = self.theta
        x = self.x
        y = self.y

        new_coords = [x + s*50*math.cos(theta), y + s*50*math.sin(theta),
                    x + s*25*math.cos(theta + 90), y + s*25*math.sin(theta + 90),
                    x + s*15*math.cos(theta), y + s*15*math.sin(theta),
                    x + s*25*math.cos(theta - 90), y + s*25*math.sin(theta - 90)]
        self.canvas.coords(player_id, new_coords)