import random
import math
from Bullet_Class import Bullet
from Ship_Class import Ship
from Asteroid_Class import Asteroid

class Game:
    def __init__(self, screen_width, screen_height, canvas = None):
        self.canvas = canvas
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.kill_on_edge = True

        self.ships = []
        self.bullets = []
        self.asteroids = []

        self.game_over = False
        self.event = None


    #Initializes a Player vs Player Game
    def game1(self):
        game1 = Game()
        player_id = self.canvas.create_polygon((0,0,0,0,0,0,0,0), fill= 'white')
        game1.ships.append([Ship(math.pi, self.screen_width - 100, self.screen_height/2), player_id])

        opponent_id = self.canvas.create_polygon((0,0), fill= 'white')
        game1.ships.append([Ship(0, 100, self.screen_height/2), opponent_id])
        return game1
    
    #Initializes a Player vs Asteroid Game
    def game2(self):
        game2 = Game()
        player_id = self.canvas.create_polygon((0,0), fill= 'white')
        game2.ships.append([Ship(-math.pi/2, self.screen_width/2, self.screen_height/2), player_id])
        return game2

    def restart(self):
        self.ships = []
        self.bullets = []
        self.asteroids = []
        self.is_paused = False
        self.canvas.delete_all()

        player_id = self.canvas.create_polygon((0,0), fill= 'white')
        self.ships.append([Ship(-math.pi/2, self.screen_width/2, self.screen_height/2), player_id])

    def update(self):
        self.detect_collision()
        self.keep_in_bounds()
        self.generate_asteroid()

        for asteroid in self.asteroids:
            asteroid[0].move()
            asteroid[0].draw_asteroid(asteroid[1])
        for bullet in self.bullets:
            bullet[0].move()
            bullet[0].draw_bullet(bullet[1])
        for ship in self.ships:
            ship[0].draw_ship(ship[1])
    
    def keep_in_bounds(self):
        #Removes out of bound entities
        for ship in self.ships:
            if self.kill_on_edge:
                if ship[0].x == self.screen_width - 10:
                    self.game_over = True
                if ship[0].y == self.screen_height - 10:
                    self.game_over = True
                if ship[0].x == 10:
                    self.game_over = True
                if ship[0].y ==  10:
                    self.game_over = True    
            else:            
                ship[0].x = min(ship[0].x, self.screen_width - 10)
                ship[0].y = min(ship[0].y, self.screen_height - 10)
                ship[0].x = max(ship[0].x, 10)
                ship[0].y = max(ship[0].y, 10)

        #code that removes bullets and asteroids for optimization
        for bullet in self.bullets:
            if abs(bullet[0].x) > self.screen_width + 100 or abs(bullet[0].y) > self.screen_height + 100:
                self.bullets.remove(bullet)
        for asteroid in self.asteroids:
            if abs(asteroid[0].x) > self.screen_width + 100 or abs(asteroid[0].y) > self.screen_height+100:
                self.asteroids.remove(asteroid)

    def detect_collision(self):
        #create dummy bullet so code runs properly
        if len(self.bullets) == 0:
            self.bullets.append([Bullet(x = -10, y = -10, theta = 3*math.pi/2),2])

        for b in self.bullets :
            c1 = [b[0].x, b[0].y]
            for ship in self.ships:
                c2 = [ship[0].x, ship[0].y]

                #asteroid on ship collision
                for ast in self.asteroids:
                    c3 = [ast[0].x, ast[0].y]
                    if ((c2[0]-c3[0])**2 + (c2[1] - c3[1])**2)**(0.5) < ast[0].size*20:
                        self.game_over = True
                        return 
                    

                    #bullet on asteroid collision
                    distance = ((c1[0]-c3[0])**2 + (c1[1] - c3[1])**2)**(0.5) < ast[0].size*20
                    if distance and b in self.bullets:
                        #creates two smaller asteroids
                        ship[0].score += 1
                        if ast[0].size != 1 and False:
                            #create first asteroid
                            temp1 = Asteroid(self.screen_width, self.screen_height, ast[0].size - 1, canvas = self.canvas)
                            temp1.theta = -(math.radians(ast[0].theta) + math.pi/2) + math.pi
                            temp1.x = ast[0].x
                            temp1.y = ast[0].y
                            self.asteroids.append([temp1, temp1.draw_asteroid(-1)])
    
                            
                            #create second asteroid with different angle
                            temp2 = Asteroid(self.screen_width, self.screen_height, ast[0].size - 1, canvas = self.canvas)
                            temp2.theta = -(math.radians(ast[0].theta) + math.pi/2) + 1
                            temp2.x = ast[0].x
                            temp2.y = ast[0].y

                            self.asteroids.append([temp2, temp2.draw_asteroid(-1)])
                        
                        if self.canvas:
                            self.canvas.delete(ast[1])
                            self.canvas.delete(b[1])
                        self.bullets.remove(b)
                        self.asteroids.remove(ast)
                        
    def generate_asteroid(self):
        if random.randint(0,1000) <= 65:
            temp = Asteroid(random.randint(1,3), self.screen_width, self.screen_height, canvas = self.canvas)
            self.asteroids.append([temp, temp.draw_asteroid(-1)])