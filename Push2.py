import math
class game:
    def __init__(self, bullets, ships) -> None:
        self.bullets = bullets
        self.ships = ships

class direction:
    def __init__(self, theta) -> None:

        '''#initiailizing direction vector
        self.x = x
        self.y = y

        #normalizing vector
        mag = (self.x^2 + self.y^2)^(0.5)
        self.x /= mag
        self.y /= mag
        assert (self.x^2 + self.y^2)^(0.5) == 1

        #calculating theta 
        if self.x > 0:
            self.theta = math.atan(y/x)
        elif 0 > x:
            self.theta = math.atan(y/x) - math.pi
        else:
            if y > 0:
                self.theta = math.pi/2
            else:
                self.theta = -math.pi/2
        '''

class ship(game):
    def __init__(self, theta, xcoord, ycoord) -> None:
        self.theta = theta
        while self.theta >= 360:
            self.theta -= 360

        self.pos = [xcoord, ycoord]

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

    def shoot():
        pass

    def detect_collision():
        pass

class bullet(ship):
    def __init__(self):
        self.isAlive = True
        while self.isAlive:
            self.move()

#commit notes:
#removed the direction vector replacing it with theta
#implemented the turn_right and turn_left methods
#bullet class now inherits from ship class
