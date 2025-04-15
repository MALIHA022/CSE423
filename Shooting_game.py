from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random

# Camera
camera_pos = (0,500,500)

fovY = 120  
GRID_LENGTH = 100  
GRID_SIZE = 12
rand_var = 423

# Game state
player_pos = [0, 0, 0]
player_angle = 0
camera_mode = "third"  
cheat_mode = False
cheat_vision = False
game_over = False

# Bullets
bullets = []

# Enemies
enemies = []
num_enemies = 5

# Player stats
life = 5
missed_bullets = 0
score = 0

def draw_text(x, y, text, font = GLUT_BITMAP_HELVETICA_12):
    glColor3f(1,1,1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    
    gluOrtho2D(0, 1000, 0, 600)  # left, right, bottom, top

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    # Draw text at (x, y) in screen coordinates
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

# grid (game floor)
def draw_grid(GRID_SIZE):
    glBegin(GL_QUADS)
    for i in range(GRID_SIZE ):
        for j in range(GRID_SIZE):
            if (i + j) % 2 == 0:
                glColor3f(1, 1, 1)
            else:
                glColor3f(0.7, 0.5, 0.95)

            x = (i - GRID_SIZE // 2) * GRID_LENGTH
            y = (j - GRID_SIZE // 2) * GRID_LENGTH

            glVertex3f(x, y, 0) #bottom left
            glVertex3f(x + GRID_LENGTH, y, 0) #bottom right
            glVertex3f(x + GRID_LENGTH, y + GRID_LENGTH, 0) #top right
            glVertex3f(x, y + GRID_LENGTH, 0) #top left
    glEnd()

def draw_border_walls():
    pass

def draw_player():
    glPushMatrix()
    
    # Apply global player transform
    glTranslatef(*player_pos)
    glRotatef(player_angle, 0, 0, 1)  # Everything now rotates together

    # Left foot
    glColor3f(0, 0, 1)
    glTranslatef(0,-20,-100)
    glRotatef(90, 0, 1, 0)
    glRotatef(90, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 16, 8, 100, 10, 10) #quadric, base radius, top radius, height, slices, stacks

    # Right
    glColor3f(0, 0, 1)
    glTranslatef(0,-80,0)
    gluCylinder(gluNewQuadric(), 16, 8, 100, 10, 10) #quadric, base radius, top radius, height, slices, stacks

    # Body
    glColor3f(0.4, 0.5, 0)
    glTranslatef(0, 40, -30)
    glutSolidCube(80)

    # Gun
    glColor3f(0.5, 0.5, 0.5)
    glTranslatef(0, 0, 40)
    glTranslatef(30, 0, -90) 
    glRotatef(90, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 20, 5, 120, 10, 10) #quadric, base radius, top radius, height, slices, stacks

    # Left Hand
    glColor3f(1, 0.7, 0.6)
    glTranslatef(0, -25, 0)
    gluCylinder(gluNewQuadric(), 15, 6, 60, 10, 10) #quadric, base radius, top radius, height, slices, stacks

    # Right Hand
    glColor3f(1, 0.7, 0.6)
    glTranslatef(0, 50, 0)
    gluCylinder(gluNewQuadric(), 15, 6, 60, 10, 10) #quadric, base radius, top radius, height, slices, stacks

    # Head
    glColor3f(0, 0, 0)
    glTranslatef(40,-25, -25)
    gluSphere(gluNewQuadric(), 30, 10, 10)

    glPopMatrix()


def draw_bullets():
    glColor3f(1, 0, 0)
    for bullet in bullets:
        glPushMatrix()
        glTranslatef(*bullet['bullet_pos'])
        glutSolidCube(10)
        glPopMatrix()

def draw_enemy(e):
        glPushMatrix()
        glTranslatef(*e['enemy_pos'])
        glScalef(e["scale"], e["scale"], e["scale"]) 

        #body
        glColor3f(1, 0, 0)
        glPushMatrix()
        glTranslatef(0, 0, 40)
        gluSphere(gluNewQuadric(), 40, 20, 20) #quadric, radius, slices, stacks
        glPopMatrix()

        #haed
        glColor3f(0,0,0)
        glPushMatrix()
        glTranslatef(0, 0, 80)
        gluSphere(gluNewQuadric(), 30, 20, 20)
        glPopMatrix()

        glPopMatrix()

def spawn_enemy():
    while True: #avoiding center
        x = random.randint(-600, 500)
        y = random.randint(-600, 500)
        
        if abs(x) > 200 or abs(y) > 200:
            break

    return {
        'enemy_pos': [x, y, 0], #position
        'scale': 1.0, #size
        'scale_dir': 0.005 #pulse
    }
enemies = [spawn_enemy() for _ in range(num_enemies)]

def mouseListener(button, state, x, y):
    global camera_mode

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN and not game_over:
        rad = math.radians(player_angle)
        dir_x = -math.cos(rad)
        dir_y = -math.sin(rad)

        # Offset of the gun tip
        gun_length = 140 
        gun_right = 50
        gun_up = 10

        bullet_start = [player_pos[0] + gun_right * math.sin(rad) + dir_x * gun_length,
                        player_pos[1] - gun_right * math.cos(rad) + dir_y * gun_length,
                        player_pos[2] + gun_up]

        bullets.append({'bullet_pos': bullet_start, 'dir': (dir_x, dir_y)})

    elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN and not game_over:
        if camera_mode == "third":
            camera_mode = "first"
        else:
            camera_mode = "third"
            print(f"Switched to {camera_mode}-person mode")
        
        glutPostRedisplay()
  

def keyboardListener(key, x, y):
    """
    Handles keyboard inputs for player movement, gun rotation, camera updates, and cheat mode toggles.
    """
    global player_pos, player_angle, camera_mode

    speed = 20
    angle_step = 5

    if key == b'w': #move backward
        angle = math.radians(player_angle)
        player_pos[0] += math.cos(angle) * speed
        player_pos[1] += math.sin(angle) * speed

    elif key == b's': #move forward
        angle = math.radians(player_angle)
        player_pos[0] -= math.cos(angle) * speed
        player_pos[1] -= math.sin(angle) * speed

    elif key == b'a':  #rotate left
        player_angle += angle_step

    elif key == b'd': #rotate right
        player_angle -= angle_step
    
    # elif key == b"c": #cheat mode
    #     if camera_mode == "third":
    #         camera_mode = "first"
    #     else:
    #         camera_mode = "third"
            

            
def specialKeyListener(key, x, y):
    """
    Handles special key inputs (arrow keys) for adjusting the camera angle and height.
    """
    global camera_pos
    x, y, z = camera_pos

    if key == GLUT_KEY_UP: # Move camera up
        y += 1

    if key == GLUT_KEY_DOWN: # Move camera down 
        y-= 1

    if key == GLUT_KEY_LEFT: # Move camera left
        x -= 1

    if key == GLUT_KEY_RIGHT:  # Move camera right 
        x += 1

    camera_pos = (x, y, z)

def setupCamera():
    glMatrixMode(GL_PROJECTION)  
    glLoadIdentity()  
    gluPerspective(fovY, 1.25, 0.1, 1500)  #(field of view, aspect ratio, near clip, far clip)
    glMatrixMode(GL_MODELVIEW)  
    glLoadIdentity()

    if camera_mode == "third":
        x, y, z = camera_pos
        gluLookAt(x,y,z, 0,0,0, 0,0,1)  
    else:
        angle = math.radians(player_angle)
        gun_length = 50
        gun_right = 30
        gun_up = 40

        # gun tip position
        cam_x = player_pos[0] + gun_right * math.sin(angle) - math.cos(angle) * gun_length
        cam_y = player_pos[1] - gun_right * math.cos(angle) - math.sin(angle) * gun_length
        cam_z = player_pos[2] + gun_up

        look_x = cam_x + (-math.cos(angle)) * 100
        look_y = cam_y + (-math.sin(angle)) * 100
        look_z = cam_z

        gluLookAt(cam_x, cam_y, cam_z, look_x, look_y, look_z, 0, 0, 1)  


def idle():
    global bullets, missed_bullets, score, life, game_over

    # Move bullets
    for bullet in bullets:
        bullet['bullet_pos'][0] += bullet['dir'][0] * 10
        bullet['bullet_pos'][1] += bullet['dir'][1] * 10

    b = 0
    while b < len(bullets):
        x, y, z = bullets[b]['bullet_pos']
        if abs(x) >= 600 or abs(y) >= 600:
            bullets.pop(b)
            missed_bullets += 1
        else:
            b += 1

    for e in enemies:
        # Move towards player
        dx = player_pos[0] - e['enemy_pos'][0]
        dy = player_pos[1] - e['enemy_pos'][1]
        dist = math.sqrt(dx**2 + dy**2)
        if dist > 1:
            e['enemy_pos'][0] += dx / dist * 0.05  # Move speed
            e['enemy_pos'][1] += dy / dist * 0.05

        # Pulse effect
        e['scale'] += e['scale_dir']
        if e['scale'] >= 1.2 or e['scale'] <= 0.8:
            e['scale_dir'] *= -1
    
    #hit enemies
    new_enemies = []
    for e in enemies:
        hit = False
        for b in bullets:
            bx, by, bz = b['bullet_pos']
            ex, ey, ez = e['enemy_pos']
            if abs(bx - ex) < 30 and abs(by - ey) < 30 and abs(bz - ez) < 30:
                hit = True
                score += 1
                break
       
        if hit:
            new_enemies.append(spawn_enemy())  
        else:
            new_enemies.append(e)
    enemies[:] = new_enemies

    if missed_bullets == 10:
        game_over = True

    glutPostRedisplay()


def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()  
    glViewport(0, 0, 1000, 700)  

    setupCamera()

    draw_grid(GRID_SIZE)
    # draw_border_walls()

    # game info text
    draw_text(10, 460, f"Player Life Remaining: {life} ")
    draw_text(10, 440, f"Game Score: {score}")
    draw_text(10, 420, f"Player Bullet Missed: {missed_bullets}")

    draw_player()
    draw_bullets()
    for e in enemies:
        draw_enemy(e)

    glutSwapBuffers()


def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)  # Double buffering, RGB color, depth test
    glutInitWindowSize(1000, 600)  # Window size
    glutInitWindowPosition(0, 0)  # Window position
    wind = glutCreateWindow(b"3D OpenGL Intro")  # Create the window
    
    glutDisplayFunc(showScreen)  # Register display function
    glutKeyboardFunc(keyboardListener)  # Register keyboard listener
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)  # Register the idle function to move the bullet automatically

    glutMainLoop()  # Enter the GLUT main loop

if __name__ == "__main__":
    main()
