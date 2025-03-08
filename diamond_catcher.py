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