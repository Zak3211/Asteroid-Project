import game
class direction:
    def __init__(self, x, y) -> None:

        #initiailizing direction vector
        self.x = x
        self.y = y

        #normalizing vector
        mag = (self.x^2 + self.y^2)^(0.5)
        self.x /= mag
        self.y /= mag
        assert (self.x^2 + self.y^2)^(0.5) == 1

class ship(game):
    def __init__(self, direction, xcoord, ycoord) -> None:
        self.direction = direction
        self.pos = [xcoord, ycoord]

        #define 3 bearings of distance 1 from the center clockwise starting at pos + direction
        self.bear1 = [self.pos[0], self.pos[1] + 1]
        self.bear2 = [self.pos[0] + 2^(-2), self.pos[1] - 2^(-2)]
        self.bear3 = [self.pos[0] - 2^(-2), self.pos[1] - 2^(-2)]

    def turn_left():
        pass

    def turn_right():
        pass

    def update_bearing():
        pass

    def move():
        pass

    def shoot():
        pass

    def detect_collision():
        pass

class bullet:
    def __init__(self, direction, pos) -> None:
        self.xcoord = pos[0]
        self.ycoord = pos[1]

        self.direction = direction
        
    def move():
        pass
