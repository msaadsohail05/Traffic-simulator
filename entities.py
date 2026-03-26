"""
Core entities for the traffic simulator
"""
from enum import Enum
from typing import List, Tuple


class Direction(Enum):
    """Car direction of travel"""
    NORTH = "N"
    SOUTH = "S"
    EAST = "E"
    WEST = "W"


class SignalState(Enum):
    """Traffic light signal states"""
    GREEN = "GREEN"
    RED = "RED"
    YELLOW = "YELLOW"


class Car:
    """Represents a car in the traffic simulation"""
    
    _car_id_counter = 0
    
    def __init__(self, speed: float, position: Tuple[float, float], direction: Direction):
        """
        Initialize a car
        
        Args:
            speed: Speed of the car in units per tick
            position: (x, y) position
            direction: Direction of travel
        """
        Car._car_id_counter += 1
        self.id = Car._car_id_counter
        self.speed = speed
        self.position = position
        self.direction = direction
        self.waiting_time = 0
        self.is_stopped = False
        
    def move(self):
        """Move the car in its direction"""
        if self.is_stopped:
            return
        
        x, y = self.position
        
        if self.direction == Direction.NORTH:
            self.position = (x, y + self.speed)
        elif self.direction == Direction.SOUTH:
            self.position = (x, y - self.speed)
        elif self.direction == Direction.EAST:
            self.position = (x + self.speed, y)
        elif self.direction == Direction.WEST:
            self.position = (x - self.speed, y)
    
    def update_waiting_time(self):
        """Increase waiting time if stopped"""
        if self.is_stopped:
            self.waiting_time += 1
    
    def __repr__(self):
        return f"Car(id={self.id}, pos={self.position}, dir={self.direction.value}, wait={self.waiting_time})"


class Road:
    """Represents a road segment in the network"""
    
    _road_id_counter = 0
    
    def __init__(self, length: float, lanes: int, start_intersection_id: int, end_intersection_id: int):
        """
        Initialize a road
        
        Args:
            length: Length of the road
            lanes: Number of lanes
            start_intersection_id: ID of starting intersection
            end_intersection_id: ID of ending intersection
        """
        Road._road_id_counter += 1
        self.id = Road._road_id_counter
        self.length = length
        self.lanes = lanes
        self.start_intersection_id = start_intersection_id
        self.end_intersection_id = end_intersection_id
        self.cars: List[Car] = []
    
    def add_car(self, car: Car):
        """Add a car to this road"""
        self.cars.append(car)
    
    def remove_car(self, car: Car):
        """Remove a car from this road"""
        if car in self.cars:
            self.cars.remove(car)
    
    def get_queue_length(self) -> int:
        """Get number of stopped cars waiting at red light"""
        return sum(1 for car in self.cars if car.is_stopped)
    
    def __repr__(self):
        return f"Road(id={self.id}, length={self.length}, lanes={self.lanes}, cars={len(self.cars)})"


class TrafficLight:
    """Represents a traffic light at an intersection"""
    
    def __init__(self, state: SignalState = SignalState.RED, duration: int = 30):
        """
        Initialize a traffic light
        
        Args:
            state: Initial signal state
            duration: How long to show current state (in ticks)
        """
        self.state = state
        self.duration = duration
        self.timer = 0
    
    def update(self):
        """Update the traffic light timer"""
        self.timer += 1
        
        if self.timer >= self.duration:
            self.timer = 0
            # Toggle state
            if self.state == SignalState.GREEN:
                self.state = SignalState.RED
            elif self.state == SignalState.RED:
                self.state = SignalState.GREEN
    
    def set_state(self, state: SignalState, duration: int = None):
        """Manually set the signal state"""
        self.state = state
        self.timer = 0
        if duration:
            self.duration = duration
    
    def __repr__(self):
        return f"TrafficLight(state={self.state.value}, timer={self.timer}/{self.duration})"


class Intersection:
    """Represents an intersection in the road network"""
    
    _intersection_id_counter = 0
    
    def __init__(self, position: Tuple[float, float]):
        """
        Initialize an intersection
        
        Args:
            position: (x, y) position of the intersection
        """
        Intersection._intersection_id_counter += 1
        self.id = Intersection._intersection_id_counter
        self.position = position
        self.incoming_roads: List[int] = []  # Road IDs
        self.outgoing_roads: List[int] = []  # Road IDs
        self.ns_light = TrafficLight(SignalState.GREEN, duration=30)  # North-South
        self.ew_light = TrafficLight(SignalState.RED, duration=30)    # East-West
        self.signal_state = "NS"  # Which direction has the light
    
    def add_incoming_road(self, road_id: int):
        """Add an incoming road"""
        if road_id not in self.incoming_roads:
            self.incoming_roads.append(road_id)
    
    def add_outgoing_road(self, road_id: int):
        """Add an outgoing road"""
        if road_id not in self.outgoing_roads:
            self.outgoing_roads.append(road_id)
    
    def update_lights(self):
        """Update both traffic lights"""
        self.ns_light.update()
        self.ew_light.update()
    
    def switch_signal(self):
        """Switch between NS and EW signal"""
        if self.signal_state == "NS":
            self.signal_state = "EW"
        else:
            self.signal_state = "NS"
    
    def get_ns_state(self) -> SignalState:
        """Get North-South light state"""
        return self.ns_light.state
    
    def get_ew_state(self) -> SignalState:
        """Get East-West light state"""
        return self.ew_light.state
    
    def __repr__(self):
        return f"Intersection(id={self.id}, pos={self.position}, NS={self.ns_light.state.value}, EW={self.ew_light.state.value})"
