from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time

w_width, w_height = 500, 600

def mpl(x1,y1,x2,y2):
    dx = int(abs(x2-x1))
    dy = int(abs(y2-y1))

    x,y = int(x1),int(y1)

    if x2>x1:
        inc_x = 1
    else:
        inc_x = -1

    if y2>y1:
        inc_y = 1
    else:
        inc_y = -1
    
    if dx>dy:
        d = 2*dy - dx

        for i in range(dx):
            glVertex2i(x,y)
            if d>0:
                y += inc_y
                d -= 2*dx
            x += inc_x
            d += 2*dy
    else:
        d = 2*dx - dy
        for i in range(dy):
            glVertex2i(x,y)
            if d>0:
                x += inc_x
                d -= 2*dy
            y += inc_y
            d += 2*dx

#catcher
c_width, c_height = 120, 20
c_color = (1.0,1.0,1.0)
c_x = (w_width - c_width)//2
c_y = 10

#diamond
d_size = 25
d_x = random.randint(50, w_width-50)
d_y = w_height - 80
d_speed = 100

#buttons
b_y = w_height - 50
b_width = 40
b_height = 40

#left arrow
la_x = 20

#pause
p_x = w_width//2 - b_width//2

#exit
cl_x = w_width-4*b_width//2

paused = False
game_over = False
score = 0
end_time = time.time()


def diamonds(x,y,size):
    glColor3f(1.0, 1.0, 0.0)
    glBegin(GL_POINTS)
    mpl(x,y+size//2, x+size//2,y) #top-right
    mpl(x+size//2,y, x,y-size//2) #bottom-right
    mpl(x,y-size//2, x-size//2,y) #bottom-left
    mpl(x-size//2,y, x,y+size//2) #top-left
    glEnd()

def catcher(x,y,w,h):
    glColor3f(*c_color)
    glBegin(GL_POINTS)
    mpl(x,y, x+w,y) #bottom
    mpl(x,y, x+w//5,y+h) #left
    mpl(x+w,y, x+w-w//5,y+h) #right
    mpl(x+w//5,y+h, x+w-w//5,y+h) #top
    glEnd()

def left_arrow(x,y,w,h):
    glColor3f(0.0,0.9,1.0)
    glBegin(GL_POINTS)
    mpl(x,y+h//2, x+w,y+h//2) #middle
    mpl(x,y+h//2, x+w//2,y) #bottom
    mpl(x,y+h//2, x+w//2,y+h) #top
    glEnd()

def pause(x,y,w,h):
    glColor3f(1.0, 0.6, 0.0)
    glBegin(GL_POINTS)
    w1 = 2*h//3 
    if paused:
        mpl(x, y, x+w1, y+w1//2) #bottom
        mpl(x, y+w1, x+w1, y+w1//2) #top
        mpl(x,y, x,y+w1) #left
    else:
        mpl(x+w1//2, y, x+w1//2, y +3*w//4) #left
        mpl(x+w1, y, x+w1, y+3*w//4) #right
    glEnd()

def exit_button(x,y,w,h):
    glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_POINTS)
    mpl(x,y, x+w, y+h)
    mpl(x+w, y, x, y+h)
    glEnd()

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    diamonds(d_x, d_y, d_size)
    catcher(c_x, c_y, c_width, c_height)
    left_arrow(la_x, b_y, b_width, b_height)
    pause(p_x, b_y, b_width, b_width)
    exit_button(cl_x, b_y, b_height, b_height)
    glutSwapBuffers()


def update_game(game):
    global d_y, game_over, score, d_speed, end_time

    if game_over or paused:
        return
    current_time = time.time()
    d_time = current_time - end_time
    end_time = current_time
    d_y = d_y - d_speed * d_time

    #collision - score increase
    if(c_x < d_x + d_size) and (c_x + c_width > d_x) and (c_y < d_y + d_size) and (c_y + c_height > d_y):
        score += 1
        print(f"Score: {score}")
        state_reset_diamond()
        d_speed+=10

    #diamond miss - game over
    elif d_y < 0:
        if not game_over:  # Ensure Game Over prints only once
            print(f"Game Over! Final Score: {score}")
        state_game_over()
        return
        
    glutPostRedisplay()
    if not paused and not game_over:
        glutTimerFunc(16, update_game, 0)

def state_reset_diamond():
    global d_x, d_y, paused
    if game_over:
        return 
    d_x = random.randint(50, w_width-50)
    d_y = w_height - 50
    paused = False

    glutPostRedisplay()
    glutTimerFunc(16, update_game, 0)

def state_game_over():
    global game_over, c_color
    game_over = True
    c_color = (1.0, 0.0, 0.0)
    glutPostRedisplay()

def state_restart():
    global score, game_over, c_color,d_speed, end_time
    score = 0
    game_over = False
    c_color = (1.0, 1.0, 1.0)
    d_speed = 100
    state_reset_diamond()
    print("Starting Over!")
    end_time = time.time()
    glutTimerFunc(16, update_game, 0)
    glutPostRedisplay()

def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, w_width, 0, w_height) 
    glMatrixMode(GL_MODELVIEW)

glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(w_width, w_height)
glutCreateWindow(b"Catch the Diamonds!")
init()
glutDisplayFunc(display)
glutTimerFunc(16, update_game, 0)  # Start update loop
glutMainLoop()
