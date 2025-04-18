from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random

# Camera
camera_pos = (0,500,500)

fovY = 120  
GRID_LENGTH = 100  
GRID_SIZE = 14
rand_var = 423

# Game state
player_pos = [0, 0, 0]
player_angle = 0
camera_mode = "third"  
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
min_bound = -GRID_SIZE * GRID_LENGTH // 2
max_bound = GRID_SIZE * GRID_LENGTH // 2

#cheat
cheat = False
gun = False
cheat_rotate = 1.0

def draw_text(x, y, text, font = GLUT_BITMAP_HELVETICA_18): # type: ignore
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
    wall_height = 100
    offset = GRID_LENGTH * GRID_SIZE // 2

    glBegin(GL_QUADS)

    # Bottom wall
    glColor3f(0.01, 0.9, 1)
    glVertex3f(-offset, -offset, 0)
    glVertex3f(offset, -offset, 0)
    glVertex3f(offset, -offset, wall_height)
    glVertex3f(-offset, -offset, wall_height)

    # Top wall
    glColor3f(1, 1, 1)
    glVertex3f(-offset, offset, 0)
    glVertex3f(offset, offset, 0)
    glVertex3f(offset, offset, wall_height)
    glVertex3f(-offset, offset, wall_height)

    # Left wall
    glColor3f(0, 0, 1)
    glVertex3f(-offset, -offset, 0)
    glVertex3f(-offset, offset, 0)
    glVertex3f(-offset, offset, wall_height)
    glVertex3f(-offset, -offset, wall_height)

    # Right wall 
    glColor3f(0.01, 0.9, 0.01)
    glVertex3f(offset, -offset, 0)
    glVertex3f(offset, offset, 0)
    glVertex3f(offset, offset, wall_height)
    glVertex3f(offset, -offset, wall_height)

    glEnd()


def draw_player():
    glPushMatrix()
    glTranslatef(*player_pos)
    glRotatef(player_angle, 0, 0, 1)  

    if game_over:
        glRotatef(90,0,1,0)

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
    
for n in range(num_enemies):
    enemy = spawn_enemy()
    enemy["collide"] = False 
    enemies.append(enemy)

def mouseListener(button, state, x, y):
    global camera_mode

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if not game_over:
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
            print("Player bullet fired!")

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
    global player_pos, player_angle, camera_mode, min_bound, max_bound, life, missed_bullets, score, game_over, cheat, gun

    speed = 20
    angle_step = 5
    if not game_over:
        if key == b'w':  # move forward
            angle = math.radians(player_angle)
            dx = -math.cos(angle) * speed
            dy = -math.sin(angle) * speed

            new_x = player_pos[0] + dx
            new_y = player_pos[1] + dy

            if min_bound <= new_x <= max_bound and min_bound <= new_y <= max_bound:
                player_pos[0] = new_x
                player_pos[1] = new_y

        elif key == b's':  # move backward
            angle = math.radians(player_angle)
            dx = math.cos(angle) * speed
            dy = math.sin(angle) * speed

            new_x = player_pos[0] + dx
            new_y = player_pos[1] + dy

            if min_bound <= new_x <= max_bound and min_bound <= new_y <= max_bound:
                player_pos[0] = new_x
                player_pos[1] = new_y


        elif key == b'a':  #rotate left
            player_angle += angle_step

        elif key == b'd': #rotate right
            player_angle -= angle_step
        
        elif key == b"c": #cheat mode
            cheat = not cheat
            if cheat:
                cheat_mode()
            else:
                gun = False
        
        elif key == b"v": #toggle automatic gun cam
            if camera_mode == "first" and cheat:
                gun = not gun
            if not cheat:
                gun = False
                
    if key == b'r' and game_over: #restart
        bullets.clear()
        enemies.clear()
        cheat = False
        camera_mode = "third"
        for _ in range(num_enemies):
            enemy = spawn_enemy()
            enemy['collide'] = False
            enemies.append(enemy)
            
        score = 0
        missed_bullets = 0
        life = 5
        game_over = False
        player_pos[:] = [0, 0, 0]
        player_angle = 0
        print("Game restarted!")
            
        glutPostRedisplay()

def specialKeyListener(key, x, y):
    """
    Handles special key inputs (arrow keys) for adjusting the camera angle and height.
    """
    global camera_pos
    x, y, z = camera_pos
    if not game_over:
        if key == GLUT_KEY_UP: # Move camera up
            y += 1

        if key == GLUT_KEY_DOWN: # Move camera down 
            y-= 1

        if key == GLUT_KEY_LEFT: # Move camera left
            x -= 1

        if key == GLUT_KEY_RIGHT:  # Move camera right 
            x += 1

    camera_pos = (x, y, z)

lastx,lasty,lastz = 0,0,0
def setupCamera():
    glMatrixMode(GL_PROJECTION)  
    glLoadIdentity()  
    gluPerspective(fovY, 1.25, 0.1, 1500)  #(field of view, aspect ratio, near clip, far clip)
    glMatrixMode(GL_MODELVIEW)  
    glLoadIdentity()

    global lastx,lasty,lastz

    if camera_mode == "third":
        x, y, z = camera_pos
        gluLookAt(x,y,z, 0,0,0, 0,0,1)

    if camera_mode == "first":
        angle = math.radians(player_angle)
        gun_length = 50
        gun_right = 30
        gun_up = 40

        # gun tip position
        cam_x = player_pos[0] + gun_right * math.sin(angle) - math.cos(angle) * gun_length
        cam_y = player_pos[1] - gun_right * math.cos(angle) - math.sin(angle) * gun_length
        cam_z = player_pos[2] + gun_up

        if camera_mode == "first" and cheat and gun:
            look_x = cam_x + (-math.cos(angle)) * 100
            look_y = cam_y + (-math.sin(angle)) * 100
            look_z = cam_z

            lastx = look_x
            lasty = look_y
            lastz = look_z
        elif cheat:
            cam_x = 30
            cam_y = 10
            cam_z = 5

            look_x = lastx
            look_y = lasty
            look_z = lastz

        else:
            look_x = cam_x + (-math.cos(angle)) * 100
            look_y = cam_y + (-math.sin(angle)) * 100
            look_z = cam_z

        gluLookAt(cam_x, cam_y, cam_z, look_x, look_y, look_z, 0, 0, 1)  

def enemy_player_interaction():
    global bullets, missed_bullets, score, life, game_over
    # enemies Move towards player
    for e in enemies:
        dx = player_pos[0] - e['enemy_pos'][0]
        dy = player_pos[1] - e['enemy_pos'][1]
        dist = math.sqrt(dx**2 + dy**2)
        if dist > 1:
            e['enemy_pos'][0] += dx / dist * 0.05  # enemy move speed
            e['enemy_pos'][1] += dy / dist * 0.05

        # Pulse effect
        e['scale'] += e['scale_dir']
        if e['scale'] >= 1.2 or e['scale'] <= 0.8:
            e['scale_dir'] *= -1
    # enemy and player collision
    if not game_over:
        for e in enemies:
            ex, ey, ez = e["enemy_pos"]
            px, py, pz = player_pos
    
            # Collision detection
            collision = abs(px - ex) < 100 and abs(py - ey) < 100 and abs(pz - ez) < 100
    
            if collision:
                if life > 0:
                    life -= 1
                    print(f"Remaining Player life: {life}")
                    enemies.remove(e)     
                    enemies.append(spawn_enemy()) 
                else:
                    game_over = True
                    enemies.clear()  
                break  
def shoot():
    global bullets, missed_bullets, game_over

    # fire bullets
    for bullet in bullets:
        bullet['bullet_pos'][0] += bullet['dir'][0] * 10
        bullet['bullet_pos'][1] += bullet['dir'][1] * 10

    b = 0
    while b < len(bullets):
        x, y, z = bullets[b]['bullet_pos']
        if abs(x) >= 600 or abs(y) >= 600:
            missed_bullets += 1
            print(f"Bullet missed: {missed_bullets}")
            bullets.pop(b)
        else:
            b += 1

    if missed_bullets >= 10 or life == 0:
        game_over = True
        enemies.clear()

def hit_enemy():
    global bullets, missed_bullets, score, life, game_over
    new_enemies = []
    hit_bullets = []

    for e in enemies:
        hit = False
        for b in bullets:
            bx, by, bz = b['bullet_pos']
            ex, ey, ez = e['enemy_pos']
            if abs(bx - ex) < 30 and abs(by - ey) < 30 and abs(bz - ez) < 30:
                hit = True
                score += 1
                hit_bullets.append(b)
                break
       
        if hit:
            new_enemies.append(spawn_enemy())  
        else:
            new_enemies.append(e)
    for b in hit_bullets:
        if b in bullets:
            bullets.remove(b) 
    enemies[:] = new_enemies

cheat_rotation = 0
can_fire = True

def cheat_mode():
    global player_angle, player_pos, score, bullets, enemies, cheat_rotation, can_fire, missed_bullets

    if cheat and not game_over:
        # Rotate player slowly
        rotate_speed = 1
        player_angle = (player_angle + rotate_speed) % 360
        cheat_rotation += rotate_speed

        if cheat_rotation >= 30:
            cheat_rotation = 0
            can_fire = True

        rad = math.radians(player_angle)
        dir_x = -math.cos(rad)
        dir_y = -math.sin(rad)

        # Gun tip position
        gun_length = 140
        gun_right = 50
        gun_up = 10

        bx = player_pos[0] + gun_right * math.sin(rad) + dir_x * gun_length
        by = player_pos[1] - gun_right * math.cos(rad) + dir_y * gun_length
        bz = player_pos[2] + gun_up

        if can_fire:
            for e in enemies:
                ex, ey, ez = e["enemy_pos"]
                dx, dy = ex - bx, ey - by
                dist_xy = math.sqrt(dx ** 2 + dy ** 2)
                if dist_xy == 0:
                    continue
                dot = (dx * dir_x + dy * dir_y) / dist_xy

                if dot > 0.998:
                    dz = ez - bz
                    dist_total = math.sqrt(dx ** 2 + dy ** 2 + dz ** 2)
                    dir_to_enemy = [dx / dist_total, dy / dist_total, dz / dist_total]

                    # Fire bullet
                    bullets.append({
                        'bullet_pos': [bx, by, bz],
                        'dir': dir_to_enemy,
                        'cheat': True 
                    })

                    can_fire = False
                    print("Cheat mode bullet fired!")
                    break

    glutPostRedisplay()





def idle():
    shoot()
    hit_enemy()
    enemy_player_interaction()
    cheat_mode()
    glutPostRedisplay()


def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()  
    glViewport(0, 0, 1000, 700)  

    setupCamera()

    draw_grid(GRID_SIZE)
    draw_border_walls()

    # game info text
    if not game_over:
        draw_text(10, 460, f"Player Life Remaining: {life} ")
        draw_text(10, 440, f"Game Score: {score}")
        draw_text(10, 420, f"Player Bullet Missed: {missed_bullets}")
    else:
        draw_text(10, 460, f"Game is Over. Your score is {score}.")
        draw_text(10, 440, f'Press "R" to RESTART the Game.')

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