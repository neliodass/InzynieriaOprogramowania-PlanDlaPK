from flask import Flask, request, jsonify, render_template
from models import CourseClass, Room, Teacher, TimeSlot, Group
from scheduler import SchedulerEngine
from services.mock_data_generator import generate_data

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/schedule', methods=['POST'])
def create_schedule():
    data = request.json

    use_mock = data.get('use_mock_data', False)
    groups = []

    if use_mock:
        num_classes = data.get('num_classes', 50)
        num_rooms = data.get('num_rooms', 10)
        num_slots = data.get('num_slots', 40)
        courses, rooms, teachers, time_slots = generate_data(num_classes, num_rooms, num_slots)
        # Generowanie podstawowych grup dla mock data
        unique_group_ids = list(set(course.group_id for course in courses))
        groups = [Group(id=gid, name=f"Grupa {gid}", parent_group_id=None) for gid in unique_group_ids]
    else:
        courses_data = data.get('courses', [])
        rooms_data = data.get('rooms', [])
        teachers_data = data.get('teachers', [])
        time_slots_data = data.get('time_slots', [])
        groups_data = data.get('groups', [])

        if not all([courses_data, rooms_data, teachers_data, time_slots_data]):
            return jsonify({"error": "Missing required data"}), 400

        courses = [CourseClass(**c) for c in courses_data]
        rooms = [Room(**r) for r in rooms_data]
        teachers = [Teacher(**t) for t in teachers_data]
        time_slots = [TimeSlot(**ts) for ts in time_slots_data]
        groups = [Group(**g) for g in groups_data] if groups_data else []

    target_score = data.get('target_score', 300)
    max_attempts = data.get('max_attempts', 50)
    population_size = data.get('population_size', 100)
    generations = data.get('generations', 100)

    engine = SchedulerEngine(courses, rooms, teachers, time_slots, groups)
    best_ind, score = engine.run(target_score, max_attempts, population_size, generations)
    schedule = engine.decode_schedule(best_ind)

    # Przygotowanie danych grup dla frontendu
    groups_dict = [{"id": g.id, "name": g.name, "parent_group_id": g.parent_group_id} for g in groups]

    # Przygotowanie danych nauczycieli dla frontendu
    teachers_dict = [{"id": t.id, "name": t.name} for t in teachers]

    return jsonify({
        "score": score,
        "success": score <= target_score,
        "schedule": schedule,
        "groups": groups_dict,
        "teachers": teachers_dict
    })


@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})


if __name__ == '__main__':
    app.run(debug=True, port=5000)

