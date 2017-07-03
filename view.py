from structure import *

import OpenGL
import math
import time as tm

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

GRD_RADIUS=2500
SENS_ROT = 5.0
SENS_OBS = 10.0
SENS_TRANSL = 30.0
FILES = ['Paths_D.txt',
	 'jp1.txt',
	 'jp2.txt']

rotX, rotY, rotX_ini, rotY_ini = 0, 0, 0, 0
obsX, obsY, obsZ = 200, 200, 200
obsX_ini, obsY_ini, obsZ_ini = 0, 0, 0
fAspect = 1
angle = 75
x_ini, y_ini, bot = 0, 0, 0

countFrame = 0

cells = []

def watcher():

	glMatrixMode(GL_MODELVIEW)

	glLoadIdentity()

	glTranslatef(-obsX,-obsY,-obsZ)

	glRotatef(rotX,1,0,0)

	glRotatef(rotY,0,1,0)

	gluLookAt(0.0,80.0,0.0, GRD_RADIUS/2,0.0,GRD_RADIUS/2, 0.0,1.0,0.0)


def view():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(angle,fAspect,0.5,50000)
    watcher()


def ground():

    glColor3f(1, 0, 1)
    glLineWidth(3)
    glBegin(GL_LINES)

    for z in range(0, GRD_RADIUS, 100):
        glVertex3f(0, -0.1, z)
        glVertex3f(GRD_RADIUS, -0.1, z)
	

    for x in range(0, GRD_RADIUS, 100):
        glVertex3f(x, -0.1, 0)
        glVertex3f(x, -0.1, GRD_RADIUS)

    glEnd()
    for x in range(0, GRD_RADIUS, 50):
	line = []
	for z in range(0, GRD_RADIUS, 50):
		name = 'cell'+str(x)+''+str(z)
		cell = Cell(x,z,name)
		line.append(cell)
		glPushMatrix()
		glTranslatef(x, 0, z)
		glRotatef(-90,1,0,0)
		glutWireCone(5, 5, 20, 10)
		glPopMatrix()
	cells.append(line)
	

    
    glLineWidth(1)


def drawScene():

    glClearColor(1.0, 1.0, 1.0, 1.0)

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    view()

    ground()

    
    takencells = []
    for person in frames[countFrame].people:
	x = person[1][0]
	y = person[1][1]
	p = people[person[0]]	

	cell = getCell(x, y)
	cell.people.append(person)
	p.cell = cell
	takencells.append(cell)

    for person in frames[countFrame].people:

        glPushMatrix()
	x = person[1][0]
	y = person[1][1]
	p = people[person[0]]
        glTranslatef(x, 0, y)

        glRotatef(-90,1,0,0)
	
	glColor3f(0.0, 0.0, 1.0)
	for cell in getCoI(p.cell):
		for q in cell.people:
			if person[0]!=q[0]:
				if euc_dist((x,y), q[1]) <= 20:
					glColor3f(1, 0, 0)
					break

        glutWireCone(10,30,20,10)

        glPopMatrix()

    for cell in takencells:	
	cell.reset()

    glFlush()

	
    #tm.sleep(0.05)

def getCoI(cell):
	coi = [cell]
	x = cell.x/50
	y = cell.y/50
	x0 = x-1
	x1 = x+1
	y0 = y-1
	y1 = y+1
	if x0>=0:
		coi.append(cells[x0][y])
		if y0>=0:
			coi.append(cells[x0][y0])
		if y1<len(cells):
			coi.append(cells[x0][y1])
	if x1<len(cells):
		coi.append(cells[x1][y])
		if y0>=0:
			coi.append(cells[x1][y0])
		if y1<len(cells):
			coi.append(cells[x1][y1])
	if y0>=0:
		coi.append(cells[x][y0])
	if y<len(cells):
		coi.append(cells[x][y1])
	return coi

def getCell(x, y):
	xcell = int(x//50)
	ycell = int(y//50)
	if (x%50)/50 >= .5:
		xcell = xcell + 1
	if (y%50)/50 >= .5:
		ycell = ycell + 1
	cell = cells[xcell][ycell]
	xcell = cell.x
	ycell = cell.y
	glPushMatrix()
	glColor3f(1,1,0)
	glTranslatef(xcell, 0, ycell)
	glRotatef(-90,1,0,0)
	glutWireCone(5, 5, 20, 10)
	glColor3f(0,0,1)
	glPopMatrix()
	return cell

def euc_dist(p1, p2):
	x1 = p1[0]
	x2 = p2[0]
	y1 = p1[1]
	y2 = p2[1]
	dist = math.sqrt((x2-x1)**2+(y2-y1)**2)
	return dist


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
	for path in FILES:
		readFile(path)

	printPeople()

	printFrames()

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
