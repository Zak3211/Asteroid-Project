import math
import tkinter as tk
import random
import json
import webbrowser
from PIL import Image, ImageTk


#declared here so that they can be static
#Configuration of window and canvas
window = tk.Tk()

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window.attributes("-fullscreen", True)
window.geometry(f'{screen_width}x{screen_height}')

canvas = tk.Canvas(window, bg = 'black', highlightthickness=0)
canvas.config(width = screen_width, height = screen_height)

score = canvas.create_text(screen_width/2, 50, text = 'Score:  0',
                           font = ('arial', 15), fill = 'white')
canvas.pack()

class Game:
    '''main game class'''
    def __init__(self):
        self.ships = []
        self.bullets = []
        self.asteroids = []
        self.is_paused = False
        self.event = None

        #self.bullets.append([bullet(x = screen_width/2, y = screen_height/2, theta = 0), -1])
        with open("game.json", "r", encoding='utf-8') as file:
            temp = json.load(file)
            self.score = temp["_"]
    #initializes a 1v1 game
    def game1(self):
        '''initializes and returns a 1v1 game'''
        game1 = Game()
        player_id = canvas.create_polygon((0,0,0,0,0,0,0,0), fill= 'white')
        game1.ships.append([Ship(math.pi, screen_width - 100, screen_height/2), player_id])

        opponent_id = canvas.create_polygon((0,0), fill= 'white')
        game1.ships.append([Ship(0, 100, screen_height/2), opponent_id])
        return game1
    #Initializes a game of player v asteroids
    def game2(self):
        '''Initializes and returns a 1 player game'''
        game2 = Game()
        player_id = canvas.create_polygon((0,0), fill= 'white')
        game2.ships.append([Ship(-math.pi/2, screen_width/2, screen_height/2), player_id])
        return game2
    def restart(self):
        '''resets all game parameteres'''
        self.ships = []
        self.bullets = []
        self.asteroids = []
        self.is_paused = False

        #self.bullets.append([bullet(x = screen_width/2, y = screen_height/2, theta = 0), -1])
        self.score = 0
        canvas.itemconfig(score, text = "Score: 0")
        #deletes everything except score menu
        for item in canvas.find_all():
            if canvas.type(item) != "text":
                canvas.delete(item)

        player_id = canvas.create_polygon((0,0), fill= 'white')
        self.ships.append([Ship(-math.pi/2, screen_width/2, screen_height/2), player_id])

    def update(self):
        '''updates the game state based on new events'''
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
    #function that prevents ships from going off screen
    def keep_in_bounds(self):
        '''removes out of bounds entities'''
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
                        #update score
                        self.score += 1
                        canvas.itemconfig(score, text = f'Score: {self.score}')
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
    #randomly generates asteroid on either of the 4 edges
    def generate_asteroid(self):
        #set difficulty based on score
        difficulty = 0.009 + 0.0003*self.score
        if random.randint(0,1000) <= 1000*difficulty:
            temp = Asteroid(random.randint(1,3), speed = 1 + 40*difficulty)
            self.asteroids.append([temp, temp.draw_asteroid(-1)])

class Ship:
    def __init__(self, theta, xcoord, ycoord) -> None:
        self.theta = theta
        
        #use for cheat codes
        self.is_invincible = False
        self.event = None
        self.is_helper = False

        #prevents overflow errors
        self.theta %= 2 * math.pi

        self.x = xcoord
        self.y = ycoord
        self.is_alive = True

        self.omega = 0.3

    def turn_left(self, event = None) -> None:
        self.event = event
        self.theta -= self.omega

    def turn_right(self, event) -> None:
        self.event = event
        self.theta += self.omega

    def move(self, event = None) -> None:
        speed = 5
        self.x += speed * math.cos(self.theta)
        self.y += speed * math.sin(self.theta)

    def shoot(self,  event = None):
        return Bullet(self.theta, self.x + 50*math.cos(self.theta),
                       self.y + 50*math.sin(self.theta))

    def draw_ship(self, player_id):
        s = 0.75
        theta = self.theta
        x = self.x
        y = self.y

        new_coords = [x + s*50*math.cos(theta), y + s*50*math.sin(theta),
                    x + s*25*math.cos(theta + 90), y + s*25*math.sin(theta + 90),
                    x + s*15*math.cos(theta), y + s*15*math.sin(theta),
                    x + s*25*math.cos(theta - 90), y + s*25*math.sin(theta - 90)]
        canvas.coords(player_id, new_coords)

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

class Asteroid:
    def __init__(self, size, speed):
        self.size = size
        self.x = random.randint(0, screen_width)
        self.y = random.randint(0, screen_height)
        self.speed = speed

        #assign randomly to one of the edges
        temp = random.randint(1,4)
        if temp == 1:
            self.x = 0
        elif temp == 2:
            self.x = screen_width
        elif temp == 3:
            self.y = 0
        else:
            self.y = screen_height

        if self.y > screen_height/2:
            self.theta = math.atan((screen_height/2 - self.y)/(screen_width/2 - self.x + 0.01))
        else:
            self.theta = math.atan((screen_width/2 - self.x)/(screen_height/2 - self.y + 0.01))

        if self.x >  screen_width/2:
            self.theta += math.pi

        self.theta %= 2*math.pi

    def move(self):
        speed = self.speed
        self.x += speed * math.cos(self.theta)
        self.y += speed * math.sin(self.theta)
    def draw_asteroid(self, asteroid_id):

        s = 10
        x = self.x
        y = self.y
        if self.size == 1:
            coords = (x-s*2, y+s*1, x-s*4, y-s*1, x, y-s*1, x+s*3, y-s*3, x+s*2, y+s*1)
        elif self.size == 2:
            coords = (x,y+s*4, x-s*3,y, x, y-s*4, x+s*4,y-s*2, x+s*4, y+s*2, x, y + s*2)
        elif self.size == 3:
            coords = (x-s*5, y+s*5,x-s*7, y, x-s*3, y-s*2, x+s*3, y-s*2,
                       x+s*4, y-s*4, x+s*6, y-s*1, x+s*5, y+s*5)
        else:
            coords = None
        if asteroid_id == -1:
            return canvas.create_polygon(coords, outline='white')
        else:
            canvas.coords(asteroid_id, coords)

#Code for GUI
def main():
    '''main game method'''

    #Instantiating game
    game1 = Game.game2(None)
    game1.is_paused = True

    def start_game():
        game1.is_paused = False
        start.place_forget()
    start = tk.Frame(window, bg='black')

    start_button = tk.Button(start, text = 'Start Game!',
                             width = 30,  command = start_game,
                             borderwidth=0)
    start_button.pack(padx = 10, pady = 30)

    start.place(relx=0.5, rely=0.5, anchor='center')

    def quit_game():
        #code for leaderboard
        with open("leaderboard.json", 'r', encoding='utf-8') as file:
            leaderboard = json.load(file)

        leaderboard = leaderboard['_']
        leaderboard.append([game1.score, "Zak"])
        leaderboard = sorted(leaderboard, key=lambda x: x[0], reverse=True)
        leaderboard = {"_": leaderboard}

        with open("leaderboard.json", "w", encoding='utf-8') as file:
            json.dump(leaderboard, file)
        #reset score to zero
        with open("game.json", "w", encoding='utf-8') as file:
            temp = {"_": 0}
            json.dump(temp, file)
        window.quit()

    def save_and_exit():
        with open("leaderboard.json", "w", encoding='utf-8') as file:
            json.dump(leaderboard, file)
        #code for saving game
        with open("game.json", "w", encoding='utf-8') as file:
            temp = {"_": game1.score}
            json.dump(temp, file)
        window.quit()

    def restart():
        game1.restart()
        pause_menu.place_forget()
        death_menu.place_forget()

        background = canvas.create_image(0, 0, image=galaxy_image, anchor="nw")
        canvas.tag_lower(background)

    #Pause Menu Configuration
    pause_menu = tk.Frame(window, bg='gray', width=800, height=200)
    pause_menu.place(relx=0.5, rely=0.5, anchor='center')

    pause_label = tk.Label(pause_menu, text="Game Paused",
                           bg='gray', fg='white', font=("Helvetica", 24))
    pause_label.pack(pady=20, padx = 30)

    resume_button = tk.Button(pause_menu, text="Resume", command=lambda: pause(None), width=30)
    resume_button.pack(pady=10)

    quit_button = tk.Button(pause_menu, text = 'Quit', command = quit_game, width= 30)
    quit_button.pack(pady = 10)

    restart_button = tk.Button(pause_menu, text = 'Restart', command =  restart, width = 30)
    restart_button.pack(pady = 10)

    save_button = tk.Button(pause_menu, text = 'Save and Exit',
                            command =  save_and_exit, width = 30)
    save_button.pack(pady = 10)

    death_menu = tk.Frame(window, bg = 'gray', width = 800, height = 200)
    death_menu.place(relx=0.5, rely=0.5, anchor='center')

    #Leaderboard menu
    def display_leaderboard():
        death_menu.place_forget()
        leaderboard_menu.place(relx=0.5, rely=0.5, anchor='center')

    def close_leaderboard():
        leaderboard_menu.place_forget()
        death_menu.place(relx=0.5, rely=0.5, anchor='center')

    with open("leaderboard.json",'r', encoding='utf-8') as file:
        leaderboard = json.load(file)

    leaderboard_menu = tk.Frame(window, bg = 'gray', )
    leaderboard_menu.place(relx=0.5, rely=0.5, anchor='center')

    s1 = f"{leaderboard['_'][0][1]}: {leaderboard['_'][0][0]}"
    first_label = tk.Label(leaderboard_menu, text=s1,
                           bg='gray', fg='white', font=("Helvetica", 24))
    first_label.pack(pady=20, padx = 30)

    s2 = f"{leaderboard['_'][1][1]}: {leaderboard['_'][1][0]}"
    second_label = tk.Label(leaderboard_menu,text = s2,
                             bg='gray', fg='white', font=("Helvetica", 24))
    second_label.pack(pady=20, padx = 30)

    s3 = f"{leaderboard['_'][2][1]}: {leaderboard['_'][2][0]}"
    third_label = tk.Label(leaderboard_menu, text = s3,
                            bg='gray', fg='white', font=("Helvetica", 24))
    third_label.pack(pady=20, padx = 30)

    s4 = f"{leaderboard['_'][3][1]}: {leaderboard['_'][3][0]}"
    fourth_label = tk.Label(leaderboard_menu, text = s4,
                             bg='gray', fg='white', font=("Helvetica", 24))
    fourth_label.pack(pady=20, padx = 30)

    s5 = f"{leaderboard['_'][4][1]}: {leaderboard['_'][4][0]}"
    fifth_label = tk.Label(leaderboard_menu, text = s5,
                           bg='gray', fg='white', font=("Helvetica", 24))
    fifth_label.pack(pady=20, padx = 30)

    back_button1 = tk.Button(leaderboard_menu, text = 'Back',
                             command = close_leaderboard, width = 30)
    back_button1.pack(pady=30)

    leaderboard_menu.place_forget()

    #death menu
    def die():
        score_label.config(text = f"Score: {game1.score}")
        death_menu.place(relx=0.5, rely=0.5, anchor='center')
        game1.is_paused = True
        pause_menu.place_forget()
        controls_menu.place_forget()
        cheat_menu.place_forget()


    death_label = tk.Label(death_menu, text = 'You Died :(',
                            bg='gray', fg='white', font=("Helvetica", 24))
    death_label.pack(pady = 10, padx = 30)

    score_label = tk.Label(death_menu, text = f"Score: {game1.score}",
                           bg='gray', fg='white', font=("Helvetica", 24))
    score_label.pack(pady = 10, padx = 30)

    quit_button2 = tk.Button(death_menu, text = 'Quit', command = quit_game, width= 30)
    quit_button2.pack(pady = 10, padx = 30)

    restart_button2 = tk.Button(death_menu, text = 'Restart', command =  restart, width = 30)
    restart_button2.pack(pady = 10)

    leaderboard_button= tk.Button(death_menu, text = 'Leaderboard',
                                  command = display_leaderboard, width = 30)
    leaderboard_button.pack(pady = 10)
    death_menu.place_forget()


    #controls menu
    def open_controls():
        pause_menu.place_forget()
        controls_menu.place(relx=0.5, rely=0.5, anchor='center')
        window.bind("<Escape>",lambda event: close_controls())
    def close_controls():
        controls_menu.place_forget()
        pause_menu.place(relx=0.5, rely=0.5, anchor='center')
        window.bind("<Escape>", pause)

    controls_button = tk.Button(pause_menu, text = 'Settings', command = open_controls, width = 30)
    controls_button.pack(pady = 10)
    pause_menu.place_forget()


    #load current key bindings
    with open('Controls.json', 'r', encoding='utf-8') as file:
        key_bindings = json.load(file)

    def take_input(event):
        if len(game1.ships) == 0:
            return
        player = game1.ships[0][0]
        key = event.keysym.lower()
        if not game1.is_paused:
            if key == key_bindings['turn_left']:
                player.turn_left(event)
            elif key == key_bindings['turn_right']:
                player.turn_right(event)
            elif key == key_bindings['move']:
                player.move(event)
            elif key == key_bindings['shoot']:
                bullet_id = canvas.create_oval(player.x - 3, player.y - 3,
                                               player.x + 3, player.y + 3, fill='red')
                game1.bullets.append([player.shoot(event), bullet_id])
            elif key == 'b':
                pause(None)
                url = 'https://web.cs.manchester.ac.uk/16321-material/new-labs/Coursework/Coursework-02.php'
                webbrowser.open(url)
                
    def configure_controls(control):
        wait = tk.StringVar()
        wait.set('.')
        def config_controls(event, control):
            with open('Controls.json', 'r', encoding='utf-8') as file:
                key_bindings = json.load(file)
            key_bindings[control] = event.keysym.lower()
            with open('Controls.json', 'w', encoding='utf-8') as file:
                json.dump(key_bindings, file)
            wait.set('_')

        window.bind("<KeyPress>", lambda event: config_controls(event, control))
        window.wait_variable(wait)
        window.unbind("<KeyPress>")
        window.bind("<Key>", take_input)
        with open('Controls.json', 'r', encoding='utf-8') as file:
            key_bindings = json.load(file)
        #display updated controls
        left_button.config(text = f"Turn Left : {key_bindings['turn_left']}")
        right_button.config(text = f"Turn Right : {key_bindings['turn_right']}")
        move_button.config(text = f"Move : {key_bindings['move']}")
        shoot_button.config(text = f"Shoot : {key_bindings['shoot']}")

    controls_menu = tk.Frame(window, bg='gray', width=800, height=200)
    controls_menu.place(relx=0.5, rely=0.5, anchor='center')

    controls_label = tk.Label(controls_menu, text="Settings",
                              bg='gray', fg='white', font=("Helvetica", 24))
    controls_label.pack(pady=20, padx = 30)

    left_button = tk.Button(controls_menu, text = f"Turn Left : {key_bindings['turn_left']}",
                             command = lambda: configure_controls('turn_left'), width = 30)
    left_button.pack(pady = 10)

    right_button = tk.Button(controls_menu, text = f"Turn Right : {key_bindings['turn_right']}",
                             command = lambda: configure_controls('turn_right'), width = 30)
    right_button.pack(pady = 10)

    move_button = tk.Button(controls_menu, text = f"Move : {key_bindings['move']}",
                            command = lambda: configure_controls('move'), width = 30)
    move_button.pack(pady = 10)

    shoot_button = tk.Button(controls_menu, text = f"Shoot : {key_bindings['shoot']}",
                             command = lambda: configure_controls('shoot'), width = 30)
    shoot_button.pack(pady = 10)

    back_button = tk.Button(controls_menu, text = 'Back',
                            command = close_controls, width= 30)
    back_button.pack(pady = 10, padx = 30)
    controls_menu.place_forget()

    #Cheat Codes Menu
    cheat_menu = tk.Frame(window, bg='gray', width=800, height=200)
    cheat_menu.place(relx=0.5, rely=0.5, anchor='center')

    def open_text_input(event):
        game1.event = event
        cheat_menu.place(relx=0.5, rely=0.5, anchor='center')
        game1.is_paused = True

    def input_cheat_code():
        code = text_widget.get()
        code = code.lower()
        game1.is_paused = False
        if code == 'invincible':
            game1.ships[0][0].is_invincible = True
        elif code == 'chaos':
            game1.score = 999
        elif code == 'help':
            game1.ships[0][0].is_invincible = True

            #creates invincible helper ship
            temp_game = Game.game2(None)
            helper = temp_game.ships[0]
            helper[0].is_invincible = True
            helper[0].is_helper  =True
            game1.ships.append(helper)
        elif code == 'black':
            canvas.delete(background)
        elif code == 'die':
            die()
        elif code == "pvp":
            game1.ships = []
            game1.bullets = []
            game1.asteroids = []
            player_id = canvas.create_polygon((0,0,0,0,0,0,0,0), fill= 'white')
            game1.ships.append([Ship(math.pi, screen_width - 100, screen_height/2), player_id])

            opponent_id = canvas.create_polygon((0,0), fill= 'white')
            game1.ships.append([Ship(0, 100, screen_height/2), opponent_id])
            
        cheat_menu.place_forget()

    text_widget = tk.Entry(cheat_menu, width=30)

    close_button = tk.Button(cheat_menu, text = 'Close', command = input_cheat_code)

    text_widget.pack(pady = 10, padx = 10)
    close_button.pack(pady = 10)

    cheat_menu.place_forget()
    window.bind("<t>", open_text_input)

    #Image rendering
    pil_image = Image.open("galaxy_image.jpg")
    pil_image = pil_image.resize((screen_width, screen_height))
    galaxy_image = ImageTk.PhotoImage(pil_image)
    background = canvas.create_image(0, 0, image=galaxy_image, anchor="nw")
    canvas.tag_lower(background)

    #END OF CONFIGURATION
    #Main game loop
    def game_loop():
        if len(game1.ships) == 0:
            die()
        if not game1.is_paused:
            game1.update()
        canvas.after(10, game_loop)
    game_loop()

    #Opens options buttons when game is paused
    def pause(event):
        game1.event = event
        game1.is_paused = not game1.is_paused
        if game1.is_paused:
            pause_menu.place(relx=0.5, rely=0.5, anchor='center')
        else:
            pause_menu.place_forget()
    #Pause functionality and keyboard input
    window.bind("<Key>", take_input)
    window.bind("<Escape>", pause)

    window.mainloop()

main()
