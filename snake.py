from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from random import randint

# add unique flair --------------------------------
# different food types
# game over if hit cat parade
# parade spawns on other side when hitting wall
# different levels
# bg music
# sprites and textures

window = 0									# glut window
width, height = 500, 500					# window size
field_width, field_height = 50, 50 			# internal resolution

snake = [(20, 20)]							# snake list of (x,y) positions
snakeDir = (1, 0)							# snake movement direction
#newPos = vectAdd(snake[0], snakeDir)		# snake head position after mvmt

food = []									# food list of type (x, y)

interval = 200								# update interval in 200 milliseconds

def refresh2d(width, height, internalWidth, internalHeight):				# draw in 2D (rather, make it look like 2D)
	glViewport(0, 0, width, height)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	glOrtho(0.0, internalWidth, 0.0, internalHeight, 0.0, 1.0)
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()

def drawRect(x, y, width, height):
	glBegin(GL_QUADS)						# start drawing rect
	glVertex2f(x, y)
	glVertex2f(x+width, y)
	glVertex2f(x+width, y+height)
	glVertex2f(x, y+height)
	glEnd()									# done drawing rect

def drawSnake():
	glColor3f(1.0, 1.0, 1.0)				# white snake
	for x, y in snake:
		drawRect(x, y, 1, 1)				# draw pixels in snake at (x, y)

def drawFood():
	glColor3f(0.5, 0.5, 1.0)				# blue food
	for x, y in food:
		drawRect(x, y, 1, 1)				# draw food at (x, y)

def vectAdd((x1, y1), (x2, y2)):
	return (x1+x2, y1+y2)

def update(value):
	# move snake
	snake.insert(0, vectAdd(snake[0], snakeDir))			# insert new pos at start of snake list
	snake.pop()												# remove last element

	# spawn food
	r = randint(0, 20)										# spawn food w/ 5% chance
	if r == 0:
		x, y = randint(0, field_width), randint(0, field_height)	# spawn position
		food.append((x,y))

	# snake eats food
	(hx, hy) = snake[0]							# snake's head position
	for x, y in food:
		if hx == x and hy == y:					# is head at food position?
			snake.append((x, y))				# elongate snake
			food.remove((x, y))					# remove food

	glutTimerFunc(interval, update, 0)			# trigger next update

def keys(*args):
	global snakeDir								# important for when setting to new value

	if args[0] == 'w':
		snakeDir = (0, 1)
	if args[0] == 's':
		snakeDir = (0, -1)
	if args[0] == 'a':
		snakeDir = (-1, 0)
	if args[0] == 'd':
		snakeDir = (1, 0)

def draw():
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)		# clear screen
	glLoadIdentity()										# reset position
	refresh2d(width, height, field_width, field_height)		# set mode to 2D

	# draw stuff here
	drawFood()
	drawSnake()

	glutSwapBuffers()										# important for double buffering

# initialization
glutInit()									# initialize glut
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
glutInitWindowSize(width, height)			# set window size
glutInitWindowPosition(0, 0)				# set window position
window = glutCreateWindow("my first python snake game")		# create window with title
glutDisplayFunc(draw)						# set draw function callback
											# calls draw func ~60 times/sec automatically
glutIdleFunc(draw)							# draw all the time
glutTimerFunc(interval, update, 0)			# trigger next update
glutKeyboardFunc(keys)						# check keys
glutMainLoop()								# start everything
