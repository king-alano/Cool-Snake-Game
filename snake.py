"""
auth: AJ Boyd
date: 8/26/23
desc: implementation of a simple Snake game with slight additions/improvements
"""

from tkinter import *
import random 

#constants 
PIXEL_SIZE = 50
GAME_DIM = 650
FOOD_COLOR = "#EC1313"
SNAKE_COLOR = "#17CD17"
SPEED_START = 150
SPEED_INTERVAL = 12
SIZE_INTERVAL = 5

#implementation of the Apple class which represents the food the Snake will get
class Apple:
    def __init__(self, c):
        self.color = c
        self.coords = [0, 0]
    
    #places an apple at a random place
    def place(self, cv, x, y):
        cv.delete("apple")
        cv.create_rectangle(x, y, x+PIXEL_SIZE, y+PIXEL_SIZE, tag = "apple", fill = self.color)
        self.coords = (x, y)

#implementation of the Snake class which represents the protagonist     
class Snake:
    def __init__(self, c):
        self.color = c
        self.size = 2
        self.coords = [(0,0)] #a list of tuples which represent the squares the Snake occupies
    
    #draws squares representing the Snake's body according to its coordinates
    def show(self, cv):
        #clears all Snake squares
        cv.delete("snake") 
        #places all Snake squares
        for x, y in self.coords:
            cv.create_rectangle(x, y, x + PIXEL_SIZE, y + PIXEL_SIZE, fill=self.color, tag="snake")
            
#implementation of the Game class that handles main functionality
class Game:
    def __init__(self, px, dim):
        #game elements
        self.Apple = Apple(FOOD_COLOR)
        self.Snake = Snake(SNAKE_COLOR)
        
        #game settings
        self.speed = SPEED_START
        self.score = 0
        self.direction = "RIGHT" 
        
        #window properties
        self.px = px
        self.width = dim
        self.height = dim
        self.window = Tk()
        self.label = None
        self.cv = None
        self.initWindow(self.window) #creates window 
        
        #start game
        self.placeApple()
        self.Snake.show(self.cv)
        self.updateCV()
    
    #start the game
    def start(self):
        self.window.mainloop()
              
    #formats the window and canvas elements as well as keybinds
    def initWindow(self, window):
        #window.resizable(False, False)
        window.title("Snake! :3")
        self.label = Label(window, text="Length:{}\tScore:{}".format(self.Snake.size, self.score), font=("consolas", 20))
        self.label.pack()
        self.cv = Canvas(window, background = "#000000", height = self.height, width = self.width)
        self.cv.pack(expand=True)
        window.bind('<Left>', lambda event: self.changeDirection("LEFT"))
        window.bind('<Right>', lambda event: self.changeDirection("RIGHT"))
        window.bind('<Up>', lambda event: self.changeDirection("UP"))
        window.bind('<Down>', lambda event: self.changeDirection("DOWN"))
   
    #move apple
    def placeApple(self, min=0, max=GAME_DIM - PIXEL_SIZE):
        x = random.randrange(min, int(max / PIXEL_SIZE)) * PIXEL_SIZE
        y = random.randrange(min, int(max / PIXEL_SIZE)) * PIXEL_SIZE
        
        #if the Apple's coords exist on the Snake, re-roll the coords
        while((x,y) in self.Snake.coords):
            x = random.randrange(min, int(max / PIXEL_SIZE)) * PIXEL_SIZE
            y = random.randrange(min, int(max / PIXEL_SIZE)) * PIXEL_SIZE
            
        self.Apple.place(self.cv, x, y)
    
    #updates the canvas
    def updateCV(self):
        x, y = self.Snake.coords[0] #the head coordinates of the Snake
        
        if(self.direction == "UP"):
            y -= PIXEL_SIZE
        elif(self.direction == "DOWN"):
            y += PIXEL_SIZE
        elif(self.direction == "RIGHT"):
            x += PIXEL_SIZE
        else:
            x -= PIXEL_SIZE
        
        #add new coord at head
        self.Snake.coords.insert(0, (x,y))
        
        #re-print the Snake
        self.Snake.show(self.cv)
        self.Snake.head = self.Snake.coords[0]
        
        #check if snake has eaten Apple
        if(self.Snake.head == self.Apple.coords):
            self.eat()
        else:
            #remove last coord
            self.Snake.coords.pop(len(self.Snake.coords) - 1) 
        
        #if wall collision, end game; else, keep going
        if self.checkCollision():
            self.gameOver()
        else:
            self.window.after(self.speed, self.updateCV)
 
    #changes the direction of the snake
    def changeDirection(self, dir):
        if(dir == "UP" and self.direction != "DOWN" or 
        dir == "DOWN" and self.direction != "UP" or
        dir == "RIGHT" and self.direction != "LEFT" or
        dir == "LEFT" and self.direction != "RIGHT"):
            self.direction = dir
 
    #checks collision between snake and wall
    def checkCollision(self):
        if(self.Snake.head[0] >= GAME_DIM or 
           self.Snake.head[0] < 0 or
           self.Snake.head[1] >= GAME_DIM or
           self.Snake.head[1] < 0):
            return True
        elif(self.Snake.head in self.Snake.coords[1:]):
            return True
    
    #increases score, length, and places new Apple
    def eat(self):
        self.Snake.size += 1
        self.score += 50 + 10 * self.Snake.size
        self.label.config(text="Length:{}\tScore:{}".format(self.Snake.size, self.score))
        self.label.pack()
        self.placeApple()
        
        #increase speed of Snake as score increases, maxing out when Snake is 45 units long
        if(self.Snake.size <= 45):
            self.speed = SPEED_START - self.Snake.size // SIZE_INTERVAL * SPEED_INTERVAL

    #checks if the game is over
    def gameOver(self):
        self.cv.delete("all")
        self.cv.create_text(self.cv.winfo_width()/2, self.cv.winfo_height()/2, fill = "red", text = "Game Over\nPress 'R' to restart!", font = ("consolas", 40), tag = "gameover")
        self.window.bind('<Key>', lambda event: self.restart(event))
        
    #restart by closing the window, and creating a new object
    def restart(self, e):
        if(e.char == 'r'):
            self.cv.delete("gameover")
            self.window.destroy()
            self.__init__(PIXEL_SIZE, GAME_DIM)
            self.window.focus_force()
            self.start()
   
#start the game         
Game(PIXEL_SIZE, GAME_DIM).start()