import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import sys
import math

cam_pos = [0.0, -5.0, 3.0]
cam_front = [0.0, 1.0, -0.3]
cam_up = [0.0, 0.0, 1.0]
yaw = 90.0
pitch = -20.0
last_x = 400
last_y = 300
first_mouse = True
move_speed = 5.0
mouse_sensitivity = 0.1

grid_size = 8.0
divisions = 80
fabric_vertices = []  # list of [x, y, z] positions

ball_pos = [0.0, 0.0]  # x, y
ball_radius = 0.4
dip_strength = 1.0
dip_falloff = 0.6
circle_radius = 2.0  # radius of ball's circular motion
circle_speed = 1.0   # speed of circular motion


def normalize(v):
    length = math.sqrt(sum([x*x for x in v]))
    if length == 0: return [0,0,0]
    return [x / length for x in v]

def cross(a, b):
    return [a[1]*b[2] - a[2]*b[1],
            a[2]*b[0] - a[0]*b[2],
            a[0]*b[1] - a[1]*b[0]]

def vec_add(a, b):
    return [a[i] + b[i] for i in range(3)]

def vec_sub(a, b):
    return [a[i] - b[i] for i in range(3)]

def vec_scale(v, s):
    return [v[i] * s for i in range(3)]

def update_camera_vectors():
    global cam_front, cam_up
    front_x = math.cos(math.radians(yaw)) * math.cos(math.radians(pitch))
    front_y = math.sin(math.radians(yaw)) * math.cos(math.radians(pitch))
    front_z = math.sin(math.radians(pitch))
    cam_front[:] = normalize([front_x, front_y, front_z])
    right = normalize(cross(cam_front, [0.0, 0.0, 1.0]))
    cam_up[:] = normalize(cross(right, cam_front))

def cursor_pos_callback(window, xpos, ypos):
    global yaw, pitch, last_x, last_y, first_mouse
    if first_mouse:
        last_x = xpos
        last_y = ypos
        first_mouse = False
    xoffset = xpos - last_x
    yoffset = last_y - ypos
    last_x = xpos
    last_y = ypos
    xoffset *= mouse_sensitivity
    yoffset *= mouse_sensitivity
    yaw -= xoffset
    pitch += yoffset
    pitch = max(-89.0, min(89.0, pitch))
    update_camera_vectors()

def init_fabric():
    global fabric_vertices
    step = grid_size / divisions
    half = grid_size / 2.0
    fabric_vertices = []
    for i in range(divisions + 1):
        row = []
        x = -half + i * step
        for j in range(divisions + 1):
            y = -half + j * step
            z = 0.0
            row.append([x, y, z])
        fabric_vertices.append(row)
    return fabric_vertices

def apply_ball_dip():
    for i in range(divisions + 1):
        for j in range(divisions + 1):
            x, y, _ = fabric_vertices[i][j]
            dx = x - ball_pos[0]
            dy = y - ball_pos[1]
            dist_sq = dx*dx + dy*dy
            z = -dip_strength * math.exp(-dist_sq * dip_falloff)
            fabric_vertices[i][j][2] = z

def draw_fabric():
    glColor3f(0.5, 0.5, 0.5)
    glBegin(GL_LINES)
    for i in range(divisions + 1):
        for j in range(divisions):
            glVertex3f(*fabric_vertices[i][j])
            glVertex3f(*fabric_vertices[i][j+1])
    for j in range(divisions + 1):
        for i in range(divisions):
            glVertex3f(*fabric_vertices[i][j])
            glVertex3f(*fabric_vertices[i+1][j])
    glEnd()

def draw_ball():
    sphere_z = ball_radius + fabric_vertices[divisions//2][divisions//2][2]
    glPushMatrix()
    glTranslatef(ball_pos[0], ball_pos[1], sphere_z)
    glColor3f(1.0, 0.0, 0.0)  # red
    quad = gluNewQuadric()
    gluSphere(quad, ball_radius, 32, 32)
    gluDeleteQuadric(quad)
    glPopMatrix()

def main():
    global cam_pos, cam_front, cam_up, ball_pos
    if not glfw.init():
        sys.exit(-1)
    window = glfw.create_window(800, 600, "Space fabric", None, None)
    if not window:
        glfw.terminate()
        sys.exit(-1)
    glfw.make_context_current(window)
    glfw.set_cursor_pos_callback(window, cursor_pos_callback)
    glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)
    glEnable(GL_DEPTH_TEST)
    update_camera_vectors()
    init_fabric()
    last_time = glfw.get_time()
    
    while not glfw.window_should_close(window):
        current_time = glfw.get_time()
        delta_time = current_time - last_time
        last_time = current_time

        # Move camera
        cam_right = normalize(cross(cam_front, cam_up))
        if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
            cam_pos = vec_add(cam_pos, vec_scale(cam_front, move_speed * delta_time))
        if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
            cam_pos = vec_sub(cam_pos, vec_scale(cam_front, move_speed * delta_time))
        if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
            cam_pos = vec_sub(cam_pos, vec_scale(cam_right, move_speed * delta_time))
        if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
            cam_pos = vec_add(cam_pos, vec_scale(cam_right, move_speed * delta_time))
        if glfw.get_key(window, glfw.KEY_Q) == glfw.PRESS:
            cam_pos[2] -= move_speed * delta_time
        if glfw.get_key(window, glfw.KEY_E) == glfw.PRESS:
            cam_pos[2] += move_speed * delta_time

        ball_pos[0] = circle_radius * math.cos(circle_speed * current_time)
        ball_pos[1] = circle_radius * math.sin(circle_speed * current_time)

        # Update fabric
        apply_ball_dip()

        # Clear screen
        glClearColor(0.0, 0.0, 0.05, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Projection
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, 800/600, 0.1, 100.0)

        # View
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        center = vec_add(cam_pos, cam_front)
        gluLookAt(cam_pos[0], cam_pos[1], cam_pos[2],
                  center[0], center[1], center[2],
                  cam_up[0], cam_up[1], cam_up[2])

        draw_fabric()
        draw_ball()

        glfw.swap_buffers(window)
        glfw.poll_events()

        if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
            glfw.set_window_should_close(window, True)

    glfw.terminate()

if __name__ == "__main__":
    main()
