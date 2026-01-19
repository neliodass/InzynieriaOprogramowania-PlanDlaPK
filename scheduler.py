import random
from deap import base, creator, tools, algorithms
import functools


class SchedulerEngine:
    def __init__(self, courses, rooms, teachers, time_slots, groups=None):
        self.courses = courses
        self.rooms = rooms
        self.teachers = teachers
        self.time_slots = time_slots
        self.groups = groups or []
        self.num_classes = len(courses)
        self.num_rooms = len(rooms)
        self.num_slots = len(time_slots)

        if not hasattr(creator, "FitnessMin"):
            creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        if not hasattr(creator, "Individual"):
            creator.create("Individual", list, fitness=creator.FitnessMin)

        self.toolbox = base.Toolbox()
        self.toolbox.register("attr_room", random.randint, 0, self.num_rooms - 1)
        self.toolbox.register("attr_slot", random.randint, 0, self.num_slots - 1)
        self.toolbox.register("individual", self._create_individual)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)
        self.toolbox.register("evaluate", functools.partial(self._evaluate_schedule))
        self.toolbox.register("mate", tools.cxTwoPoint)
        self.toolbox.register("mutate", tools.mutUniformInt, low=0, up=self.num_slots-1, indpb=0.05)
        self.toolbox.register("select", tools.selTournament, tournsize=3)

    def _create_individual(self):
        ind = []
        for _ in range(self.num_classes):
            ind.append(self.toolbox.attr_room())
            ind.append(self.toolbox.attr_slot())
        return creator.Individual(ind)

    def _evaluate_schedule(self, individual):
        penalty = 0
        teacher_schedule = {t.id: [] for t in self.teachers}
        group_schedule = {}
        room_occupancy = {}

        for i in range(0, len(individual), 2):
            course_index = i // 2
            course = self.courses[course_index]
            assigned_room_id = individual[i] % self.num_rooms
            assigned_slot_id = individual[i+1] % self.num_slots
            room = self.rooms[assigned_room_id]
            teacher = next((t for t in self.teachers if t.id == course.teacher_id), None)
            ts = self.time_slots[assigned_slot_id]

            occupancy_key = (assigned_room_id, assigned_slot_id)
            if occupancy_key in room_occupancy:
                penalty += 5000
            else:
                room_occupancy[occupancy_key] = True

            if room.capacity < course.student_count:
                penalty += 1000

            if assigned_slot_id in teacher.unavailable_time_slots_ids:
                penalty += 1000

            entry = (ts.day, ts.hour_index, assigned_room_id)
            teacher_schedule[teacher.id].append(entry)

            if course.group_id not in group_schedule:
                group_schedule[course.group_id] = []
            group_schedule[course.group_id].append(entry)

        for t_id, schedule in teacher_schedule.items():
            penalty += self._calculate_continuity_penalty(schedule)
        for g_id, schedule in group_schedule.items():
            penalty += self._calculate_continuity_penalty(schedule)

        return penalty,

    def _calculate_continuity_penalty(self, schedule_list):
        local_penalty = 0
        if not schedule_list:
            return 0
        sorted_schedule = sorted(schedule_list, key=lambda x: (x[0], x[1]))
        for k in range(len(sorted_schedule) - 1):
            curr_class = sorted_schedule[k]
            next_class = sorted_schedule[k + 1]
            if curr_class[0] == next_class[0]:
                if curr_class[1] == next_class[1]:
                    local_penalty += 5000
                    continue
                gap = next_class[1] - curr_class[1] - 1
                if gap > 0:
                    local_penalty += (10 * gap)
                if gap == 0 and curr_class[2] != next_class[2]:
                    local_penalty += 5
        return local_penalty

    def run(self, target_score=300, max_attempts=50, population_size=100, generations=100):
        attempt = 1
        stats = tools.Statistics(lambda ind: ind.fitness.values[0])
        stats.register("min", min)
        stats.register("avg", lambda x: sum(x) / len(x))

        while attempt <= max_attempts:
            print(f"\n--- ATTEMPT {attempt} ---")
            pop = self.toolbox.population(n=population_size)
            pop, log = algorithms.eaSimple(pop, self.toolbox, cxpb=0.7, mutpb=0.3, ngen=generations,
                                           stats=stats, verbose=False)
            best_ind = tools.selBest(pop, 1)[0]
            score = best_ind.fitness.values[0]
            print(f"Attempt {attempt} finished. Best score: {score}")

            if score <= target_score:
                print(f"\nSUCCESS! Found solution with score {score} in attempt {attempt}.")
                return best_ind, score
            else:
                print("Score not satisfactory. Restarting...")
                attempt += 1

        print("Failed to find satisfactory solution.")
        return best_ind, score

    def decode_schedule(self, individual):
        schedule = []
        # Utworzenie mapy grup dla szybkiego dostępu
        groups_map = {g.id: g for g in self.groups}

        for i in range(0, len(individual), 2):
            course_index = i // 2
            course = self.courses[course_index]
            assigned_room_id = individual[i] % self.num_rooms
            assigned_slot_id = individual[i+1] % self.num_slots
            room = self.rooms[assigned_room_id]
            ts = self.time_slots[assigned_slot_id]
            teacher = next((t for t in self.teachers if t.id == course.teacher_id), None)

            group = groups_map.get(course.group_id)
            group_name = group.name if group else f"Grupa {course.group_id}"
            parent_group_id = group.parent_group_id if group else None

            schedule.append({
                "course_id": course.id,
                "course_name": course.name,
                "room_id": room.id,
                "room_name": room.name,
                "time_slot_id": ts.id,
                "day": ts.day,
                "hour_index": ts.hour_index,
                "label": ts.label,
                "teacher_id": teacher.id,
                "teacher_name": teacher.name,
                "group_id": course.group_id,
                "group_name": group_name,
                "parent_group_id": parent_group_id,
            })
        return schedule

