import math
import tkinter as tk

class game:
    def __init__(self) -> None:
        self.bullets = []
        self.ships = []

    def detect_collisions(self):
        for ship in self.ships:
            for bullet in self.bullets:
                if int(ship.xcoord) == int(bullet.xcoord) and int(ship.ycoord) == int(bullet.ycoord):
                    ship.isAlive = False
                    bullet.isAlive = False
                    self.ships.pop(ship)
                    self.bullets.pop(bullet)
                    break    

    def shoot(self):
        self.bullets.append(bullet(self.ships[0].theta, self.ships[0].x, self.ships[0].y))        

class ship:
    def __init__(self, theta, xcoord, ycoord) -> None:
        self.theta = theta
        while self.theta >= 360:
            self.theta -= 360

        self.x = xcoord
        self.y = ycoord
        self.isAlive = True

        #define rate of change of angle as omega
        self.omega = 1

        self.update_bearing()


    def turn_left(self):
        self.theta += self.omega

    def turn_right(self):
        self.theta -= self.omega

    def update_bearing(self):
        self.bear1 = [self.x, self.y + 1]
        self.bear2 = [self.x + 2^(-2), self.y - 2^(-2)]
        self.bear3 = [self.x - 2^(-2), self.y - 2^(-2)]

    def move(self, speed):
        self.x += speed * math.cos(self.theta)
        self.x += speed * math.sin(self.theta)

#Bullet Class that inherits from ship class
class bullet(ship):
    def __init__(self):
        while self.isAlive:
            self.move(2)

#Code for GUI
def main():
    testGame = game()
    testGame.ships.append(ship(theta=0, xcoord=0, ycoord=0))

    root = tk.Tk()
    root.title('Test')
    
    root.bind("<Down>", game.ships[0].turn_left)
    root.bind('<Up>', game.ships[0].turn_right)
    root.bind('<Enter>', game.shoot())
    root.mainloop()

main()

#Commit notes:
#Implemented basic GUI setup
#moved shoot method to game class
#need to fix error: type object 'game' has no attribute 'ships