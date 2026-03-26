"""
Configuration for the traffic simulator
"""

# Game Configuration
GAME_DURATION = 180  # 3 minutes in seconds
TICK_INTERVAL = 100  # milliseconds
TICKS_PER_SECOND = 1000 // TICK_INTERVAL

# Spawning Configuration
CAR_SPAWN_PROBABILITY = 0.30  # 30% chance per tick per road
MAX_CARS_PER_ROAD = 10  # lanes * 5

# Car Configuration
MIN_CAR_SPEED = 0.5
MAX_CAR_SPEED = 2.0

# Traffic Light Configuration
DEFAULT_LIGHT_DURATION = 30  # ticks
DEFAULT_NS_STATE = "GREEN"
DEFAULT_EW_STATE = "RED"

# Scoring Configuration
SCORE_PER_CAR_PASSED = 10
SCORE_PER_WAIT_TICK = -0.5
SCORE_PER_COLLISION = -50
SCORE_PER_QUEUED_CAR = -2

# Road Configuration
ROAD_FOLLOW_DISTANCE = 5  # units to stop before intersection
GREEN_LIGHT_THRESHOLD = 10  # units away to determine if light affects car

# Map Configuration (2x2 Grid)
MAP_INTERSECTIONS = {
    1: {"name": "Northwest", "position": (0, 100)},
    2: {"name": "Northeast", "position": (100, 100)},
    3: {"name": "Southwest", "position": (0, 0)},
    4: {"name": "Southeast", "position": (100, 0)},
}

MAP_ROADS = {
    1: {"name": "North", "start": 1, "end": 2, "length": 100},
    2: {"name": "South", "start": 3, "end": 4, "length": 100},
    3: {"name": "West", "start": 1, "end": 3, "length": 100},
    4: {"name": "East", "start": 2, "end": 4, "length": 100},
}

# Display Configuration
DISPLAY_STATS_INTERVAL = 1  # seconds
DISPLAY_CLEAR_SCREEN = True

# Simulation Modes
SIMULATION_MODES = {
    "headless": "Run without UI, output statistics",
    "controlled": "Run with automatic traffic light control",
    "interactive": "Run with player control (CLI)",
}
