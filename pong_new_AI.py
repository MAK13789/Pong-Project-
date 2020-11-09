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

intersected = False
prev_sign = 0

def new_ai(paddle_frect, other_paddle_frect, ball_frect, table_size):
	global intersected
	global prev_sign
	print("djslfje")
	print(ball_frect.speed[0])
	#x_vel = ball_frect.speed[0]
	sign = x_vel/abs(x_vel)
	if (sign - prev_sign == 2):
		print("intersected")
	

	prev_sign = sign
	
	'''
	if intersected:
		print("intersected")
		intersected = False
	elif intersect(other_paddle_frect, ball_frect):
		intersected = True
	'''
   # if opponent's paddle intersects with the ball, then do this:

# call intersect_line
# check if it's farther than the paddle position - if it is, use the previous line, and intersect it with the paddle x-pos to find the y-pos

def intersect_line(vel, init_pos, table_size):
	# pos = init_pos + t*vel
	# t = (pos[1] - init_pos[1])/vel[1]
	# if vel[1] > 0, find pos[0] when pos[1] = table_size[1]
	if (vel[1] > 0):
		t = (table_size[1] - init_pos[1])/vel[1]
		return init_pos[0] + t*vel[0]
	if (vel[1] < 0):
		t = (0 - init_pos[1]) / vel[1]
		return init_pos[0] + t*vel[0]
	# if vel[1] = 0 - --   save for lalter
	# if vel[1] < 0, find pos[0] when pos[1] = 0

def intersect_paddle(vel, init_pos):
	t = (paddle_frect.pos[0] - init_pos[0])/vel[0]
	return init_pos[1] + t*vel[1]

def reflect_line(vel):
	return [vel[0], -vel[1]]

def intersect(other_paddle_frect, ball_frect):
        # two rectangles intersect iff both x and y projections intersect
        for i in range(2):
            if ball_frect.pos[i] < other_paddle_frect.pos[i]: # projection of self begins to the left  MAYBE ADD SOME CONSTANT
                if other_paddle_frect.pos[i] >= ball_frect.pos[i] + ball_frect.size[i]:
                    return 0
            elif ball_frect.pos[i] > other_paddle_frect.pos[i]:
                if ball_frect.pos[i] >= other_paddle_frect.pos[i] + other_paddle_frect.size[i]:
                    return 0
        return 1#ball_frect.size > 0 and other_paddle_frect.size > 0

'''
    def get_angle(self, y):
        center = self.frect.pos[1]+self.size[1]/2
        rel_dist_from_c = ((y-center)/self.size[1])
        rel_dist_from_c = min(0.5, rel_dist_from_c)
        rel_dist_from_c = max(-0.5, rel_dist_from_c)
        sign = 1-2*self.facing

        return sign*rel_dist_from_c*self.max_angle*math.pi/180




            if self.frect.intersect(paddle.frect):
                if (paddle.facing == 1 and self.get_center()[0] < paddle.frect.pos[0] + paddle.frect.size[0]/2) or \
                (paddle.facing == 0 and self.get_center()[0] > paddle.frect.pos[0] + paddle.frect.size[0]/2):
                    continue

                c = 0

                while self.frect.intersect(paddle.frect) and not self.frect.get_rect().colliderect(walls_Rects[0]) and not self.frect.get_rect().colliderect(walls_Rects[1]):
                    self.frect.move_ip(-.1*self.speed[0], -.1*self.speed[1], move_factor)

                    c += 1
                theta = paddle.get_angle(self.frect.pos[1]+.5*self.frect.size[1])


                v = self.speed

                v = [math.cos(theta)*v[0]-math.sin(theta)*v[1],
                             math.sin(theta)*v[0]+math.cos(theta)*v[1]]

                v[0] = -v[0]

                v = [math.cos(-theta)*v[0]-math.sin(-theta)*v[1],
                              math.cos(-theta)*v[1]+math.sin(-theta)*v[0]]


                # Bona fide hack: enforce a lower bound on horizontal speed and disallow back reflection
                if  v[0]*(2*paddle.facing-1) < 1: # ball is not traveling (a) away from paddle (b) at a sufficient speed
                    v[1] = (v[1]/abs(v[1]))*math.sqrt(v[0]**2 + v[1]**2 - 1) # transform y velocity so as to maintain the speed
                    v[0] = (2*paddle.facing-1) # note that minimal horiz speed will be lower than we're used to, where it was 0.95 prior to the  increase by 1.2

                #a bit hacky, prevent multiple bounces from accelerating
                #the ball too much
                if not paddle is self.prev_bounce:
                    self.speed = (v[0]*self.paddle_bounce, v[1]*self.paddle_bounce)
                else:
                    self.speed = (v[0], v[1])
                self.prev_bounce = paddle


                while c > 0 or self.frect.intersect(paddle.frect):

                    self.frect.move_ip(.1*self.speed[0], .1*self.speed[1], move_factor)

                    c -= 1

                moved = 1
'''