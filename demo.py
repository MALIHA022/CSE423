# from OpenGL.GL import *
# from OpenGL.GLUT import *
# from OpenGL.GLU import *
# import math
# import random

# # Camera-related variables
# camera_pos = (0,500,500)

# fovY = 130  # Field of view
# GRID_LENGTH = 100  # Length of grid lines
# GRID_SIZE = 12
# rand_var = 423

# # Game state
# player_pos = [0, 0, 0]
# player_angle = 0
# camera_mode = "third"  # or "first"
# cheat_mode = False
# cheat_vision = False
# game_over = False

# # Bullets: list of dicts with 'pos' and 'dir'
# bullets = []

# # Enemies: list of dicts with 'pos' and 'size_scale'
# enemies = []
# num_enemies = 5

# # Player stats
# life = 5
# missed_bullets = 0
# score = 0

# def draw_text(x, y, text, font = GLUT_BITMAP_HELVETICA_12):
#     glColor3f(1,1,1)
#     glMatrixMode(GL_PROJECTION)
#     glPushMatrix()
#     glLoadIdentity()
    
#     gluOrtho2D(0, 1000, 0, 600)  # left, right, bottom, top

#     glMatrixMode(GL_MODELVIEW)
#     glPushMatrix()
#     glLoadIdentity()
    
#     # Draw text at (x, y) in screen coordinates
#     glRasterPos2f(x, y)
#     for ch in text:
#         glutBitmapCharacter(font, ord(ch))
    
#     glPopMatrix()
#     glMatrixMode(GL_PROJECTION)
#     glPopMatrix()
#     glMatrixMode(GL_MODELVIEW)

# # grid (game floor)
# def draw_grid(GRID_SIZE):
#     glBegin(GL_QUADS)
#     for i in range(GRID_SIZE ):
#         for j in range(GRID_SIZE):
#             if (i + j) % 2 == 0:
#                 glColor3f(1, 1, 1)
#             else:
#                 glColor3f(0.7, 0.5, 0.95)

#             x = (i - GRID_SIZE // 2) * GRID_LENGTH
#             y = (j - GRID_SIZE // 2) * GRID_LENGTH

#             glVertex3f(x, y, 0) #bottom left
#             glVertex3f(x + GRID_LENGTH, y, 0) #bottom right
#             glVertex3f(x + GRID_LENGTH, y + GRID_LENGTH, 0) #top right
#             glVertex3f(x, y + GRID_LENGTH, 0) #top left
#     glEnd()

# def draw_border_walls():
# #     wall_height = 100
# #     glColor3f(0.7, 0.2, 0.2)

# #     # Four sides of the border
# #     for i in range(GRID_SIZE):
# #         for side in ['bottom', 'top', 'left', 'right']:
# #             if side == 'bottom':
# #                 x = (i - GRID_SIZE // 2) * GRID_LENGTH
# #                 y = -(GRID_SIZE // 2) * GRID_LENGTH
# #                 draw_wall(x, y)

# #             elif side == 'top':
# #                 x = (i - GRID_SIZE // 2) * GRID_LENGTH
# #                 y = (GRID_SIZE // 2) * GRID_LENGTH
# #                 draw_wall(x, y)

# #             elif side == 'left':
# #                 x = -(GRID_SIZE // 2) * GRID_LENGTH
# #                 y = (i - GRID_SIZE // 2) * GRID_LENGTH
# #                 draw_wall(x, y, vertical=True)

# #             elif side == 'right':
# #                 x = (GRID_SIZE // 2) * GRID_LENGTH
# #                 y = (i - GRID_SIZE // 2) * GRID_LENGTH
# #                 draw_wall(x, y, vertical=True)


# # def draw_wall(x, y, vertical=False):
# #     z1 = 0
# #     z2 = 100  # wall height

# #     glBegin(GL_QUADS)
# #     if vertical:
# #         # Wall along Y direction
# #         glVertex3f(x, y, z1)
# #         glVertex3f(x + GRID_LENGTH, y, z1)
# #         glVertex3f(x + GRID_LENGTH, y, z2)
# #         glVertex3f(x, y, z2)
# #     else:
# #         # Wall along X direction
# #         glVertex3f(x, y, z1)
# #         glVertex3f(x, y + GRID_LENGTH, z1)
# #         glVertex3f(x, y + GRID_LENGTH, z2)
# #         glVertex3f(x, y, z2)
# #     glEnd()
#     pass



# def draw_player():
#     glPushMatrix()
    
#     # Apply global player transform
#     glTranslatef(*player_pos)
#     glRotatef(player_angle, 0, 0, 1)  # Everything now rotates together

#     # Left foot
#     glColor3f(0, 0, 1)
#     glTranslatef(0,-20,-100)
#     glRotatef(90, 0, 1, 0)
#     glRotatef(90, 0, 1, 0)
#     gluCylinder(gluNewQuadric(), 16, 8, 100, 10, 10) #quadric, base radius, top radius, height, slices, stacks

#     # Right
#     glColor3f(0, 0, 1)
#     glTranslatef(0,-80,0)
#     gluCylinder(gluNewQuadric(), 16, 8, 100, 10, 10) #quadric, base radius, top radius, height, slices, stacks

#     # Body
#     glColor3f(0.4, 0.5, 0)
#     glTranslatef(0, 40, -30)
#     glutSolidCube(80)

#     # Gun
#     glColor3f(0.5, 0.5, 0.5)
#     glTranslatef(0, 0, 40)
#     glTranslatef(30, 0, -90) 
#     glRotatef(90, 0, 1, 0)
#     gluCylinder(gluNewQuadric(), 20, 5, 120, 10, 10) #quadric, base radius, top radius, height, slices, stacks

#     # Left Hand
#     glColor3f(1, 0.7, 0.6)
#     glTranslatef(0, -25, 0)
#     gluCylinder(gluNewQuadric(), 15, 6, 60, 10, 10) #quadric, base radius, top radius, height, slices, stacks

#     # Right Hand
#     glColor3f(1, 0.7, 0.6)
#     glTranslatef(0, 50, 0)
#     gluCylinder(gluNewQuadric(), 15, 6, 60, 10, 10) #quadric, base radius, top radius, height, slices, stacks

#     # Head
#     glColor3f(0, 0, 0)
#     glTranslatef(40,-25, -25)
#     gluSphere(gluNewQuadric(), 30, 10, 10)

#     glPopMatrix()


# def draw_bullets():
#     glColor3f(1, 1, 0)
#     for bullet in bullets:
#         glPushMatrix()
#         glTranslatef(*bullet['pos'])
#         glutSolidCube(15)
#         glPopMatrix()


# def mouseListener(button, state, x, y):
#     global camera_mode

#     if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN and not game_over:
#         # Fire a bullet from gun's tip
#         rad = math.radians(player_angle)
#         dir_x = math.cos(rad)
#         dir_y = math.sin(rad)
#         bullet_start = [
#             player_pos[0] + dir_x * 60,
#             player_pos[1] + dir_y * 60,
#             player_pos[2] + 30
#         ]
#         bullets.append({'pos': bullet_start, 'dir': (dir_x, dir_y)})

#     elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
#         # Toggle camera mode
#         camera_mode = "first" if camera_mode == "third" else "third"

# def keyboardListener(key, x, y):
#     """
#     Handles keyboard inputs for player movement, gun rotation, camera updates, and cheat mode toggles.
#     """
#     global player_pos, player_angle

#     speed = 20
#     angle_step = 10

#     if key == b'w':
#         rad = math.radians(player_angle)
#         player_pos[0] += math.cos(rad) * speed
#         player_pos[1] += math.sin(rad) * speed

#     elif key == b's':
#         rad = math.radians(player_angle)
#         player_pos[0] -= math.cos(rad) * speed
#         player_pos[1] -= math.sin(rad) * speed

#     elif key == b'a':
#         player_angle += angle_step

#     elif key == b'd':
#         player_angle -= angle_step


# def specialKeyListener(key, x, y):
#     """
#     Handles special key inputs (arrow keys) for adjusting the camera angle and height.
#     """
#     global camera_pos
#     x, y, z = camera_pos
#     # Move camera up (UP arrow key)
#     if key == GLUT_KEY_UP:
#         y += 1

#     # Move camera down (DOWN arrow key)
#     if key == GLUT_KEY_DOWN:
#         y-= 1
#     # moving camera left (LEFT arrow key)
#     if key == GLUT_KEY_LEFT:
#         x -= 1  # Small angle decrement for smooth movement

#     # moving camera right (RIGHT arrow key)
#     if key == GLUT_KEY_RIGHT:
#         x += 1  # Small angle increment for smooth movement

#     camera_pos = (x, y, z)

# def setupCamera():
#     """
#     Configures the camera's projection and view settings.
#     Uses a perspective projection and positions the camera to look at the target.
#     """
#     glMatrixMode(GL_PROJECTION)  # Switch to projection matrix mode
#     glLoadIdentity()  # Reset the projection matrix
#     # Set up a perspective projection (field of view, aspect ratio, near clip, far clip)
#     gluPerspective(fovY, 1.25, 0.1, 1500) # Think why aspect ration is 1.25?
#     glMatrixMode(GL_MODELVIEW)  # Switch to model-view matrix mode
#     glLoadIdentity()  # Reset the model-view matrix

#     # Extract camera position and look-at target
#     x, y, z = camera_pos
#     # Position the camera and set its orientation
#     gluLookAt(x, y, z,  # Camera position
#               0, 0, 0,  # Look-at target
#               0, 0, 1)  # Up vector (z-axis)


# def idle():
#     global bullets, missed_bullets

#     # Move bullets
#     for bullet in bullets:
#         bullet['pos'][0] += bullet['dir'][0] * 10
#         bullet['pos'][1] += bullet['dir'][1] * 10

#     # Remove bullets that went too far
#     bullets = [b for b in bullets if abs(b['pos'][0]) < 1000 and abs(b['pos'][1]) < 1000]

#     glutPostRedisplay()


# def showScreen():
#     glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
#     glLoadIdentity()  # Reset modelview matrix
#     glViewport(0, 0, 1000, 700)  # Set viewport size

#     setupCamera()  # Configure camera perspective

#     draw_grid(GRID_SIZE)
#     draw_border_walls()

#     # game info text
#     draw_text(10, 460, f"Player Life Remaining: {life} ")
#     draw_text(10, 440, f"Game Score: {score}")
#     draw_text(10, 420, f"Player Bullet Missed: {missed_bullets}")

#     draw_player()
#     draw_bullets()

#     # Swap buffers for smooth rendering (double buffering)
#     glutSwapBuffers()



# # Main function to set up OpenGL window and loop
# def main():
#     glutInit()
#     glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)  # Double buffering, RGB color, depth test
#     glutInitWindowSize(1000, 600)  # Window size
#     glutInitWindowPosition(0, 0)  # Window position
#     wind = glutCreateWindow(b"3D OpenGL Intro")  # Create the window

#     glutDisplayFunc(showScreen)  # Register display function
#     glutKeyboardFunc(keyboardListener)  # Register keyboard listener
#     glutSpecialFunc(specialKeyListener)
#     glutMouseFunc(mouseListener)
#     glutIdleFunc(idle)  # Register the idle function to move the bullet automatically

#     glutMainLoop()  # Enter the GLUT main loop

# if __name__ == "__main__":
#     main()
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random

# Camera-related variables
camera_pos = (0,500,500)

fovY = 130  # Field of view
GRID_LENGTH = 100  # Length of grid lines
GRID_SIZE = 12
rand_var = 423

# Game state
player_pos = [0, 0, 0]
player_angle = 0
camera_mode = "third"  # or "first"
cheat_mode = False
cheat_vision = False
game_over = False

# Bullets: list of dicts with 'pos' and 'dir'
bullets = []

# Enemies: list of dicts with 'pos' and 'size_scale'
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
    glColor3f(1, 1, 0)
    for bullet in bullets:
        glPushMatrix()
        glTranslatef(*bullet['pos'])
        glutSolidCube(15)
        glPopMatrix()


def mouseListener(button, state, x, y):
    global camera_mode

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN and not game_over:
        # Fire a bullet from gun's tip
        rad = math.radians(player_angle)
        dir_x = math.cos(rad)
        dir_y = math.sin(rad)
        bullet_start = [
            player_pos[0] + dir_x * 60,
            player_pos[1] + dir_y * 60,
            player_pos[2] + 30
        ]
        bullets.append({'pos': bullet_start, 'dir': (dir_x, dir_y)})

    elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        # Toggle camera mode
        camera_mode = "first" if camera_mode == "third" else "third"

def keyboardListener(key, x, y):
    """
    Handles keyboard inputs for player movement, gun rotation, camera updates, and cheat mode toggles.
    """
    global player_pos, player_angle

    speed = 20
    angle_step = 10

    if key == b'w':
        rad = math.radians(player_angle)
        player_pos[0] += math.cos(rad) * speed
        player_pos[1] += math.sin(rad) * speed

    elif key == b's':
        rad = math.radians(player_angle)
        player_pos[0] -= math.cos(rad) * speed
        player_pos[1] -= math.sin(rad) * speed

    elif key == b'a':
        player_angle += angle_step

    elif key == b'd':
        player_angle -= angle_step


def specialKeyListener(key, x, y):
    """
    Handles special key inputs (arrow keys) for adjusting the camera angle and height.
    """
    global camera_pos
    x, y, z = camera_pos
    # Move camera up (UP arrow key)
    if key == GLUT_KEY_UP:
        y += 1

    # Move camera down (DOWN arrow key)
    if key == GLUT_KEY_DOWN:
        y-= 1
    # moving camera left (LEFT arrow key)
    if key == GLUT_KEY_LEFT:
        x -= 1  # Small angle decrement for smooth movement

    # moving camera right (RIGHT arrow key)
    if key == GLUT_KEY_RIGHT:
        x += 1  # Small angle increment for smooth movement

    camera_pos = (x, y, z)

def setupCamera():
    """
    Configures the camera's projection and view settings.
    Uses a perspective projection and positions the camera to look at the target.
    """
    glMatrixMode(GL_PROJECTION)  # Switch to projection matrix mode
    glLoadIdentity()  # Reset the projection matrix
    # Set up a perspective projection (field of view, aspect ratio, near clip, far clip)
    gluPerspective(fovY, 1.25, 0.1, 1500) # Think why aspect ration is 1.25?
    glMatrixMode(GL_MODELVIEW)  # Switch to model-view matrix mode
    glLoadIdentity()  # Reset the model-view matrix

    # Extract camera position and look-at target
    x, y, z = camera_pos
    # Position the camera and set its orientation
    gluLookAt(x, y, z,  # Camera position
              0, 0, 0,  # Look-at target
              0, 0, 1)  # Up vector (z-axis)


def idle():
    global bullets, missed_bullets

    # Move bullets
    for bullet in bullets:
        bullet['pos'][0] += bullet['dir'][0] * 10
        bullet['pos'][1] += bullet['dir'][1] * 10

    # Remove bullets that went too far
    bullets = [b for b in bullets if abs(b['pos'][0]) < 1000 and abs(b['pos'][1]) < 1000]

    glutPostRedisplay()


def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()  # Reset modelview matrix
    glViewport(0, 0, 1000, 700)  # Set viewport size

    setupCamera()  # Configure camera perspective

    draw_grid(GRID_SIZE)
    # draw_border_walls()

    # game info text
    draw_text(10, 460, f"Player Life Remaining: {life} ")
    draw_text(10, 440, f"Game Score: {score}")
    draw_text(10, 420, f"Player Bullet Missed: {missed_bullets}")

    draw_player()
    draw_bullets()

    # Swap buffers for smooth rendering (double buffering)
    glutSwapBuffers()



# Main function to set up OpenGL window and loop
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
