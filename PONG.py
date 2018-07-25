# Implementation of classic arcade game Pong

import simplegui
import random
import math
# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
paddle1_pos = HEIGHT
paddle2_pos = HEIGHT
paddle2_vel = 0
paddle1_vel = 0

ball_vel = [0, 0]
# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    ball_vel[0] = random.randrange(160,240)/ 60
    ball_vel[1] = random.randrange(100, 180)/ 60
    if direction == RIGHT:
        ball_vel[0] =  ball_vel[0]
        ball_vel[1] = - ball_vel[1]
    elif direction == LEFT:
        ball_vel[0] = - ball_vel[0]
        ball_vel[1] = - ball_vel[1]


# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints

    spawn_ball(random.choice([RIGHT, LEFT]))
    score1 = 0
    score2 = 0
    paddle1_pos = HEIGHT
    paddle2_pos = HEIGHT
    paddle1_vel = 0
    paddle2_vel = 0

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, paddle1_vel, paddle2_vel, BALL_RADIUS


    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")

    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 1, "Red", 'White')
    if  ball_pos[1] <= BALL_RADIUS:
           ball_vel[1] = - ball_vel[1]
    elif ball_pos[1] >= HEIGHT - BALL_RADIUS:
           ball_vel[1] = - ball_vel [1]
    #Checks wether ball goes into the gutter
    # update paddle's vertical position, keep paddle on the screen
    paddle1_pos += paddle1_vel
    paddle2_pos += paddle2_vel

    if paddle1_pos <= 80:
        paddle1_pos = 80
        paddle1_vel = 0

    elif paddle1_pos >= (720):
        paddle1_pos = 720
        paddle1_vel = 0
    if paddle2_pos <= 80:
        paddle2_pos = 80
        paddle2_vel = 0
    elif paddle2_pos >= (720):
        paddle2_pos = 720
        paddle2_vel = 0

    # draw paddles
    canvas.draw_line([0,(paddle1_pos -PAD_HEIGHT) / 2],[0,(paddle1_pos + PAD_HEIGHT) / 2] , PAD_WIDTH + 7 ,"White")
    canvas.draw_line([WIDTH,(paddle2_pos -PAD_HEIGHT) / 2],[WIDTH,(paddle2_pos + PAD_HEIGHT) / 2] , PAD_WIDTH + 7 ,"White")
    # determine whether paddle and ball collide
    if ball_pos[0] <= (PAD_WIDTH  + BALL_RADIUS):
        if ball_pos[1] < (paddle1_pos - PAD_HEIGHT)/ 2 or ball_pos[1] > (paddle1_pos + PAD_HEIGHT)/ 2:
            score2 += 1
            return spawn_ball(RIGHT)
        else:
            ball_vel[0] = -ball_vel[0] * 1.15
    if ball_pos[0] >= (WIDTH - BALL_RADIUS - PAD_WIDTH):
        if ball_pos[1] < (paddle2_pos - PAD_HEIGHT)/ 2 or ball_pos[1] > (paddle2_pos + PAD_HEIGHT)/ 2:
            score1 += 1
            return spawn_ball(LEFT)
        else:
            ball_vel[0] = -ball_vel[0] * 1.15




    # draw scores

    canvas.draw_text(str(score1), [150,70], 70, "White")
    canvas.draw_text(str(score2), [400,70], 70, "White")

    canvas.draw_circle([300,200], 60, 1, "White")


def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['up']:
        paddle2_vel = -8
    elif key == simplegui.KEY_MAP['down']:
        paddle2_vel = 8
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel = -8
    elif key == simplegui.KEY_MAP['s']:
        paddle1_vel = 8


def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['up'] or simplegui.KEY_MAP['down']:
        paddle2_vel = 0
    if key == simplegui.KEY_MAP['w'] or simplegui.KEY_MAP['s']:
        paddle1_vel = 0


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", new_game, 100)

# start frame
new_game()
frame.start()
