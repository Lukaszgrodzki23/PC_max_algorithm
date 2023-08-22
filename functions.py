def naive_schedule(process, cpu_count):
    cpu_history = cpu_count * [[]]
    out = []
    shifted_proc = []
    cpu_time = [0] * cpu_count

    for i in process:
        mini = cpu_time.index(min(cpu_time))
        cpu_time[mini] += i
        cpu_history[mini].append(i)

    for i in range(len(cpu_history)):
        for j in cpu_history[i]:
            out.append(i)
            shifted_proc.append(j)

    return out, shifted_proc


def initialize_population(starting_solution, pop_size, pc_count, task_count):
    population = [starting_solution] * (math.ceil(pop_size / 2))
    for i in range (math.floor(pop_size / 2)):
        rand_solution = []
        for j in range(task_count):
            rand_solution.append(random.randint(0, pc_count - 1))
        population.append(rand_solution)
    return population


def evaluate_solution(solution, pc_count, task_times):
    pc_times = [0] * pc_count
    for i in range(len(solution)):
        pc_index = solution[i]
        pc_times[pc_index] += task_times[i]
    return max(pc_times)


def select_parents(population, fitnesses, parent_count):
    population_and_fitnesses = list(zip(population, fitnesses))
    total_fitness = sum(fitnesses)
    chosen_indices = []
    for _ in range(parent_count):
        rand = random.uniform(0, total_fitness)
        curr_sum = 0
        for i, (solution, fitness) in enumerate(population_and_fitnesses):
            curr_sum += fitness
            if curr_sum >= rand:
                chosen_indices.append(i)
                break
    return [population[i] for i in chosen_indices]


def crossover(parent1, parent2):
    cross_point = random.randint(1, len(parent1) - 1)
    child = parent1[:cross_point] + parent2[cross_point:]
    return child


def mutate(solution, mutation_probability, pc_count):
    for i in range(len(solution)):
        if random.random() < mutation_probability:
            solution[i] = random.randint(0, pc_count - 1)
    return solution


def shuffle(task_times, solution, number_of_shuffles):
    for i in range(number_of_shuffles):
        a = random.randint(0, len(solution) - 1)
        b = random.randint(0, len(solution) - 1)
        task_times[a], task_times[b] = task_times[b], task_times[a]
        solution[a], solution[b] = solution[b], solution[a]
    return task_times, solution


def solve_pcmax(pc_count, task_times, starting_solution, pop_size, max_generations, mutation_probability):

    population = initialize_population(starting_solution, pop_size, pc_count, task_count)
    
    fitnesses = [evaluate_solution(solution, pc_count, task_times) for solution in population]
    best_fitness = 100000000
    counter = 0
    for generation in range(max_generations):
        parents = select_parents(population, fitnesses, 2)
        a = len(population)
        population = []
        for i in range(a - 1):
            population.append(crossover(parents[0], parents[1]))
        population.append([random.randint(0, pc_count - 1) for i in range(len(task_times))])
        for i in range(a):
            mutated_population = [mutate(j, mutation_probability, pc_count) for j in population]
        population = mutated_population[:]
        fitnesses = [evaluate_solution(solution, pc_count, task_times) for solution in population]
        temp = min(fitnesses)
        if temp < best_fitness:
            best_fitness = temp
            best_solution = population[fitnesses.index(temp)]
            counter = 0
        else:
            counter += 1
        if counter == 150:
            mutation_probability += 0.00001
            print("mutation increased")
            
        if counter == 200:
            population[random.randint(0, pop_size - 1)] = starting_solution
            counter = 0
        print(best_fitness, generation,temp)
    return (best_fitness, best_solution)
