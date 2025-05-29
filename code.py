Web VPython 3.2
scene = canvas()
pos_graph = graph(title="Ball Heights", xtitle="Time", ytitle = "Height")
vel_graph = graph(title="Ball Velocities", xtitle="Time", ytitle = "Velocity")
L=3
initial_angle=-pi/3
axis_pos=3
ball_radius=0.3

num_balls=2
num_starting_balls=1
#def setInitialAngle(x):
#    global initial_angle
#    initial_angle=-pi * x/180
#def setNumBalls(x):
#    global num_balls
#    num_balls=x
#def setNumBallsStarting(x):
#    global num_starting_balls
#    global num_balls
#    num_starting_balls=min(x, num_balls)
#initial_angle_input = slider( bind=setInitialAngle, min=0, max=90, value=60, step=1)
#num_balls_input = slider( bind=setNumBalls, min=1, max=10, value=1, step=1)
#num_balls_starting_input = slider( bind=setNumBallsStarting, min=1, max=10, value=1, step=1)

balls=[]
rods=[]
pos_curves=[]
vel_curves=[]
balls.append(sphere(pos=vec(L * sin(initial_angle),axis_pos-L * cos(initial_angle),0), radius=ball_radius, color=color.cyan))
rods.append(cylinder(pos=balls[0].pos, axis=vec(0,axis_pos,0)-balls[0].pos, radius=0.03, color=color.red))
for i in range(1,num_balls):
    balls.append(sphere(pos=vec(2*i*ball_radius,axis_pos-L,0), radius=ball_radius, color=color.cyan))
    rods.append(cylinder(pos=balls[i].pos, axis=vec(2*i*ball_radius,axis_pos,0)-balls[i].pos, radius=0.03, color=color.red))

g = 9.81
for i in range(num_balls):
    balls[i].acc=0
    balls[i].vel=0
    balls[i].theta=0
    curr_color=(vector.random()+vec(1,1,1))/2
    pos_curves.append(gcurve(graph=pos_graph, color=curr_color, label="Ball "+str(i)))
    vel_curves.append(gcurve(graph=vel_graph, color=curr_color, label="Ball "+str(i)))
    
balls[0].theta=initial_angle
t = 0
dt = 1/200
program_rate = 100


def collide(i, j):
    balls[j].acc=balls[i].acc
    balls[j].vel=balls[i].vel
    balls[i].acc=0
    balls[i].vel=0
while (True):
    rate(program_rate)
    for i in range(num_balls):
        ball=balls[i]
        ball.acc=-g * sin(ball.theta)/L
        ball.vel+=ball.acc*dt
        ball.theta+=ball.vel*dt
        ball.pos=vec(L * sin(ball.theta)+2*i*ball_radius,axis_pos-L * cos(ball.theta),0)
        rods[i].pos=ball.pos
        rods[i].axis=vec(2*i*ball_radius,axis_pos,0)-ball.pos
        for j in range(0, num_balls):
            if ball.vel.mag!=0:
                if (j>i and ball.pos.x>=balls[j].pos.x-2*ball_radius):
                    collide(i,j)
                else if (j<i and ball.pos.x<=balls[j].pos.x+2*ball_radius):
                    collide(i,j)
#    print(ball.acc + " " + ball.vel + " " + theta)
        pos_curves[i].plot(t, ball.pos.y)
        vel_curves[i].plot(t, ball.vel)
    t+=dt
    
