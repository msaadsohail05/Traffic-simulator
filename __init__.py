"""
Traffic Simulator Package
Smart Traffic Control Simulation Game
"""

__version__ = "1.0.0"
__author__ = "Some Great Fastians"

from src.entities import Car, Road, Intersection, TrafficLight, Direction, SignalState
from src.simulation_engine import SimulationEngine
from src.game import TrafficSimulatorGame

__all__ = [
    "Car",
    "Road",
    "Intersection",
    "TrafficLight",
    "Direction",
    "SignalState",
    "SimulationEngine",
    "TrafficSimulatorGame",
]
