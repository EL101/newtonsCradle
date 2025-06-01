Web VPython 3.2
scene = canvas()
pos_graph = graph(title="Ball Heights", xtitle="Time", ytitle = "Height")
vel_graph = graph(title="Ball Velocities", xtitle="Time", ytitle = "Velocity")
L=3
initial_angle=-pi/3
axis_pos=3
ball_radius=0.3

num_balls=7
num_starting_balls=4
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
for i in range(num_starting_balls):
    balls.append(sphere(pos=vec(L * sin(initial_angle)+2*i*ball_radius,axis_pos-L * cos(initial_angle),0), radius=ball_radius, color=color.cyan))
    rods.append(cylinder(pos=balls[i].pos, axis=vec(2*i*ball_radius,axis_pos,0)-balls[i].pos, radius=0.03, color=color.red))
for i in range(num_starting_balls,num_balls):
    balls.append(sphere(pos=vec(2*i*ball_radius,axis_pos-L,0), radius=ball_radius, color=color.cyan))
    rods.append(cylinder(pos=balls[i].pos, axis=vec(0,L,0), radius=0.03, color=color.red))

g = 9.81
for i in range(num_balls):
    balls[i].acc=0
    balls[i].vel=0
    balls[i].theta=0
    balls[i].prev_vel=0
    balls[i].prev_theta=0
    curr_color=(vector.random()+vec(1,1,1))/2
    pos_curves.append(gcurve(graph=pos_graph, color=curr_color, label="Ball "+str(i)))
    vel_curves.append(gcurve(graph=vel_graph, color=curr_color, label="Ball "+str(i)))
    
for i in range(num_starting_balls):
    balls[i].theta=initial_angle
t = 0
dt = 1/1000
program_rate = 2000

def setRt(x):
    global program_rate
    program_rate = x.value

def collide(i, j):
    overlap=-balls[i].theta
    dir=balls[i].vel/abs(balls[i].vel)
    balls[j].vel=sqrt(balls[i].vel*balls[i].vel+2*balls[i].acc*overlap)*dir
#    print(balls[j].vel)
    balls[i].vel=0
    balls[i].theta=0

buffer=1E-3
slider_title = wtext(text = "Set Rate:")
rateSlider = slider(bind = setRt, min=10, max=10000, value=program_rate, step=10)

run=True
def pause():
    global run
    run=!run
    if (!run):
        pause_button.background=color.green
    else:
        pause_button.background=color.red
pause_button=button(bind=pause, text='Pause/Unpause', background=color.red)

display_graph=True
graph_spacing=10
def change_display_graph():
    global display_graph
    display_graph=!display_graph
    if (!display_graph):
        display_graph_button.background=color.green
    else:
        display_graph_button.background=color.red
display_graph_button=button(bind=change_display_graph, text='Undisplay/Display', background=color.red)
while (True):
    rate(program_rate)
    if !run:
        continue
    moving=num_balls
    for j in range(num_balls):
        if balls[j].theta==0 and balls[j].vel==0:
            moving-=1
    if (moving!=num_starting_balls):
        print(moving)
        for ball in balls:
            print(ball.prev_theta, ball.prev_vel, ball.theta, ball.vel)
        run=False
        break
    for i in range(num_balls):  
        ball=balls[i]
        if ball.vel==0 and ball.theta==0:
            continue
        
        j=i+1
        collided=False
        if j<num_balls and ball.vel>0:
            if (ball.pos.x>balls[j].pos.x-2*ball_radius+buffer):
#                print("Forward:",i,j,ball.pos.x,balls[j].pos.x, ball.vel)
                collide(i,j)
                collided=True
#                    print(i,j,ball.pos.x,balls[j].pos.x)
                
        j=i-1
        if j>=0 and ball.vel<0:
            if (ball.pos.x<balls[j].pos.x+2*ball_radius-buffer):
#                print("Backward:",i,j,ball.pos.x,balls[j].pos.x, ball.vel)
                collide(i,j)
                collided=True
#                    print(i,j,ball.pos.x,balls[j].pos.x)
        ball.prev_vel=ball.vel
        ball.prev_theta=ball.theta
        ball.acc=-g * sin(ball.theta)/L
        ball.vel+=ball.acc*dt
        ball.theta+=ball.vel*dt
        ball.pos=vec(L * sin(ball.theta)+2*i*ball_radius,axis_pos-L * cos(ball.theta),0)
        rods[i].pos=ball.pos
        rods[i].axis=vec(2*i*ball_radius,axis_pos,0)-ball.pos
#    print(ball.acc + " " + ball.vel + " " + theta)
    t+=dt
    if (display_graph and int(t/dt)%graph_spacing==0):
        for i in range(num_balls):
            pos_curves[i].plot(t, balls[i].pos.y)
            vel_curves[i].plot(t, balls[i].vel)
    
    
