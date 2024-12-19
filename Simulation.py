from Game_Class import Game
from Ship_Class import Ship
import math
import tkinter as tk

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


def simulate(ship = None):
    sim = Game(screen_width, screen_height, canvas= canvas)

    ship_id = canvas.create_polygon((0,0,0,0,0,0,0,0), fill= 'white')
    ship = Ship(math.pi/2, screen_width/2, screen_height/2, sim, canvas = canvas)

    sim.ships.append([ship, ship_id])

    def game_loop():
        sim.update()
        inputs = getInputs(ship, sim)
        ship.action(inputs)
        if not sim.game_over:
            canvas.after(10, game_loop)

    game_loop()


simulate()
root.mainloop()
