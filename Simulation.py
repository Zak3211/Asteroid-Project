from Game_Class import Game
from Ship_Class import Ship
import math
import tkinter as tk
from ShipNet import ShipNet
import pickle

screen_height = 1000
screen_width = 1000

root = tk.Tk()

canvas = tk.Canvas(root, width=screen_width, height=screen_height, bg='black')
canvas.pack()

def distance(x1, y1, x2, y2):
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)

def getInputs(ship, game):
    asteroids = [asteroid[0] for asteroid in game.asteroids]
    asteroids = [(asteroid.x, asteroid.y)  for asteroid in asteroids]

    x_pos, y_pos = 0,0
    min_distance = 1000
    for x, y in asteroids:
        if distance(ship.x, ship.y, x, y) < min_distance:
            min_distance = distance(ship.x, ship.y, x, y)
            x_pos = x
            y_pos = y

    return [abs(ship.theta -math.atan2(ship.y-y_pos,ship.x-x_pos)), min_distance]

class Simulation:
    def __init__(self, canvas = None, brain = None):

        self.canvas = canvas
        self.score = 0
        self.sim = Game(screen_width, screen_height, canvas= self.canvas)
        self.ship = Ship(math.pi/2, screen_width/2, screen_height/2, self.sim, canvas = canvas)

        if brain:
            self.ship.brain = brain
        
        if self.canvas:
            ship_id = canvas.create_polygon((0,0,0,0,0,0,0,0), fill= 'white')
        else:
            ship_id = -1
        
        self.sim.ships.append([self.ship, ship_id])
        

    def simulate(self):
        if self.canvas:
            def game_loop():
                self.sim.update()
                inputs = getInputs(self.ship, self.sim)
                self.ship.action(inputs)
                if not self.sim.game_over:
                    canvas.after(10, game_loop)

            game_loop()
            root.mainloop()
        else:
            while not self.sim.game_over:
                self.sim.update()
                inputs = getInputs(self.ship, self.sim)
                self.ship.action(inputs)
            self.score = self.ship.score

def load_networks():
    with open(f"networks.pkl", "rb") as file:
        return pickle.load(file)
    
def simulateGeneration(initial = None):
    if not initial:
        initial = load_networks()

    offspring = []
    for brain in initial:
        for i in range(10):
            offspring.append(brain.reproduce())
    
    for i in range(len(offspring)):
        sim = Simulation(brain = offspring[i])
        sim.simulate()
        offspring[i] = [sim.score, offspring[i]]
    
    offspring.sort(reverse= True, key = lambda x: x[0])
    offspring = offspring[:10]
    offspring = [child[1] for child in offspring]

    with open("networks.pkl", "wb") as file:
        pickle.dump(offspring, file)

def display_generation():
    offspring = load_networks()
    sim = Simulation(brain = offspring[0], canvas = canvas)
    sim.simulate()

for i in range(10):
    simulateGeneration()
