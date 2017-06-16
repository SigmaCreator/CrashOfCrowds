from structure import *

import OpenGL

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

readFile()

printPeople()

printFrames()

SENS_ROT = 5.0
SENS_OBS = 10.0
SENS_TRANSL = 30.0

rotX, rotY, rotX_ini, rotY_ini = 0, 0, 0, 0
obsX, obsY, obsZ = 200, 200, 200
obsX_ini, obsY_ini, obsZ_ini = 0, 0, 0
fAspect = 1
angle = 44
x_ini, y_ini, bot = 0, 0, 0

countFrame = 0


def watcher():

	glMatrixMode(GL_MODELVIEW)

	glLoadIdentity()

	glTranslatef(-obsX,-obsY,-obsZ)

	glRotatef(rotX,1,0,0)

	glRotatef(rotY,0,1,0)

	gluLookAt(0.0,80.0,200.0, 0.0,0.0,0.0, 0.0,1.0,0.0)


def view():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(angle,fAspect,0.5,50000)
    watcher()


def ground():

    glColor3f(1, 0, 1)
    glLineWidth(3)
    glBegin(GL_LINES)

    for z in range(-2000, 2000, 10):
        glVertex3f(-2000, -0.1, z)
        glVertex3f(2000, -0.1, z)

    for x in range(-2000, 2000, 10):
        glVertex3f(x, -0.1, -2000)
        glVertex3f(x, -0.1, 2000)

    glEnd()
    glLineWidth(1)


def drawScene():

    glClearColor(1.0, 1.0, 1.0, 1.0)

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    view()

    ground()

    glColor3f(0.0, 0.0, 1.0)

    for person in frames[countFrame].people:

        glPushMatrix()

        glTranslatef(person[1][0], 28, person[1][1])

        glRotatef(-90,1,0,0)

        glutWireCone(15,30,20,10)

        glPopMatrix()

    glFlush()


def window(w, h):

    global fAspect

    if h == 0 :
        h = 1

    glViewport(0, 0, w, h)

    fAspect = w / h

    view()


def mouse(button, state, x, y):

    global rotX_ini, rotY_ini, obsX_ini, obsY_ini, obsZ_ini, x_ini, y_ini, bot

    if state == GLUT_DOWN :
        x_ini = x
        y_ini = y
        obsX_ini = obsX
        obsY_ini = obsY
        obsZ_ini = obsZ
        rotX_ini = rotX
        rotY_ini = rotY
        bot = button

    else :
        bot = -1


def manageMovement(x, y):

    global obsX, obsY, obsZ, rotX, rotY

    if bot == GLUT_LEFT_BUTTON :
        deltax = x_ini - x
        deltay = y_ini - y

        rotY = rotY_ini - deltax/SENS_ROT
        rotX = rotX_ini - deltay/SENS_ROT


    elif bot == GLUT_RIGHT_BUTTON :
        deltaz = y_ini - y
        obsZ = obsZ_ini + deltaz/SENS_OBS

    elif bot == GLUT_MIDDLE_BUTTON :
        deltax = x_ini - x
        deltay = y_ini - y

        obsX = obsX_ini + deltax/SENS_TRANSL
        obsY = obsY_ini - deltay/SENS_TRANSL

    watcher()
    glutPostRedisplay()


def framing():

    global countFrame

    countFrame += 1

    if countFrame == Frame.frameCount - 1:
        countFrame = 0

    glutPostRedisplay()


if __name__ == '__main__':

    glutInit()

    glutInitDisplayMode(GLUT_RGB)

    glutInitWindowPosition(5, 5)

    glutInitWindowSize(800,600)

    glutCreateWindow("Teste")

    glEnable(GL_DEPTH_TEST)

    glutDisplayFunc(drawScene)

    glutIdleFunc(framing)

    glutReshapeFunc(window)

    glutMotionFunc(manageMovement)

    glutMouseFunc(mouse)

    glClearColor(1.0, 1.0, 1.0, 1.0)
    glLineWidth(2.0)

    # glutIdleFunc(drawScene)

    # glutKeyboardFunc()

    # glutSpecialFunc()

    glutMainLoop()