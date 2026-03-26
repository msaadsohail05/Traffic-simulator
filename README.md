# Traffic Simulator - Smart Traffic Control System

A Python-based traffic control simulation game where you manage traffic lights at intersections to optimize traffic flow over a 3-minute period.

## 🎮 Game Overview

**Objective**: Control traffic lights at intersections to:
- ✅ Maximize traffic flow (+10 points per car passed)
- ❌ Minimize congestion (-2 points per queued car)
- ⏱️ Reduce waiting time (-0.5 points per tick of wait)
- 🚫 Prevent collisions (-50 points each)

**Duration**: 3 minutes of real-time simulation

## 🏗️ Project Structure

```
traffic simulator/
├── src/
│   ├── entities.py              # Core game entities (Car, Road, Intersection, TrafficLight)
│   ├── simulation_engine.py     # Main simulation loop and game mechanics
│   └── game.py                  # CLI game controller and UI
├── tests/
│   └── test_simulator.py        # Unit tests for all components
├── README.md                    # This file
└── requirements.txt             # Python dependencies
```

## 🧩 Core Entities

### 1. **Car**
- Moves along roads at variable speeds
- Stops at red lights
- Tracks waiting time
- Removed when reaching destination

**Attributes**:
- `id`: Unique identifier
- `speed`: Units per tick (0.5-2.0)
- `position`: (x, y) coordinates
- `direction`: N, S, E, W
- `waiting_time`: Accumulated ticks stopped
- `is_stopped`: Current motion state

### 2. **Road**
- Connects two intersections
- Has multiple lanes
- Contains queue of cars
- Tracks traffic flow

**Attributes**:
- `id`: Unique identifier
- `length`: Road distance
- `lanes`: Number of lanes
- `cars`: List of cars on road
- `start_intersection_id`, `end_intersection_id`

### 3. **Intersection**
- Junction of roads
- Controls traffic lights for two directions
- NS (North-South) and EW (East-West) lights

**Attributes**:
- `id`: Unique identifier
- `position`: (x, y) coordinates
- `ns_light`: North-South traffic light
- `ew_light`: East-West traffic light
- `incoming_roads`, `outgoing_roads`: Connected roads

### 4. **Traffic Light**
- Controls vehicle flow
- Two states: GREEN or RED
- Configurable duration

**Attributes**:
- `state`: GREEN or RED
- `duration`: Ticks before switching
- `timer`: Current progress

## 🔄 Simulation Engine

### Game Loop (every 100ms)

```python
while game_running:
    spawn_cars()           # Randomly add cars to roads (30% chance per tick)
    update_car_positions() # Move cars and check for red lights
    handle_intersections() # Update traffic light timers
    update_waiting_times() # Increment wait timers for stopped cars
    calculate_score()      # Update scoring
```

### Tick-Based System
- **Tick Interval**: 100ms
- **Ticks Per Second**: 10
- **Total Ticks**: 1,800 (3 minutes)

## 🎮 How to Play

### Starting the Game

```bash
python src/game.py
```

### Main Menu
```
1. Start Game      - Begin the simulation
2. Settings        - Configure game options
3. Help            - View game rules
4. Exit            - Quit the game
```

### In-Game Commands

**Change Traffic Light:**
```
light <intersection_id> <NS/EW> <GREEN/RED>
```

**Examples:**
```
light 1 NS GREEN   # Set intersection 1 north-south to green
light 2 EW RED     # Set intersection 2 east-west to red
light 3 NS RED     # Set intersection 3 north-south to red
```

**Exit Game:**
```
quit               # End game early
```

## 📊 Scoring System

### Points Gained
- **+10 points** per car that successfully passes through intersection

### Points Lost
- **-0.5 points** per tick of waiting time (accumulated across all cars)
- **-2 points** per car in queue at any given moment
- **-50 points** per collision
- **-10 points** per second of total queue wait time

### Example Score Calculation
```
Flow Score:        200 cars × 10 = +2000 points
Wait Penalty:      1000 ticks × 0.5 = -500 points
Queue Penalty:     avg 5 cars × 2 = -10 points per tick
Total Score:       2000 - 500 - queue_penalty = ~1490
```

## 🕹️ Default Map Layout

A 2×2 grid intersection setup:

```
        NW -------- NE
        |           |
        |           |
        SW -------- SE
```

**Intersections**:
- NW (0, 100) - Northwest
- NE (100, 100) - Northeast
- SW (0, 0) - Southwest
- SE (100, 0) - Southeast

**Connections**:
- North Road: NW ↔ NE
- South Road: SW ↔ SE
- West Road: NW ↔ SW
- East Road: NE ↔ SE

## 💡 Strategy Tips

1. **Alternate Traffic Lights**
   - Switch between NS and EW to prevent gridlock
   - Coordinate timing across intersections

2. **Monitor Queue Lengths**
   - Watch for buildup at specific approaches
   - Adjust light timing preemptively

3. **Balance Flow**
   - Don't favor one direction completely
   - Rotate priority every 20-30 seconds

4. **Plan Ahead**
   - Anticipate traffic surges
   - Adjust lights before congestion occurs

## 🧪 Testing

Run unit tests:

```bash
python -m pytest tests/test_simulator.py -v
```

Or using unittest:

```bash
python tests/test_simulator.py
```

### Test Coverage
- Entity creation and manipulation
- Car movement and stopping logic
- Queue tracking
- Traffic light state transitions
- Simulation engine initialization and game loop
- Scoring calculations

## 📋 Installation

### Requirements
- Python 3.8+
- No external dependencies for core simulation

### Setup

1. Clone or download the project
2. Navigate to project directory
3. Run the game:
   ```bash
   python src/game.py
   ```

## 🚀 Future Enhancements

- [ ] Graphical UI (Pygame/PyQt)
- [ ] Real-time visualization of traffic flow
- [ ] Multiple difficulty levels
- [ ] Advanced AI for traffic prediction
- [ ] Custom map editor
- [ ] Network multiplayer
- [ ] Leaderboards
- [ ] Replay system
- [ ] Advanced collision detection
- [ ] Variable spawn rates based on time of day

## 📝 API Reference

### SimulationEngine

```python
engine = SimulationEngine(game_duration=180, tick_interval=100)

# Setup
engine.setup_grid_network()

# Game control
engine.start_game()
engine.stop_game()
engine.tick()

# Traffic light control
engine.set_traffic_light(intersection_id, "NS", SignalState.GREEN, duration=30)

# Statistics
stats = engine.get_game_stats()
```

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Enhanced visualization
- Better pathfinding for cars
- Accident physics
- Weather effects
- Time-of-day traffic patterns

## 📄 License

This project is open source and available for educational purposes.

---

**Built with ❤️ as an educational traffic simulation system**
