from models import TimeSlot,Teacher,CourseClass,Room
import random


def generate_data(n_classes, n_rooms, n_slots):
    time_slots = []
    slots_per_day = n_slots // 5
    for i in range(n_slots):
        day = i // slots_per_day
        hour = i % slots_per_day
        time_slots.append(TimeSlot(id=i, day=day, hour_index=hour, label=f"Slot {i}"))
    rooms = []
    for i in range(n_rooms):
        cap = random.choice([30, 60, 120])
        rooms.append(Room(id=i, name=f"Sala {i}", capacity=cap))

    teachers = []
    for i in range(5):
        unavail = random.sample(range(n_slots), 3)
        teachers.append(Teacher(id=i, name=f"Nauczyciel {i}", unavailable_time_slots_ids=unavail))

    courses = []
    for i in range(n_classes):
        t_id = random.randint(0, 4)
        g_id = random.randint(0, 5)  #
        stud_count = random.choice([25, 55, 110])
        courses.append(CourseClass(
            id=i, name=f"Lekcja {i}", group_id=g_id,
            subject="Algo", teacher_id=t_id, student_count=stud_count
        ))

    return courses, rooms, teachers, time_slots