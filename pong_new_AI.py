'''return "up" or "down", depending on which way the paddle should go to
    align its centre with the centre of the ball, assuming the ball will
    not be moving

    Arguments:
    paddle_frect: a rectangle representing the coordinates of the paddle
                  paddle_frect.pos[0], paddle_frect.pos[1] is the top-left
                  corner of the rectangle.
                  paddle_frect.size[0], paddle_frect.size[1] are the dimensions
                  of the paddle along the x and y axis, respectively

    other_paddle_frect:
                  a rectangle representing the opponent paddle. It is formatted
                  in the same way as paddle_frect
    ball_frect:   a rectangle representing the ball. It is formatted in the
                  same way as paddle_frect
    table_size:   table_size[0], table_size[1] are the dimensions of the table,
                  along the x and the y axis respectively

    The coordinates look as follows:

     0             x
     |------------->
     |
     |
     |
 y   v
    '''


'''
TO DO:
- loop through values between -0.5 and 0.5 at some increment (idk if it should be constant or non-constant) and find the value where when the paddle is diplaced that fraction of its length, it gives the max distance from the opponent's paddle
        - exit the loop before timed out and use the one with the max distance

- if the opponent's paddle stops moving, calculate everything early, based on what would happen if the paddle stayed still
        - also maybe do this anyways if the other paddle is moving

- check that the thing where it doesn't go all the way to the edge isn't risky

- try it where it always hits the ball near the corner of the paddle, and then after see what happens if you try and hit it with the side of the paddle (make the x-coordinate of intersection further back)

In general:
- hunt bugs
- made code more efficient to allow more computation before time-out

'''


import time
import PongAIvAI
import math

first_run = True
prev_pos = [0, 0]
sign2 = 0
y = 0
counter = 0

def new_ai(paddle_frect, other_paddle_frect, ball_frect, table_size):
    global prev_pos
    global first_run
    global sign2
    global y
    global counter

    broken = False

    # on the first frame, there is no previous position of the ball, so it is set to the middle
    if first_run:
        prev_pos = [table_size[0]/2, table_size[1]/2]
        first_run = False

    start_time = time.time()

    # find the position of the ball's center, and also
    pos = [ball_frect.pos[0] + ball_frect.size[0] / 2, ball_frect.pos[1] + ball_frect.size[1]/2]
    vel = [pos[0] - prev_pos[0], pos[1] - prev_pos[1]]

    if (vel[0] == 0):
        sign = -1  # so that there is no intersection if vel is 0
    else:
        sign = vel[0]/abs(vel[0])
    # (sign - sign2 == 2  or wall_collide) and

    if paddle_frect.pos[0] > table_size[0]/2:
        your_side = "right"
    else:
        your_side = "left"

    if ((your_side == "right" and sign > 0) or (your_side == "left" and sign < 0)):
        # runs the following code either after it bounces off the opponent's paddle or at the start of a round if it's going towards your paddle
        # only works if your paddle is on the right - the code needs to change based on what side of the board your paddle is on
        
        final_pos = pos.copy()
        predicted_prev_pos = final_pos
        vel_new = vel.copy()
        prev_vel = vel_new
        counter = 0

        while (True):
            # find the x-coordinate when the ball intersects a wall
            if (vel_new[1] > 0):
                t = (table_size[1] - ball_frect.size[1] / 2 - final_pos[1])/vel_new[1]
                final_pos = [final_pos[0] + t*vel_new[0], table_size[1] - ball_frect.size[1]/2]
            elif (vel_new[1] < 0):
                t = (0 + ball_frect.size[1]/2 - final_pos[1]) / vel_new[1]
                final_pos = [final_pos[0] + t * vel_new[0], 0 + ball_frect.size[1]/2]
            vel_new = [vel_new[0], -vel_new[1]]

            end_time = time.time()
            if ((end_time - start_time) * 1000) > 0.05:
                broken = True
                break

            # check if the point where it intersects a wall is to the right of the paddle, and exit the loop
            if ((your_side == "right" and final_pos[0] >= paddle_frect.pos[0]) or (your_side == "left" and final_pos[0] <= paddle_frect.pos[0] + paddle_frect.size[0])):
                break
            #print(final_pos[0], "-----wall------", counter) # print the predicted position for when it intersects with a wall
            predicted_prev_pos = final_pos
            prev_vel = vel_new
            counter += 1
        # use the previous inersection point (before it passed the paddle's position) as the starting position, and intersect the line made from that with the paddle
        # x = x0 + t*v_x  --> solve for t to get: t = (x-x0)/v_x
        if (your_side == "right"):
            t = (paddle_frect.pos[0] - (predicted_prev_pos[0] + ball_frect.size[0] / 2))/prev_vel[0] # double check
        else:
            t = (paddle_frect.pos[0] + paddle_frect.size[0] - (predicted_prev_pos[0] - ball_frect.size[0] / 2))/prev_vel[0] # double check
            
        if (not broken):
            y = predicted_prev_pos[1] + t*prev_vel[1]
    prev_pos = pos
    sign2 = sign
    
    # if it intersects with a wall -- for debugging
    if (pos[1] >= table_size[1] - ball_frect.size[1]/2 or pos[1] <= ball_frect.size[1]/2) and sign > 0:
        pass

    # when it bounces off your side  (also runs 2 pixels before this happens)
    if (your_side == "right" and pos[0] + ball_frect.size[0]/2 >= paddle_frect.pos[0] - 2) or (your_side == "left" and pos[0] - ball_frect.size[0]/2 <= paddle_frect.pos[0] + paddle_frect.size[0] + 2):
        y = table_size[1]/2

    # if the ball goes out of bounds
    # score if it passes the entire width of the paddle, ----      pos[0] >= paddle_frect.pos[0] + ball_frect.size[0] or pos[0] <= other_paddle_frect.pos[0]
    if (your_side == "right"):
        if pos[0]+ball_frect.size[0]/2 >= paddle_frect.pos[0] + other_paddle_frect.size[0] + 5 or pos[0]-ball_frect.size[0]/2 <= other_paddle_frect.pos[0] + other_paddle_frect.size[0] - 5:
            y = table_size[1]/2
            prev_pos = [table_size[0]/2, table_size[1]/2]
    else:
        if pos[0]-ball_frect.size[0]/2 <= paddle_frect.pos[0] + paddle_frect.size[0] - 5 or pos[0] + ball_frect.size[0]/2 >= other_paddle_frect.pos[0] + 5:
            y = table_size[1]/2
            prev_pos = [table_size[0]/2, table_size[1]/2]
    
    
    if paddle_frect.pos[1] <= ball_frect.size[1] - 3: # top of paddle above top boundary # changed to 3 from 1
        return "down"

    if paddle_frect.pos[1] + paddle_frect.size[1] >= table_size[1] - ball_frect.size[1] + 3:
        return "up"
    
# at the start of the run, y got updated when the ball was moving away from the paddle
# also it went to the correct position near the edge but moved away right before the ball came  --- check more so that this doesn't happen again - maybe add more padding

    if paddle_frect.pos[1] + paddle_frect.size[1]/2 < y: # want to go up
        return "down"
    else:
        return "up"
