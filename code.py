Web VPython 3.2
scene = canvas(width=1000, height=450)

program_rate = 1000

#program rate slider - DISABLE FOR USER
#def setRt(x):
#    global program_rate
#    program_rate = x.value
#    rate_text.text="Rate: " + str(x.value)
#wtext(text = "Set Rate:")
#rate_slider = slider(bind = setRt, min=10, max=1000000, value=program_rate, step=10)
#rate_text = wtext("Rate: " + str(rate_slider.value))
#scene.append_to_caption('\n\n')

pos_graph = graph(title="Ball Heights", xtitle="Time", ytitle = "Height")
vel_graph = graph(title="Ball Velocities", xtitle="Time", ytitle = "Velocity")

L=3
axis_pos=3
ball_radius=0.3

initial_angle=0
num_balls=1
num_starting_balls=0

def setInitialAngle(x):
    global initial_angle
    initial_angle=-pi * x.value/180
    initial_angle_text.text="Angle: " + str(x.value)
    
def setNumBalls(x):
    global num_balls
    num_balls=x.value
    num_balls_text.text="# of Balls: " + str(num_balls)
    
def setNumBallsStarting(x):
    global num_starting_balls
    global num_balls
    num_starting_balls=min(x.value, num_balls)
    num_starting_balls_text.text = "# of Elevated Balls: "+str(num_starting_balls)
    
def start():
    set_initial_values.disabled=True
#    initial_angle_slider.delete()
    num_balls_slider.delete()
#    num_starting_balls_slider.delete()
#    initial_angle_slider_caption.delete()
    num_balls_slider_caption.delete()
#    num_starting_balls_slider_caption.delete()
       
#initial_angle_slider_caption = wtext(text = "Set Initial Angle:")
#initial_angle_slider = slider( bind=setInitialAngle, min=0, max=90, value=60, step=1)
#initial_angle_text = wtext(text = "Angle: "+str(initial_angle_slider.value))
#scene.append_to_caption('\n\n')

num_balls_slider_caption = wtext(text = "Set Total # of Balls:")
num_balls_slider = slider(bind=setNumBalls, min=1, max=10, value=1, step=1)
num_balls_text = wtext(text = "# of Balls: "+str(num_balls_slider.value))
scene.append_to_caption('\n\n')

#num_starting_balls_slider_caption = wtext(text = "Set Total # of Elevated Balls:")
#num_starting_balls_slider = slider(bind=setNumBallsStarting, min=1, max=10, value=1, step=1)
#num_starting_balls_text = wtext(text = "# of Elevated Balls: "+str(num_starting_balls_slider.value))
#scene.append_to_caption('\n\n')

set_initial_values = button(bind=start, text="Start", disabled=False)
scene.append_to_caption('\n\n')

while !set_initial_values.disabled:
    rate(program_rate)

#print(initial_angle, num_balls, num_starting_balls)

offset=-ball_radius*num_balls

balls=[]
rods=[]
pos_curves=[]
vel_curves=[]

for i in range(0,num_balls):
    balls.append(sphere(pos=vec(2*i*ball_radius+offset,axis_pos-L,0), radius=ball_radius, color=color.white, texture=textures.metal))
    rods.append(cylinder(pos=balls[i].pos, axis=vec(0,L,0), radius=0.03, color=color.white))
    balls[i].acc=0
    balls[i].vel=0
    balls[i].theta=0
    curr_color=(vector.random()+vec(1,1,1))/2
    pos_curves.append(gcurve(graph=pos_graph, color=curr_color, label="Ball "+str(i)))
    vel_curves.append(gcurve(graph=vel_graph, color=curr_color, label="Ball "+str(i)))

def on_click(ball, mouse):
    dist=sqrt((mouse.x-ball.pos.x)*(mouse.x-ball.pos.x)+(mouse.y-ball.pos.y)*(mouse.y-ball.pos.y)+(mouse.z-ball.pos.z)*(mouse.z-ball.pos.z))
    return dist<=ball_radius

click_drag_text = text(text='Click and Drag', pos=vec(-4,3,0), color=color.red, visible=True)

drag=False
def start_drag():
    global drag
    drag=True
def stop_drag():
    global drag
    drag=False

scene.bind('mousedown', start_drag)
scene.bind('mouseup', stop_drag)

mouse_down = scene.waitfor('mousedown')

starting_ball=-1
while (starting_ball==-1):
    rate(program_rate)
    for i in range(0,num_balls):
        if (on_click(balls[i], mouse_down.pos)):
            starting_ball=i
            break

while drag:
    rate(100)
#    print(scene.mouse.pos.x, scene.mouse.pos.y)
    initial_angle=asin(max(-1, min(1, (scene.mouse.pos.x-mouse_down.pos.x)/L)))
    if (initial_angle<0):
        num_starting_balls=starting_ball+1
        for i in range(num_starting_balls):
            balls[i].pos=pos=vec(L * sin(initial_angle)+2*i*ball_radius+offset,axis_pos-L * cos(initial_angle),0)
            rods[i].pos=balls[i].pos
            rods[i].axis=vec(2*i*ball_radius+offset,axis_pos,0)-balls[i].pos
            balls[i].theta=initial_angle
        for i in range(starting_ball, num_balls):
            balls[i].pos=vec(2*i*ball_radius+offset, axis_pos-L,0)
            rods[i].pos=balls[i].pos
            rods[i].axis=vec(2*i*ball_radius+offset,axis_pos,0)-balls[i].pos
            balls[i].theta=0
    else:
        num_starting_balls=num_balls-starting_ball
        for i in range(starting_ball, num_balls):
            balls[i].pos=vec(L * sin(initial_angle)+2*i*ball_radius+offset,axis_pos-L * cos(initial_angle),0)
            rods[i].pos=balls[i].pos
            rods[i].axis=vec(2*i*ball_radius+offset,axis_pos,0)-balls[i].pos
            balls[i].theta=initial_angle
        for i in range(0, starting_ball):
            balls[i].pos=vec(2*i*ball_radius+offset, axis_pos-L,0)
            rods[i].pos=balls[i].pos
            rods[i].axis=vec(2*i*ball_radius+offset,axis_pos,0)-balls[i].pos
            balls[i].theta=0
#    
#mouse_up = scene.waitfor('mouseup')
click_drag_text.visible=False

#initial_angle=atan((mouse_up.pos.x-balls[starting_ball].pos.x)/(mouse_up.pos.y-balls[starting_ball].pos.y))
#
#if (initial_angle<0):
#    num_starting_balls=starting_ball+1
#    for i in range(num_starting_balls):
#        balls[i].pos=pos=vec(L * sin(initial_angle)+2*i*ball_radius+offset,axis_pos-L * cos(initial_angle),0)
#        rods[i].pos=balls[i].pos
#        rods[i].axis=vec(2*i*ball_radius+offset,axis_pos,0)-balls[i].pos
#        balls[i].theta=initial_angle
#else:
#    num_starting_balls=num_balls-starting_ball
#    for i in range(starting_ball, num_balls):
#        balls[i].pos=pos=vec(L * sin(initial_angle)+2*i*ball_radius+offset,axis_pos-L * cos(initial_angle),0)
#        rods[i].pos=balls[i].pos
#        rods[i].axis=vec(2*i*ball_radius+offset,axis_pos,0)-balls[i].pos
#        balls[i].theta=initial_angle

#while True:
#    rate(program_rate)

g = 9.81
t = 0
dt = 1/2000

def collide(i, j):
    overlap=balls[j].theta-balls[i].theta
#    dir=balls[i].vel/abs(balls[i].vel)
#    balls[j].vel=sqrt(balls[i].vel*balls[i].vel+2*balls[i].acc*overlap)*dir
    balls[j].vel=balls[i].vel
#    print(balls[j].vel)
    balls[i].vel=0
    balls[i].theta+=overlap

buffer=1E-3

run=True
def pause():
    global run
    run=!run
    if (!run):
        pause_button.background=color.green
        pause_button.text='Unpause'
    else:
        pause_button.background=color.red
        pause_button.text='Pause'
pause_button=button(bind=pause, text='Pause', background=color.red)

display_graph=True
graph_spacing=10
def change_display_graph():
    global display_graph
    display_graph=!display_graph
    if (!display_graph):
        display_graph_button.background=color.green
        display_graph_button.text='Display'
    else:
        display_graph_button.background=color.red
        display_graph_button.text='Undisplay'
display_graph_button=button(bind=change_display_graph, text='Undisplay', background=color.red)
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
        ball.pos=vec(L * sin(ball.theta)+2*i*ball_radius+offset,axis_pos-L * cos(ball.theta),0)
        rods[i].pos=ball.pos
        rods[i].axis=vec(2*i*ball_radius+offset,axis_pos,0)-ball.pos#    print(ball.acc + " " + ball.vel + " " + theta)
    t+=dt
    if (display_graph and int(t/dt)%graph_spacing==0):
        for i in range(num_balls):
            pos_curves[i].plot(t, balls[i].pos.y)
            vel_curves[i].plot(t, balls[i].vel)

