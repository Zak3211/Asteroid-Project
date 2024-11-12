import math
class game:
    def __init__(self, bullets, ships) -> None:
        self.bullets = bullets
        self.ships = ships

    def detect_collisions(self):
        for ship in self.ships:
            for bullet in self.bullets:
                if ship.xcoord == bullet.xcoord and ship.ycoord == bullet.ycoord:
                    ship.isAlive = False
                    bullet.isAlive = False
                    self.ships.pop(ship)
                    self.bullets.pop(bullet)
                    break
                

class ship:
    def __init__(self, theta, xcoord, ycoord) -> None:
        self.theta = theta
        while self.theta >= 360:
            self.theta -= 360

        self.pos = [xcoord, ycoord]
        self.isAlive = True

        #define rate of change of angle as omega
        self.omega = 1

        #define 3 bearings of distance 1 from the center clockwise starting at pos + direction
        self.bear1 = [self.pos[0], self.pos[1] + 1]
        self.bear2 = [self.pos[0] + 2^(-2), self.pos[1] - 2^(-2)]
        self.bear3 = [self.pos[0] - 2^(-2), self.pos[1] - 2^(-2)]

    def turn_left(self):
        self.theta += self.omega

    def turn_right(self):
        self.theta -= self.omega

    def update_bearing(self):
        self.bear1 = [self.pos[0], self.pos[1] + 1]
        self.bear2 = [self.pos[0] + 2^(-2), self.pos[1] - 2^(-2)]
        self.bear3 = [self.pos[0] - 2^(-2), self.pos[1] - 2^(-2)]

    def move(self):
        self.pos[0] += math.cos(self.theta)
        self.pos[1] += math.sin(self.theta)

    def shoot(self):
        bullet = bullet(self.theta, self.xcoord, self.ycoord)

class bullet(ship):
    def __init__(self):
        while self.isAlive:
            self.move()

#Push notes:
#implemented collision detection in game class
#finalized most game classes