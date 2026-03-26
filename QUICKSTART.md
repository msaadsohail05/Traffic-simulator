# Quick Start Guide - Traffic Simulator

## Installation

1. **Navigate to project directory**:
```bash
cd "c:\Users\ABC\Documents\traffic simulator"
```

2. **Python 3.8+ is required** (check with `python --version`)

## Running the Simulation

### Option 1: Interactive CLI Game
```bash
python src/game.py
```
- Use menu to start game
- Control traffic lights with commands: `light <id> <NS/EW> <GREEN/RED>`
- Example: `light 1 NS GREEN`

### Option 2: Headless Simulation (Automated)
```bash
python simulation_demo.py --duration 30 --mode headless
```
- Runs without player input
- Shows statistics every second
- Useful for testing and analysis

### Option 3: Controlled Simulation (Auto-switching lights)
```bash
python simulation_demo.py --duration 30 --mode controlled
```
- Automatically alternates traffic lights every 10 seconds
- Shows statistics and current light state

## Running Tests

```bash
python tests/test_simulator.py -v
```

Expected output: `Ran 23 tests in ~0.01s - OK`

## Game Structure

```
Traffic Simulator
├── Entities
│   ├── Car (moves on roads, waits at lights)
│   ├── Road (connects intersections)
│   ├── Intersection (has traffic lights)
│   └── TrafficLight (GREEN/RED control)
│
├── Engine (handles simulation loop)
│   ├── Spawn cars
│   ├── Update positions
│   ├── Handle lights
│   ├── Calculate score
│   └── Run 10 ticks/second (100ms intervals)
│
└── Game Controller (CLI interface)
    ├── Menu
    ├── HUD
    └── Command processing
```

## Map Layout

Default 2×2 grid:
```
NW (0,100) ---- N Road ---- NE (100,100)
|                                |
W Road                          E Road
|                                |
SW (0,0)  ----- S Road ----- SE (100,0)
```

**Intersections**: 4 total
**Roads**: 4 total (N, S, E, W)
**Lanes**: 2 per road

## Gameplay Tips

1. **Monitor Queue Lengths**
   - Watch the "Queue Length" stat
   - Longer queues = more penalties

2. **Alternate Lights**
   - Don't keep one direction green too long
   - Switch between NS and EW regularly

3. **Anticipate Flow**
   - Adjust lights before congestion builds
   - Look ahead for car spawning patterns

4. **Scoring Strategy**
   - Each car passed: +10 points
   - Each queue car: -2 points
   - Focus on throughput over individual wait times

## Example Commands (In-Game)

```
light 1 NS GREEN      # Intersection 1, North-South, Green
light 2 EW RED        # Intersection 2, East-West, Red
light 3 NS RED        # Intersection 3, North-South, Red
light 4 EW GREEN      # Intersection 4, East-West, Green
quit                  # End game
```

## Files Overview

| File | Purpose |
|------|---------|
| `src/entities.py` | Core game objects (Car, Road, Intersection, TrafficLight) |
| `src/simulation_engine.py` | Main game loop and simulation logic |
| `src/game.py` | CLI game controller and UI |
| `src/config.py` | Configuration constants |
| `simulation_demo.py` | Standalone headless/controlled demo |
| `tests/test_simulator.py` | Unit tests (23 tests) |
| `README.md` | Full documentation |

## Troubleshooting

**ImportError when running tests?**
- Make sure you're in the project root directory
- Python path is configured correctly

**No cars spawning?**
- This is normal - spawning is probabilistic
- Run simulation longer or increase `CAR_SPAWN_PROBABILITY` in config.py

**Score always 0?**
- Try longer simulations (60+ seconds)
- Cars need time to reach intersections and pass through

## Next Steps

- Try different light timings
- Experiment with the controlled simulation
- Modify `config.py` for harder difficulty
- Extend with custom map layouts

---

For full documentation, see [README.md](README.md)
