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
import PongAIvAI 
import time
first_run = True
prev_pos = [0,0]
sign2 = 0
y = 0
counter = 0
wall_collide = False
frame_delay = True

def new_ai(paddle_frect, other_paddle_frect, ball_frect, table_size):
    global prev_pos
    global first_run
    global sign2
    global y
    global counter
    global wall_collide
    start_time = time.time()
    # on the first frame, there is no previous position of the ball, so it is set to the middle
    if first_run:
        prev_pos = [table_size[0]/2, table_size[1]/2]
        first_run = False        

    # find the position of the ball's center, and also 
    pos = [ball_frect.pos[0] + ball_frect.size[0]/2, ball_frect.pos[1]+ ball_frect.size[1]/2]
    vel = [pos[0] - prev_pos[0], pos[1] - prev_pos[1]]

    if (vel[0] == 0):
        sign = -1 # so that there is no intersection if vel is 0
    else:
        sign = vel[0]/abs(vel[0])
    # (sign - sign2 == 2  or wall_collide) and 
    if (sign > 0): #abs val or not - maybe for change of directions
        # runs the following code either after it bounces off the opponent's paddle or at the start of a round if it's going towards your paddle
        # only works if your paddle is on the right - the code needs to change based on what side of the board your paddle is on
        if (False): # frame_delay
            frame_delay = False
        else:
            print("run")
            
            final_pos = pos.copy()
            predicted_prev_pos = final_pos
            vel_new = vel.copy()
            prev_vel = vel_new
            counter = 0
            
            while (True):
                # find the x-coordinate when the ball intersects a wall
                if (vel_new[1] > 0):
                    t = (table_size[1] - ball_frect.size[1]/2 - final_pos[1])/vel_new[1]
                    final_pos = [final_pos[0] + t*vel_new[0], table_size[1] - ball_frect.size[1]/2]
                elif (vel_new[1] < 0):
                    t = (0 + ball_frect.size[1]/2 - final_pos[1]) / vel_new[1]
                    final_pos = [final_pos[0] + t*vel_new[0], 0 + ball_frect.size[1]/2]
                vel_new = [vel_new[0], -vel_new[1]]
                end_time = time.time()
                print ((end_time - start_time) * 1000)
                if ((end_time - start_time) * 1000) > 0.1:
                    break
                # check if the point where it intersects a wall is to the right of the paddle, and exit the loop
                if (final_pos[0] >= paddle_frect.pos[0]):
                    break
                #print(final_pos[0], "-----wall------", counter) # print the predicted position for when it intersects with a wall
                predicted_prev_pos = final_pos
                prev_vel = vel_new
                counter += 1
            # use the previous inersection point (before it passed the paddle's position) as the starting position, and intersect the line made from that with the paddle    
            t = (paddle_frect.pos[0] - ball_frect.size[0]/2 - predicted_prev_pos[0])/prev_vel[0]
            y = predicted_prev_pos[1] + t*prev_vel[1]
            #print(y, "-------------------paddle----")
            wall_collide = False
    prev_pos = pos
    sign2 = sign

    # if it intersects with a wall
    if (pos[1] >= table_size[1] - ball_frect.size[1]/2 or pos[1] <= ball_frect.size[1]/2) and sign > 0:
        #print("--wall_pos--", pos[0])
        wall_collide = True
        pass

    if pos[0]+ball_frect.size[0]/2 >= paddle_frect.pos[0] - 2:
        # when it bounces off the right-hand side
        #print(pos[1]-y, "--paddle error--", counter)
        y = table_size[1]/2
        #print("go to center")

    # if the ball goes out of bounds    
    if pos[0]+ball_frect.size[0]/2 >= paddle_frect.pos[0] + 5 or pos[0]-ball_frect.size[0]/2 <= other_paddle_frect.pos[0] - 5:
        y = table_size[1]/2
        #print("go to center")
        prev_pos = [table_size[0]/2, table_size[1]/2]

    if paddle_frect.pos[1] + paddle_frect.size[1]/2 < y:
       return "down"
    else:
       return  "up"


