import random
import math
from Bullet_Class import Bullet
from Ship_Class import Ship
from Asteroid_Class import Asteroid

class Game:
    def __init__(self):
        self.ships = []
        self.bullets = []
        self.asteroids = []
        self.is_paused = False
        self.event = None

    #initializes a 1v1 game
    def game1(self):
        game1 = Game()
        player_id = canvas.create_polygon((0,0,0,0,0,0,0,0), fill= 'white')
        game1.ships.append([Ship(math.pi, screen_width - 100, screen_height/2), player_id])

        opponent_id = canvas.create_polygon((0,0), fill= 'white')
        game1.ships.append([Ship(0, 100, screen_height/2), opponent_id])
        return game1
    
    def game2(self):
        '''Initializes and returns a 1 player game'''
        game2 = Game()
        player_id = canvas.create_polygon((0,0), fill= 'white')
        game2.ships.append([Ship(-math.pi/2, screen_width/2, screen_height/2), player_id])
        return game2

    def restart(self):
        
        self.ships = []
        self.bullets = []
        self.asteroids = []
        self.is_paused = False

        #deletes everything except score menu
        canvas.delete_all()

        player_id = canvas.create_polygon((0,0), fill= 'white')
        self.ships.append([Ship(-math.pi/2, screen_width/2, screen_height/2), player_id])

    def update(self):
        self.detect_collision()
        self.keep_in_bounds()
        self.generate_asteroid()

        #randomly controls all helper ships
        for ship in self.ships:
            if ship[0].is_helper:
                action = random.randint(1,100)
                if action %2 == 0:
                    ship[0].move(None)
                    bullet_id = canvas.create_oval(ship[0].x - 3, ship[0].y - 3,
                                                    ship[0].x + 3, ship[0].y + 3, fill='red')
                    self.bullets.append([ship[0].shoot(None),  bullet_id])
                    if action % 3 == 0:
                        ship[0].turn_left(None)
                elif action%3:
                    ship[0].turn_right(None)


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
            ship[0].x = min(ship[0].x, screen_width - 10)
            ship[0].y = min(ship[0].y, screen_height - 10)
            ship[0].x = max(ship[0].x, 10)
            ship[0].y = max(ship[0].y, 10)

        #code that removes bullets and asteroids for optimization
        for bullet in self.bullets:
            if abs(bullet[0].x) > screen_width + 100 or abs(bullet[0].y) > screen_height + 100:
                self.bullets.remove(bullet)
        for asteroid in self.asteroids:
            if abs(asteroid[0].x) > screen_width + 100 or abs(asteroid[0].y) > screen_height+100:
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
                        if ship[0].is_invincible:
                            continue
                        canvas.delete(ast[1])
                        canvas.delete(ship[1])
                        self.ships.remove(ship)
                        self.asteroids.remove(ast)
                        continue

                    #bullet on asteroid collision
                    distance = ((c1[0]-c3[0])**2 + (c1[1] - c3[1])**2)**(0.5) < ast[0].size*20
                    if distance and b in self.bullets:

                        #creates two smaller asteroids
                        if ast[0].size != 1:
                            difficulty = 0.009 + 0.0003*self.score
                            #create first asteroid
                            temp1 = Asteroid(ast[0].size - 1, speed = 1 + 40*difficulty)
                            temp1.theta = -(math.radians(ast[0].theta) + math.pi/2) + math.pi
                            temp1.x = ast[0].x
                            temp1.y = ast[0].y
                            self.asteroids.append([temp1, temp1.draw_asteroid(-1)])

                            #create second asteroid with different angle
                            temp2 = Asteroid(ast[0].size - 1, speed = 1 + 40*difficulty)
                            temp2.theta = -(math.radians(ast[0].theta) + math.pi/2) + 1
                            temp2.x = ast[0].x
                            temp2.y = ast[0].y
                            #temp2.theta = math.radians(ast[0].theta) + 1
                            self.asteroids.append([temp2, temp2.draw_asteroid(-1)])

                        canvas.delete(ast[1])
                        canvas.delete(b[1])
                        self.bullets.remove(b)
                        self.asteroids.remove(ast)
                        
    def generate_asteroid(self):
        #set difficulty based on score
        difficulty = 0.009 + 0.0003*self.score
        if random.randint(0,1000) <= 1000*difficulty:
            temp = Asteroid(random.randint(1,3), speed = 1 + 40*difficulty)
            self.asteroids.append([temp, temp.draw_asteroid(-1)])