from services.mock_data_generator import generate_data
from scheduler import SchedulerEngine


if __name__ == "__main__":
    NUM_CLASSES = 50
    NUM_ROOMS = 10
    NUM_SLOTS = 40

    courses, rooms, teachers, time_slots = generate_data(NUM_CLASSES, NUM_ROOMS, NUM_SLOTS)

    engine = SchedulerEngine(courses, rooms, teachers, time_slots)
    best_ind, score = engine.run(target_score=300, max_attempts=50)

    if score <= 300:
        schedule = engine.decode_schedule(best_ind)
        print(f"\nSchedule details:")
        for entry in schedule[:5]:
            print(entry)
        print(f"... and {len(schedule) - 5} more entries")
