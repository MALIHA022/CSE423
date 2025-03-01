#Task 2
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

w_width, w_height = 800, 600
balls = []

blink = False
frozen = False
speed = 5
size = 5
class Balls:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = random.choice([(-1, 1), (-1, -1), (1, 1), (1, -1)])
        self.color = [random.random(), random.random(), random.random()]
        self.visible = True 

    def move(self):
        if not frozen:
            dx, dy = self.direction 
            self.x += dx * speed
            self.y += dy * speed

        #check bound
        if self.x <= 0:
            self.x = 0 
            dx = abs(dx) 
        elif self.x >= w_width:
            self.x = w_width  
            dx = -abs(dx) 

        if self.y <= 0:
            self.y = 0
            dy = abs(dy) 
        elif self.y >= w_height:
            self.y = w_height
            dy = -abs(dy)

        self.direction = (dx, dy)  #update direction
    
    def visibility(self):
        if blink:
            self.visible = not self.visible

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    
    glPointSize(size)
    glBegin(GL_POINTS)
    for b in balls:
        if b.visible:
            glColor3fv(b.color)
            glVertex2f(b.x, b.y)
    glEnd()
    glutSwapBuffers()

def update(value):
    if not frozen:
        for b in balls:
            b.move()
        
        if blink:
            for b in balls:
                b.visibility()

    glutPostRedisplay()
    glutTimerFunc(20, update, 0)

def mouse(button, state, x, y):
    global blink
    if not frozen:
        if state == GLUT_DOWN:
            if button == GLUT_RIGHT_BUTTON:
                balls.append(Balls(x, w_height - y)) 
                print("New ball added")
            elif button == GLUT_LEFT_BUTTON:
                blink = not blink
                if blink:
                    print("Blinking")
                else:
                    print("Not Blinking")
    glutPostRedisplay()
            

def keyboard(key, x, y):
    global speed, frozen, size
    if key == b' ':
        frozen = not frozen
    if not frozen:
        if key == b'l':
            size = min(20, size + 1)
            print("Ball Size increased")
        if key == b's':
            size = max(5, size - 1)
            print("Ball Size Decreased")
    glutPostRedisplay()

def special_keys(key, x, y):
    global speed
    if frozen:
        return
    
    if key == GLUT_KEY_UP:
        speed += 0.5
        print("Speed Increased")
    elif key == GLUT_KEY_DOWN:
        speed = max(0.5, speed - 0.5)
        print("Speed Decreased")

def reshape(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, w, 0, h)
    glMatrixMode(GL_MODELVIEW)

glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(w_width, w_height)
glutCreateWindow(b"Building the Amazing Box")
glClearColor(0, 0, 0, 1)
glPointSize(5)

glutDisplayFunc(display)
glutReshapeFunc(reshape)
glutMouseFunc(mouse)
glutKeyboardFunc(keyboard)
glutSpecialFunc(special_keys)
glutTimerFunc(16, update, 0)
glutMainLoop()
