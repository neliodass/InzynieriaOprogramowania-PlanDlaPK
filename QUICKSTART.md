# Quick Start

## 1. Run CLI version
```bash
python main.py
```

## 2. Start API server
```bash
python api.py
```

## 3. Test API (in another terminal)

### Option A: Python script
```bash
pip install requests
python test_api.py
```

### Option B: Shell script
```bash
./test_api.sh
```

### Option C: Manual curl
```bash
# Test health
curl http://localhost:5000/health

# Test with mock data
curl -X POST http://localhost:5000/schedule \
  -H "Content-Type: application/json" \
  -d '{"use_mock_data": true, "num_classes": 10, "num_rooms": 3, "num_slots": 15}'

# Test with custom data
curl -X POST http://localhost:5000/schedule \
  -H "Content-Type: application/json" \
  -d @example_custom_request.json
```

