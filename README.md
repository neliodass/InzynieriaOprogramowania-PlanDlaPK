# Schedule Optimizer

Genetic algorithm-based class schedule optimizer with API support.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Command Line (with mock data)
```bash
python main.py
```

### API Server
```bash
python api.py
```

Server runs on `http://localhost:5000`

## API Endpoints

### POST /schedule
Create optimized schedule

**Parameters:**
- `use_mock_data` (bool): Use generated test data
- `target_score` (int): Maximum acceptable penalty score (default: 300)
- `max_attempts` (int): Maximum optimization attempts (default: 50)
- `population_size` (int): GA population size (default: 100)
- `generations` (int): GA generations per attempt (default: 100)

**Mock data mode:**
- `num_classes` (int): Number of classes to generate
- `num_rooms` (int): Number of rooms to generate
- `num_slots` (int): Number of time slots to generate

**Custom data mode:**
- `courses`: Array of course objects
- `rooms`: Array of room objects
- `teachers`: Array of teacher objects
- `time_slots`: Array of time slot objects

### GET /health
Check API status

## Examples

### Using mock data
```bash
curl -X POST http://localhost:5000/schedule \
  -H "Content-Type: application/json" \
  -d @example_mock_request.json
```

### Using custom data
```bash
curl -X POST http://localhost:5000/schedule \
  -H "Content-Type: application/json" \
  -d @example_custom_request.json
```

### Run all tests
```bash
./test_api.sh
```

## Data Models

**Course:**
```json
{
  "id": 0,
  "name": "Math 101",
  "group_id": 0,
  "subject": "Mathematics",
  "teacher_id": 0,
  "student_count": 30
}
```

**Room:**
```json
{
  "id": 0,
  "name": "Room A",
  "capacity": 50
}
```

**Teacher:**
```json
{
  "id": 0,
  "name": "John Doe",
  "unavailable_time_slots_ids": [5, 10]
}
```

**TimeSlot:**
```json
{
  "id": 0,
  "day": 0,
  "hour_index": 0,
  "label": "Monday 8:00"
}
```


