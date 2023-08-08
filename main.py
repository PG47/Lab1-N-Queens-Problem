from queue import PriorityQueue
import time, psutil, tracemalloc, random
import  random, heapq


# Check if a queen can be placed at position (row, col)
def is_safe(state, col, row):
    for i in range(col):
        if state[i] == row or abs(state[i] - row) == abs(i - col):
            return False
    return True

#expanding the state with all childs for A*
def Achildstate(state):
    childs = []
    n = len(state)
    for i in range(n):
        for j in range(n):
            if (j != state[i]):
                new_child = state.copy()
                new_child[i] = j
                childs.append(new_child)
    return childs

#check conflicts of the current state,
#It is also a heuristic in A* and fitness in GA
def conflict(state):
    c = 0
    n = len(state)
    for i in range(n):
        for j in range(i + 1, n):
            if ((state[i] == state[j]) or (abs(state[i] - state[j]) == j - i)):
                c += 1
    return c

def set_population(n):
    list = PriorityQueue()
    num = random.randint(2,n)
    while num !=0:
        initial_state = [random.randint(0, n - 1) for _ in range(n)]
        list.put((conflict(initial_state), initial_state))
        num -=1
    return  list

def checkgoal(queue):
    list = []
    while not queue.empty():
        item = queue.get()
        list.append(item)
        cost, state = item[0],item[1]
        if(cost == 0):
            return state

    for item in list:
        queue.put(item)
    return None

def crossover(state1, state2):
    n = len(state2)
    cross_point = random.randint(0, n-1)
    return state1[:cross_point] + state2[cross_point:n], state2[:cross_point] + state1[cross_point:n]

def mutate(state):
    n = len(state)
    mutate_point = random.randint(0,n-1)
    mutate_num = random.randint(0,n-1)
    #check if the mutation number is not the same at the present number
    while (mutate_num == state[mutate_point]):
        mutate_num = random.randint(0, n - 1)
    state[mutate_point] = mutate_num
    return  state

def UCS(n):
    #create a random first state to solve
    init_state = [random.randint(0, n - 1) for _ in range(n)]
    print(init_state)
    # creat a queue to put all state to check one by one
    stack = [(0,init_state)]
    while stack:
        cost,state = heapq.heappop(stack)
        if (conflict(state) == 0):  # mean this state is an answer => return it
            return state
        #if not put expand the state
        for row in range(n):
            if(is_safe(state,cost,row)):
                new_state = state[:cost] + [row] + state[cost + 1:]
                heapq.heappush(stack,(cost+1,new_state))
        stack.sort(key=lambda x: x[0])
    return None

def A_star(n):
    #create a random first state to solve
    init_state = [random.randint(0, n - 1) for _ in range(n)]

    #create a first node with heuristic + cost + state
    node = [(conflict(init_state),0,init_state)]

    # create an exlored stack so we dont have to check state again
    explored = []
    # create a stack to put all node to check one by one
    stack = [node]
    while stack:
        heuristic,cost,state = heapq.heappop(node)
        # checked the state so we dont have to check it again
        explored.append(state)
        if (heuristic == 0):  # mean this state is an answer => return it
            return state
        #if not put all child state to stack
        for c_state in Achildstate(state):
            if(c_state not in explored):
                heapq.heappush(node,(conflict(c_state),cost+1,c_state))
        stack.sort(key=lambda x: x[0] + x[1])
    return None

def GA(n):
    init_state = [random.randint(0, n - 1) for _ in range(n)]
    population = set_population(n)
    population.put((conflict(init_state),init_state))

    # create an exlored stack so we dont have to check state again
    explored = []

    #check if there is a solution state already in the sample?
    result = checkgoal(population)

    while result == None:
        m = random.randint(2, population.qsize())
        for i in range(0, m, 2):
            if (i + 2 <= m):
                #pick 2 state to begin crossover and mutation
                cost1,state1 = population.get()
                cost2,state2 = population.get()

                explored.append(state1)
                explored.append(state2)

                # crossover
                state1,state2 = crossover(state1,state2)

                # mutation
                state1 = mutate(state1)
                while (state1 in explored or cost1 < conflict(state1)):
                    state1 = mutate(state1)
                state2 = mutate(state2)
                while (state2 in explored or cost2 < conflict(state2)):
                    state2 = mutate(state2)

                # add 2 new mutation state into the population
                population.put((conflict(state1),state1))
                population.put((conflict(state2),state2))

        result = checkgoal(population)

    return  result

def print_board(state):
    n = len(state)
    for i in range(n):
        line = ""
        for j in range(n):
            if(state[j] == i):
                line +="Q "
            else:
                line +="* "
        print(line)
    print()


#Main program
n = int(input("Enter the number of queens: "))
print("1. UCS")
print("2. A*")
print("3. Genetic algorithm")
a = int(input("Enter the type of algorithms to solve(1-3):"))

#variable to count time and memory
tim = []
mem = []

if (n <= 3):
    print("No solution found")
    exit()

if (a == 1):
    print("Solution with UCS algorithm")
    for i in range(3):
        tracemalloc.start()  # start tracking memory usage
        start_time = time.time()  # start tracking running time
        print(f"Case {i+1}")
        solution = UCS(n)
        print_board(solution)

        peak = tracemalloc.get_traced_memory()[1]
        tracemalloc.stop()
        tim.append(time.time() - start_time)
        mem.append(peak / 1024 ** 2)

    print(f"Running time: {(sum(tim)/3) * 1000:.4f} ms")
    print(f"Memory usage: {(sum(mem)/3):.4f} MB")

elif(a == 2):
    print("Solution with A* algorithm")
    for i in range(3):
        tracemalloc.start()  # start tracking memory usage
        start_time = time.time()  # start tracking running time
        print(f"Case {i + 1}")
        solution = A_star(n)
        print_board(solution)

        peak = tracemalloc.get_traced_memory()[1]
        tracemalloc.stop()
        tim.append(time.time() - start_time)
        mem.append(peak / 1024 ** 2)

    print(f"Running time: {(sum(tim) / 3) * 1000:.4f} ms")
    print(f"Memory usage: {(sum(mem) / 3):.4f} MB")
elif(a == 3):
    print("Solution wit Genetic Algorithm")
    for i in range(3):
        tracemalloc.start()  # start tracking memory usage
        start_time = time.time()  # start tracking running time
        print(f"Case {i+1}")
        solution = GA(n)
        print_board(solution)

        peak = tracemalloc.get_traced_memory()[1]
        tracemalloc.stop()
        tim.append(time.time() - start_time)
        mem.append(peak / 1024 ** 2)

    print(f"Running time: {(sum(tim) / 3) * 1000:.4f} ms")
    print(f"Memory usage: {(sum(mem) / 3):.4f} MB")
else:
    print("Wrong input!")