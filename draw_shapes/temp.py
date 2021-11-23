import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
from PIL import Image
from glumpy import glm

vertex_src = """
#version 330 core
layout (location = 0) in vec3 aPos;
layout (location = 1) in vec3 aColor;

out vec3 ourColor;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

void main()
{
    gl_Position = projection * view * model * vec4(aPos, 1.0);
	ourColor = aColor;

}
"""

fragment_src = """
#version 330 core
out vec4 FragColor;
in vec3 ourColor;

void main()
{
	FragColor = vec4(ourColor, 1.0); 
}
"""


def window_resize(window, width, height):
    glViewport(0, 0, width, height)


# initializing glfw library
if not glfw.init():
    raise Exception("glfw can not be initialized!")

# creating the window
window = glfw.create_window(640, 480, "My OpenGL window", None, None)

# check if window was created
if not window:
    glfw.terminate()
    raise Exception("glfw window can not be created!")

# set window's position
glfw.set_window_pos(window, 400, 200)

# set the callback function for window resize
glfw.set_window_size_callback(window, window_resize)

# make the context current
glfw.make_context_current(window)

vertices_1 = [0.5, 0.5, 0.0, 1.0, 0.0, 0.0,  # Face1
              0.5, -0.5, 0.0, 0.0, 1.0, 0.0,
              -0.5, -0.5, 0.0, 0.0, 0.0, 1.0,
              -0.5, 0.5, 0.0, 1.0, 1.0, 0.0,
              0.5, 0.5, 0.0, 1.0, 0.0, 0.0,  # Face2
              0.5, 0.5, 0.5, 0.0, 1.0, 0.0,
              -0.5, 0.5, 0.0, 0.0, 0.0, 1.0,
              -0.5, 0.5, 0.5, 1.0, 1.0, 0.0,
              0.5, 0.5, 0.0, 1.0, 0.0, 0.0,  # Face3
              0.5, 0.5, 0.5, 0.0, 1.0, 0.0,
              0.5, -0.5, 0.0, 0.0, 1.0, 0.0,
              0.5, -0.5, 0.5, 0.0, 1.0, 0.0,
              0.5, -0.5, 0.0, 0.0, 1.0, 0.0,  # Face4
              0.5, -0.5, 0.5, 0.0, 1.0, 0.0,
              -0.5, -0.5, 0.0, 0.0, 1.0, 0.0,
              -0.5, -0.5, 0.5, 0.0, 1.0, 0.0,
              -0.5, -0.5, 0.0, 0.0, 1.0, 0.0,  # Face5
              -0.5, -0.5, 0.5, 0.0, 1.0, 0.0,
              -0.5, 0.5, 0.0, 1.0, 1.0, 0.0,
              -0.5, 0.5, 0.5, 1.0, 1.0, 0.0,
              0.5, 0.5, 0.5, 1.0, 0.0, 0.0,  # Face6
              0.5, -0.5, 0.5, 0.0, 1.0, 0.0,
              -0.5, -0.5, 0.5, 0.0, 0.0, 1.0,
              -0.5, 0.5, 0.5, 1.0, 1.0, 0.0,
              ]

indexes = [0, 1, 3,
           1, 2, 3,
           4, 5, 6,
           5, 6, 7,
           8, 9, 10,
           9, 10, 11,
           12, 13, 14,
           13, 14, 15,
           16, 17, 18,
           17, 18, 19,
           20, 21, 23,
           21, 22, 23
           ]

vertices_1 = np.array(vertices_1, dtype=np.float32)
indexes = np.array(indexes, dtype=np.uint32)

# configure global opengl state
glEnable(GL_DEPTH_TEST)

# Compile shader
shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER), compileShader(fragment_src, GL_FRAGMENT_SHADER))

# Create VAOs and VBOs
VAO = glGenVertexArrays(1)
VBO = glGenBuffers(1)
EBO = glGenBuffers(1)

# Configure First VAO
glBindVertexArray(VAO)  # bind the Vertex Array Object
glBindBuffer(GL_ARRAY_BUFFER, VBO)  # bind and set vertex buffer(s)
glBufferData(GL_ARRAY_BUFFER, vertices_1.nbytes, vertices_1, GL_STATIC_DRAW)  # configure vertex attributes(s)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, indexes.nbytes, indexes, GL_STATIC_DRAW)

# Bind corresponding attributes
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
glEnableVertexAttribArray(0)
glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
glEnableVertexAttribArray(1)

# Select shader
glUseProgram(shader)
glClearColor(0, 0.1, 0.1, 1)

# uncomment this call to draw in wireframe polygons.
# glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

width = 640
height = 480

# the main application loop
while not glfw.window_should_close(window):
    glfw.poll_events()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Set transformation matrices
    timeValue = glfw.get_time()
    model = np.eye(4, dtype=np.float32)  # make sure to initialize matrix to identity matrix first
    view = glm.translation(0, 0, -5)
    glm.rotate(model, timeValue * 8.0, 0, 0, 1)
    glm.rotate(model, -45, 1, 0, 0)
    projection = glm.perspective(45.0, width / float(height), 2.0, 100.0)
    # retrieve the matrix uniform locations
    modelLoc = glGetUniformLocation(shader, "model")
    viewLoc = glGetUniformLocation(shader, "view")
    projectionLoc = glGetUniformLocation(shader, "projection")
    # pass them to the shaders(3 different ways)
    glUniformMatrix4fv(modelLoc, 1, GL_FALSE, model)
    glUniformMatrix4fv(viewLoc, 1, GL_FALSE, view)
    # note: currently we set the projection matrix each frame, but since the projection matrix rarely changes it's often best practice to set it outside the main loop only once.
    glUniformMatrix4fv(projectionLoc, 1, GL_FALSE, projection)

    # Render container
    glBindVertexArray(VAO)
    glDrawElements(GL_TRIANGLES, 36, GL_UNSIGNED_INT, None)

    glfw.swap_buffers(window)

# terminate glfw, free up allocated resources
glfw.terminate()
