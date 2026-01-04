import turtle, keyboard as kb, random, time,json,copy

#constants
WIDTH, HEIGHT = 800, 600
gravity = 1
bird_x = -250
bird_size = 50
pipe_xstart = 500
pipe_xend = -500
pipe_speed = 5
pipe_gap = 200
pipe_width = 100
#variables
pipes = []
bird_y = 0
points = 0 # = score
bird_speed = 0
next_pipe = 0
last_inp = False
death = False

turrtlesetupt = False


#pipe = [x,y,point(True when pipe already gave the bird point)]
def draw():
    global turrtlesetupt,s,t
    if not turrtlesetupt:
        s = turtle.Screen()
        s.setup(WIDTH, HEIGHT)
        s.title("Flappy Bird")
        s.bgcolor("skyblue")
        s.tracer(0,0)
        t = turtle.Turtle()
        t.hideturtle()
        t.speed(0)
        t.clear()
        t.penup()
        turrtlesetupt = True
    t.clear()
    t.goto(bird_x, bird_y)
    t.dot(bird_size, "yellow")
    t.write(str(points), align="center", font=("Arial", 16, "normal"))
    for pipe in pipes:
        t.goto(pipe[0]-pipe_width/2, HEIGHT/2)
        t.color("green", "green")
        t.begin_fill()
        t.goto(pipe[0]-pipe_width/2, pipe[1]+pipe_gap/2)
        t.goto(pipe[0]+pipe_width/2, pipe[1]+pipe_gap/2)
        t.goto(pipe[0]+pipe_width/2, HEIGHT/2)
        t.end_fill()
        t.goto(pipe[0]-pipe_width/2, -HEIGHT/2)
        t.begin_fill()
        t.goto(pipe[0]-pipe_width/2, pipe[1]-pipe_gap/2)
        t.goto(pipe[0]+pipe_width/2, pipe[1]-pipe_gap/2)
        t.goto(pipe[0]+pipe_width/2, -HEIGHT/2)
        t.end_fill()
    s.update()

def setup():
    global bird_y, bird_speed, pipes, points, bird_x, next_pipe, gravity, last_inp, death
    pipes = []
    bird_y = 0
    points = 0
    bird_speed = 0
    next_pipe = 0
    last_inp = False
    death = False
def update(inp):
    global bird_y, bird_speed, pipes, points, bird_x, next_pipe, gravity, last_inp, death
    pipe_delete = []
    if inp:
        if not last_inp:
            bird_speed = 10
            last_inp = True   
    else:
        last_inp = False
    bird_y += bird_speed
    bird_speed -= gravity
    for i in range(len(pipes)):
        pipes[i][0] -= pipe_speed
        if pipes[i][0] < bird_x:
            if pipes[i][2] == False:
                points += 1
                pipes[i][2] = True
        if pipes[i][0] < pipe_xend:
            pipe_delete.append(i)
    for i in pipe_delete:
        pipes.pop(i)
    next_pipe -= pipe_speed
    if next_pipe < 0:
        next_pipe = random.randint(300, 350)
        pipes.append([pipe_xstart, random.randint(-HEIGHT/2+pipe_gap/2,HEIGHT/2-pipe_gap/2), False])



    for pipe in pipes:
        pipe_left = pipe[0] - pipe_width / 2
        pipe_right = pipe[0] + pipe_width / 2
        gap_top = pipe[1] + pipe_gap / 2
        gap_bottom = pipe[1] - pipe_gap / 2
        bird_radius = bird_size / 2
        closest_x = max(pipe_left, min(bird_x, pipe_right))
        closest_y = max(gap_top, min(bird_y, HEIGHT/2))
        dx = bird_x - closest_x
        dy = bird_y - closest_y
        if dx*dx + dy*dy < bird_radius*bird_radius:
            death = True
        closest_x = max(pipe_left, min(bird_x, pipe_right))
        closest_y = max(-HEIGHT/2, min(bird_y, gap_bottom))
        dx = bird_x - closest_x
        dy = bird_y - closest_y
        if dx*dx + dy*dy < bird_radius*bird_radius:
            death = True
    if bird_y < -HEIGHT/2 + bird_size/2 or bird_y > HEIGHT/2 - bird_size/2:
        death = True
    #if points > 500:
        #death = True
        
def play():
    setup()
    time.sleep(1)
    while True:
        time.sleep(0.02)
        inp = kb.is_pressed("space")
        update(inp)
        draw()
        if death:
            t.goto(0, 0)
            t.write("Game Over! Score: " + str(points), align="center", font=("Arial", 24, "normal"))
            s.update()
            time.sleep(2)
            setup()

#play()

def random_weights():
    l = [[],[]]
    b = []
    for i in range(7):
        l2 = []
        for j in range(10):
            l2.append(round(random.uniform(-1, 1),3))
        l[0].append(l2)
    for i in range(10):
        l2 = []
        for j in range(2):
            l2.append(round(random.uniform(-1, 1),3))
        l[1].append(l2)
    b2 = []
    for i in range(10):
        b2.append(round(random.uniform(-1, 1),3))
    b.append(b2)
    for i in range(2):
        b2 = []
        b2.append(round(random.uniform(-1, 1),3))
    b.append(b2)
    return [l, b]

def aiinp(bird_y, bird_speed, last_inp, pipes,weight, bias):
    if last_inp:
        return False
    for i in range(len(pipes)):
        if pipes[i][0] + pipe_width/2 < bird_x - bird_size/2:
            continue
        p = i
        break
    if len(pipes) == 0:
        inputs = [bird_y, bird_speed, last_inp, 800, 0, 800, 0]
    elif p == len(pipes)-1:
        inputs = [bird_y, bird_speed, last_inp, pipes[p][0], pipes[p][1], 800, 0]
    else:
        inputs = [bird_y, bird_speed, last_inp, pipes[p][0], pipes[p][1], pipes[p+1][0], pipes[p+1][1]]
    layer1 = []
    for i in range(10):
        layer1.append(0)
    for i in range(7):
        for j in range(10):
            layer1[j] += inputs[i] * weight[0][i][j]
    for i in range(10):
        layer1[i] += bias[0][i]
    outputlayer = []
    for i in range(2):
        outputlayer.append(0)
    for i in range(10):
        for j in range(2):
            outputlayer[j] += layer1[i] * weight[1][i][j]
    
    if outputlayer[0] > outputlayer[1]:
        return True
    else:
        return False
    
def ai_train(weight, bias):
    global bird_y, bird_speed, pipes, points, bird_x, next_pipe, gravity, last_inp, death
    setup()
    while True:
        inp = aiinp(bird_y, bird_speed, last_inp, pipes, weight, bias)
        update(inp)
        if death or points >= 500:
            return points
def mutate_weights(weights, bias, rate, amount):
    new_weights = []
    new_bias = []
    for i in weights:
        mutated_layer = []
        for j in i:
            mutated_neuron = []
            for k in j:
                if random.random() < rate:
                    k += random.uniform(-amount, amount)
                mutated_neuron.append(round(k, 3))
            mutated_layer.append(mutated_neuron)
        new_weights.append(mutated_layer)
    for i in bias:
        mutated_layer = []
        for j in i:
            if random.random() < rate:
                j += random.uniform(-amount, amount)
            mutated_layer.append(round(j, 3))
        new_bias.append(mutated_layer)
    return [new_weights, new_bias]
def ai_evolution(birds_per_gen,gens,keep,mutate,topmutate,rate=0.05,amount=0.1):
    train_data = []
    for i in range(birds_per_gen):
        print(f"Training Gen0: {i+1}/{birds_per_gen}", end="\r")
        a = random_weights()
        p = ai_train(a[0], a[1])
        train_data.append((a[0], a[1], p))
    print()
    print(f"Best Score: {max(train_data, key=lambda x: x[2])[2]}")
    for i in range(gens):
        print (f"Training Gen{i+1}: ", end="\r")
        train_data.sort(key=lambda x: x[2], reverse=True)
        new_data = []
        for j in range(keep):
            print(f"Training Gen{i+1}: {j+1}/{birds_per_gen}", end="\r")
            p = ai_train(train_data[j][0], train_data[j][1])
            new_data.append([train_data[j][0], train_data[j][1], p])
        for j in range(mutate-keep):
            print(f"Training Gen{i+1}: {j+1+keep}/{birds_per_gen}", end="\r")
            index = random.randint(0, topmutate-1)
            a = mutate_weights(train_data[index][0],train_data[index][1], rate, amount)
            p = ai_train(a[0], a[1])
            new_data.append((a[0], a[1], p))
        for j in range(birds_per_gen - mutate):
            print(f"Training Gen{i+1}: {j+1+mutate}/{birds_per_gen}", end="\r")
            a = random_weights()
            p = ai_train(a[0], a[1])
            new_data.append((a[0], a[1], p))
        print(f"\nBest Score: {max(train_data, key=lambda x: x[2])[2]}")
        train_data = copy.deepcopy(new_data)
    best_weights = max(train_data, key=lambda x: x[2])
    print("Training Done!")
    file = input("Enter filname to save trainingdata: ")
    if file.split(".")[-1] != "json":
        file += ".json"
    with open(file, "w") as f:
        json.dump([best_weights[0],best_weights[1]], f)
def ai_play(weight, bias):
    global bird_y, bird_speed, pipes, points, bird_x, next_pipe, gravity, last_inp, death
    setup()
    while True:
        inp = aiinp(bird_y, bird_speed, last_inp, pipes, weight, bias)
        update(inp)
        draw()
        time.sleep(0.01)
        if death:
            t.goto(0, 0)
            t.write("Game Over! Score: " + str(points), align="center", font=("Arial", 24, "normal"))
            s.update()
            time.sleep(2)
            setup()
def read_weights(filename):
    if filename.split(".")[-1] != "json":
        filename += ".json"
    with open(filename, "r") as f:
        data = json.load(f)
    return [data[0], data[1]]

if __name__== "__main__":
    print("1: Play\n2: Train AI\n3: Let AI play from Trainingdata")
    option = 0
    while not option in ["1","2","3"]:
        option = input("Option: ")
        if option not in ["1","2","3"]:
            print("Invalid Option, try again!")
    option = int(option)
    match option:
        case 1:
            play()
        case 2:
            inputs = []
            current = ""
            valid = False
            for k in [["Generations",30,True],["Birds per generation",1000,True],["the best Birds to keep",50,True],["Birds to mutate",200,True],["Max rank for Mutation",300,False]]:
                valid = False
                while not valid:
                    current = input("Amount of "*k[2]+k[0]+f"(write nothing for default: {k[1]}): ")
                    if current == "":
                        current = k[1]
                        break
                    try:
                        current = int(current)
                        valid = True
                    except:
                        print("Invalid Value, try again!")
                inputs.append(current)
            ai_evolution(inputs[1],inputs[0],inputs[2],inputs[3],inputs[4])
        case 3:
            file = input("Enter filname to load trainingdata: ")
            data = read_weights(file)
            ai_play(data[0],data[1])

        case _:
            print("Unexpected error occured")
            quit()