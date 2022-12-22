import pygame
import numpy as np

# Set the dimensions of the window
width, height = 640, 480

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((width, height))

# Set the camera position and orientation
camera_pos = np.array([5, 5, 5])
camera_target = np.array([0, 0, 0])
camera_up = np.array([0, 1, 0])
SCALE = 40

# Define the vertices of the cube
vertices = [
    # Front face
    [-0.5, -0.5, 0.5],
    [0.5, -0.5, 0.5],
    [0.5, 0.5, 0.5],
    [-0.5, 0.5, 0.5],
    # Back face
    [-0.5, -0.5, -0.5],
    [0.5, -0.5, -0.5],
    [0.5, 0.5, -0.5],
    [-0.5, 0.5, -0.5]
]

# Define the colors of the vertices
colors = [
    (255, 0, 0),  # Front face
    (0, 255, 0),  # Back face
    (0, 0, 255),  # Left face
    (255, 255, 0)  # Right face
]

# Define the indices of the vertices that form each face
indices = [
    [0, 1, 2, 3],  # Front face
    [4, 5, 6, 7],  # Back face
    [3, 2, 6, 7],  # Left face
    [1, 0, 4, 5]   # Right face
]

def look_at(eye, target, up):
    z = (eye - target) / np.linalg.norm(eye - target)
    x = np.cross(up, z) / np.linalg.norm(np.cross(up, z))
    y = np.cross(z, x)
    view_matrix = np.array([
        [x[0], y[0], z[0], 0],
        [x[1], y[1], z[1], 0],
        [x[2], y[2], z[2], 0],
        [-np.dot(x, eye), -np.dot(y, eye), -np.dot(z, eye), 1]
    ])
    return view_matrix

# Set the background color
screen.fill((255, 255, 255))

# Loop until the user closes the window
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill((255, 255, 255))

    # Create the projection matrix
    projection = np.array([
        [SCALE, 0, 0, 0],
        [0, SCALE, 0, 0],
        [0, 0, SCALE, 0],
        [0, 0, 0, 1]
    ])

    # Transform the vertices to screen coordinates
    view_matrix = look_at(camera_pos, camera_target, camera_up)
    t_vertices = []
    for vertex in vertices:
        t_vertex = np.dot(view_matrix, np.append(vertex, 1))
        t_vertices.append(t_vertex[:3])

    transformed_vertices = []
    for vertex in t_vertices:
        transformed_vertex = np.dot(projection, np.append(vertex, 1))
        transformed_vertices.append(transformed_vertex[:2] / transformed_vertex[3])

    # Add an offset to the transformed vertices to move them to the center of the screen
    offset = np.array([width / 2, height / 2])
    transformed_vertices = [vertex + offset for vertex in transformed_vertices]

    # Draw the cube
    for face in indices:
        points = [transformed_vertices[index] for index in face]
        color = colors[indices.index(face)]
        pygame.draw.polygon(screen, color, points)
        print(points)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
