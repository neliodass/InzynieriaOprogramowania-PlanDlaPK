import random
from deap import base, creator, tools, algorithms
import functools
from services.mock_data_generator import *

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)
toolbox = base.Toolbox()
NUM_CLASSES = 50
NUM_ROOMS = 10
NUM_SLOTS = 40
courses,rooms,teachers,time_slots = generate_data(NUM_CLASSES, NUM_ROOMS, NUM_SLOTS)
toolbox.register("attr_room", random.randint, 0, NUM_ROOMS - 1)
toolbox.register("attr_slot", random.randint, 0, NUM_SLOTS - 1)
def create_individual():
    ind = []
    for _ in range(NUM_CLASSES):
        ind.append(toolbox.attr_room())
        ind.append(toolbox.attr_slot())
    return creator.Individual(ind)
toolbox.register("individual", create_individual)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
def evaluate_schedule(individual,courses,rooms,teachers,time_slots):
    penalty = 0
    teacher_schedule = {t.id: [] for t in teachers}
    group_schedule = {}


    for i in range(0,len(individual),2):
        course_index = i // 2
        course = courses[course_index]

        assigned_room_id = individual[i]%len(rooms)
        assigned_slot_id = individual[i+1]%len(time_slots)
        room = rooms[assigned_room_id]
        teacher = next((t for t in teachers if t.id == course.teacher_id), None)
        ts = time_slots[assigned_slot_id]

        if room.capacity < course.student_count:
            penalty += 1000
        if assigned_slot_id in teacher.unavailable_time_slots_ids:
            penalty += 1000

        entry = (ts.day, ts.hour_index, assigned_room_id)
        teacher_schedule[teacher.id].append(entry)

        if course.group_id not in group_schedule:
            group_schedule[course.group_id] = []
        group_schedule[course.group_id].append(entry)

    def calculate_continuity_penalty(schedule_list):
        local_penalty = 0
        if not schedule_list:
            return 0
        sorted_schedule = sorted(schedule_list, key=lambda x: (x[0], x[1]))
        for k in range(len(sorted_schedule) - 1):
            curr_class = sorted_schedule[k]
            next_class = sorted_schedule[k + 1]
            # Same day continuity check
            if curr_class[0] == next_class[0]:
                # Check for gaps
                gap = next_class[1] - curr_class[1] - 1
                if gap > 0:
                    # Penalty for gaps between classes
                    local_penalty += (10 * gap)
                    # Additional penalty if different rooms
                if gap == 0 and curr_class[2] != next_class[2]:
                    local_penalty += 5
        return local_penalty

    for t_id, schedule in teacher_schedule.items():
        penalty += calculate_continuity_penalty(schedule)
    for g_id, schedule in group_schedule.items():
        penalty += calculate_continuity_penalty(schedule)
    return penalty,

toolbox.register("evaluate", functools.partial(evaluate_schedule, courses=courses, rooms=rooms, teachers=teachers, time_slots=time_slots))
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutUniformInt, low=0, up=NUM_SLOTS-1, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)
if __name__ == "__main__":
    pop = toolbox.population(n=100)

    stats = tools.Statistics(lambda ind: ind.fitness.values[0])
    stats.register("min", min)
    stats.register("avg", lambda x: sum(x) / len(x))
    print("Start ewolucji...")
    result, log = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=50,
                                      stats=stats, verbose=True)

    best_ind = tools.selBest(pop, 1)[0]
    print(f"\nNajlepszy wynik (Penalty): {best_ind.fitness.values[0]}")