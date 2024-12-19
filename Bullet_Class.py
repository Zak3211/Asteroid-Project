import math
class Bullet:
    def __init__(self, theta, x, y, canvas = None) -> None:
        self.canvas = canvas
        self.theta = theta
        self.x = x
        self.y = y
        self.is_alive = True

    def draw_bullet(self, bullet_id):
        if not self.canvas:
            return
        
        r = 3
        new_coords = [self.x - r, self.y - r, self.x + r, self.y + r]
        self.canvas.coords(bullet_id, new_coords)
        
    def move(self):
        s = 10
        self.x += s * math.cos(self.theta)
        self.y += s * math.sin(self.theta)