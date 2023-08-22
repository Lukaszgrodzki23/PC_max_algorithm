import random
import math

filepath = "m10.txt.txt"
f = open(filepath, "r")
pc_count = int(f.readline())
task_count = int(f.readline())
task_times = []
for i in range(task_count):
    task_times.append(int(f.readline()))
starting_solution, shifted_proc = list(naiveschedule(task_times, pc_count))
shuffledStartingSolution, shuffledTask_times = shuffle(starting_solution, shifted_proc, task_count * 5)
# print(starting_solution)
print(evaluate_solution(shuffledStartingSolution, pc_count, shuffledTask_times))
solve_pcmax(pc_count, shuffledTask_times, shuffledStartingSolution,50, 100000, 0.005)
