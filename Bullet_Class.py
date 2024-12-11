class Bullet:
    def __init__(self, theta, x, y) -> None:
        self.theta = theta
        self.x = x
        self.y = y
        self.is_alive = True

    def draw_bullet(self, bullet_id):
        r = 3
        new_coords = [self.x - r, self.y - r, self.x + r, self.y + r]
        canvas.coords(bullet_id, new_coords)
    def move(self):
        s = 10
        self.x += s * math.cos(self.theta)
        self.y += s * math.sin(self.theta)