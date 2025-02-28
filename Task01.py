#Task1
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import math
import random

w_width, w_height = 900, 500
rain_count = 20
rain_speed = 10
length = 50
direction = 0

class Raindrop:
    def __init__(self, color):
        self.x = random.randint(-w_width//2, w_width//2)
        self.y = random.randint(-w_height, w_height-10)
        self.color = color

    def fall(self):
        self.x += direction *0.5
        self.y -= rain_speed
        if self.y < -w_height:
            self.x = random.randint(-w_width//2, w_width//2)
            self.y = random.randint(-w_height, w_height-10)

    def draw(self):
        glColor3f(*self.color)
        glVertex2f(self.x, self.y)
        glVertex2f(self.x + direction, self.y - length)

class Rain:
    def __init__(self, count):
        self.drops_b = [Raindrop((0.0, 0.0, 1.0)) for b in range(count)]
        self.drops_g = [Raindrop((1.0, 1.0, 1.0)) for g in range(count)]

    def update(self):
        for drop in self.drops_b:
            drop.fall()
        for drop in self.drops_g:
            drop.fall()
        glutPostRedisplay()

    def draw(self):
        glLineWidth(1.5)
        glBegin(GL_LINES)
        for drop in self.drops_b:
            drop.draw()
        for drop in self.drops_g:
            drop.draw()
        glEnd()

rain = Rain(rain_count)

def keyboard_listeners_rain(key, x, y):
    global rain_speed, direction

    if key == GLUT_KEY_UP:
        rain_speed += 1
        print("Speed increased")
    
    if key == GLUT_KEY_DOWN:
        if rain_speed>1:
            rain_speed -= 1
            print("Speed decreased")
        else:
            print("minimum speed reached.")
    
    if key == GLUT_KEY_RIGHT:
        if direction<20:
            direction += 1
            print("bent right")
        else:
            print("Maximum bent right")

    if key == GLUT_KEY_LEFT:
        if direction > -20:
            direction -= 1
            print("bent left")
        else:
            print("Maximum bent left")
    glutPostRedisplay()

def background():
    # Sky
    global day_progress

    color = (0.53, 0.81, 0.92)  # Sky Blue
    glBegin(GL_QUADS)
    r = day_progress * color[0]
    g = day_progress * color[1]
    b = day_progress * color[2]

    glColor3f(r, g, b)
    glVertex2f(-w_width//2, w_height//-4) #sky bottom left
    glVertex2f(w_width//2, w_height//-4) #sky bottom right
    glVertex2f(w_width//2, w_height)
    glVertex2f(-w_width//2, w_height)
    glEnd()

    # Ground
    glBegin(GL_QUADS)
    glColor3f(0.8, 0.52, 0.25)  # Brown ground
    glVertex2f(-w_width, -w_height) #ground bottom left
    glVertex2f(w_width, -w_height) #ground bottom right
    glVertex2f(w_width//2, -w_height//4) #ground top right
    glVertex2f(-w_width//2, -w_height//4)  #ground top left
    glEnd()

    #trees
    glBegin(GL_TRIANGLES)
    glColor3f(0.34, 0.69, 0.19)  # Grass green
    x = -w_width//2  
    while x < w_width//2: 
        glVertex2f(x, -w_width//4)  # Left base
        glVertex2f(x + 35, w_height//4)  # top
        glVertex2f(x + 60 , -w_width//4)  # Right base
        x += 60
    glEnd()

day = True  
day_progress = 1  

def update_day_night(value):
    global day_progress

    target = 1.0 if day else 0.0
    if day_progress != target:
        step = 0.001
        if day_progress < target:
            day_progress = min(day_progress + step, target)
        else:
            day_progress = max(day_progress - step, target)
        
        glutTimerFunc(100, update_day_night, 0)


def keyboard_transition(key, x, y):
    global day
    if key == b'd':
        day = True 
        print("day")
    elif key == b'n':
        day = False  
        print("night")
    glutPostRedisplay()

def house():
    #base
    glColor3f(1.0, 1.0, 0.0) #yellow
    glBegin(GL_TRIANGLES)
    glVertex2f(-200, -250)     # Bottom-left
    glVertex2f(200, -250)     # Bottom-right
    glVertex2f(-200, 0)       # Top-left
    
    glVertex2f(200, -250)       # Bottom-right
    glVertex2f(200, 0)       # Top-right
    glVertex2f(-200, 0)      # Top-left
    
    glVertex2f(-200, 0)      # Top-left
    glVertex2f(200, 0)       # Top-right
    glVertex2f(0, 250)      # Top point
    glEnd()


    # roof
    glColor3f(0.8,0.3,0.2)  # Red color
    glBegin(GL_TRIANGLES)
        # roof-left
    glVertex2f(-250, 0) #bottom-right
    glVertex2f(-200, 0) #bottom-left
    glVertex2f(0, 250) #top
    glVertex2f(0, 250) #top
    glVertex2f(0, 200) #top-down
    glVertex2f(-200, 0) #bottom-right

        # roof-right
    glVertex2f(200, 0) #bottom-left
    glVertex2f(250, 0) #bottom-right
    glVertex2f(0, 250) #top
    glVertex2f(0, 250) #top
    glVertex2f(0, 200) #top-down
    glVertex2f(200, 0) #bottom-left
    
    #chimney
    glVertex2f(100, 150) #bottom-left
    glVertex2f(150, 100) #bottom-right
    glVertex2f(100, 200) #top
    glVertex2f(100,200) #top    
    glVertex2f(150,200) #top-right
    glVertex2f(150,100) #bottom-right

    

    glEnd()

    # Door
    glColor3f(0.4, 0.2, 0.0)  # Dark brown 
    glBegin(GL_TRIANGLES)
    glVertex2f(-40, -250)  # Bottom-left
    glVertex2f(40, -250)   # Bottom-right
    glVertex2f(-40, -10)    # Top-left

    glVertex2f(40, -250)   # Bottom-right
    glVertex2f(40, -10)     # Top-right
    glVertex2f(-40, -10)    # Top-left
    glEnd()

    glPointSize(6)
    glColor3f(0.0, 0.0, 0.0)
    glBegin(GL_POINTS)
    glVertex2f(-30, -120)
    glEnd()

    # window
    glColor3f(0.53, 0.81, 0.92)
    glBegin(GL_TRIANGLES)
    glVertex2f(70, -70) #bottom-left
    glVertex2f(130, -70) #bottom right
    glVertex2f(130, 20)  #top right

    glVertex2f(130, 20) #top right
    glVertex2f(70, 20) #top left
    glVertex2f(70, -70) #bottom left

    glEnd()

    glColor3f(0.53, 0.81, 0.92)
    glBegin(GL_TRIANGLES)
    glVertex2f(-70, -70) #bottom-left
    glVertex2f(-130, -70) #bottom right
    glVertex2f(-130, 20)  #top right

    glVertex2f(-130, 20) #top right
    glVertex2f(-70, 20) #top left
    glVertex2f(-70, -70) #bottom left

    glEnd()

    #window lines
    glColor3f(0.0, 0.0, 0.0)
    glBegin(GL_LINES)
    glVertex2f(70, -25) #start-x
    glVertex2f(130, -25) #end-x
    glVertex2f(100, -70) #start-y
    glVertex2f(100, 20) #end-y
    glEnd()

    glColor3f(0.0, 0.0, 0.0)
    glBegin(GL_LINES)
    glVertex2f(-70, -25) #start-x
    glVertex2f(-130, -25) #end-x
    glVertex2f(-100, -70) #start-y
    glVertex2f(-100, 20) #end-y
    glEnd()

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    background()
    house()
    rain.draw()
    glutSwapBuffers()

def idle():
    update_day_night(0)
    rain.update()
    glutPostRedisplay()

glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(w_width, w_height)
glutCreateWindow(b"Building a House in Rainfall")
glClearColor(0, 0, 0, 1)
gluOrtho2D(-w_width//2, w_width//2, -w_height, w_height)

glutDisplayFunc(display)
glutIdleFunc(idle)
glutSpecialFunc(keyboard_listeners_rain) 
glutKeyboardFunc(keyboard_transition)
glutMainLoop()