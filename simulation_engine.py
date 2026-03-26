"""
Core simulation engine for traffic simulator
Handles the game loop, car spawning, movement, and scoring
"""
import random
from typing import Dict, List
try:
    from .entities import Car, Road, Intersection, TrafficLight, Direction, SignalState
except ImportError:
    from entities import Car, Road, Intersection, TrafficLight, Direction, SignalState


class SimulationEngine:
    """Main simulation engine that runs the traffic simulator"""
    
    def __init__(self, game_duration: int = 180, tick_interval: int = 100):
        """
        Initialize the simulation engine
        
        Args:
            game_duration: Duration of game in seconds (default 3 minutes = 180s)
            tick_interval: Milliseconds between ticks (default 100ms)
        """
        self.game_duration = game_duration
        self.tick_interval = tick_interval
        self.ticks_per_second = 1000 // tick_interval
        self.total_ticks = game_duration * self.ticks_per_second
        self.current_tick = 0
        self.game_running = False
        
        # Game entities
        self.roads: Dict[int, Road] = {}
        self.intersections: Dict[int, Intersection] = {}
        self.all_cars: List[Car] = []
        
        # Scoring
        self.score = 0
        self.cars_passed = 0
        self.total_wait_time = 0
        self.collisions = 0
        
    def create_road(self, length: float, lanes: int, start_int_id: int, end_int_id: int) -> Road:
        """Create and register a road"""
        road = Road(length, lanes, start_int_id, end_int_id)
        self.roads[road.id] = road
        return road
    
    def create_intersection(self, x: float, y: float) -> Intersection:
        """Create and register an intersection"""
        intersection = Intersection((x, y))
        self.intersections[intersection.id] = intersection
        return intersection
    
    def setup_grid_network(self):
        """Setup a simple 2x2 grid intersection network"""
        # Create 4 intersections in a grid
        int_nw = self.create_intersection(0, 100)    # Northwest
        int_ne = self.create_intersection(100, 100)  # Northeast
        int_sw = self.create_intersection(0, 0)      # Southwest
        int_se = self.create_intersection(100, 0)    # Southeast
        
        # Create roads connecting them
        # Horizontal roads
        road_n = self.create_road(100, 2, int_nw.id, int_ne.id)  # North
        road_s = self.create_road(100, 2, int_sw.id, int_se.id)  # South
        
        # Vertical roads
        road_w = self.create_road(100, 2, int_nw.id, int_sw.id)  # West
        road_e = self.create_road(100, 2, int_ne.id, int_se.id)  # East
        
        # Connect intersections
        int_nw.add_outgoing_road(road_n.id)
        int_nw.add_outgoing_road(road_w.id)
        int_ne.add_incoming_road(road_n.id)
        int_ne.add_outgoing_road(road_e.id)
        int_sw.add_incoming_road(road_w.id)
        int_sw.add_outgoing_road(road_s.id)
        int_se.add_incoming_road(road_s.id)
        int_se.add_incoming_road(road_e.id)
    
    def spawn_cars(self):
        """Spawn random cars on roads"""
        # 30% chance to spawn a car each tick on each road
        for road in self.roads.values():
            if random.random() < 0.30 and len(road.cars) < road.lanes * 5:
                speed = random.uniform(0.5, 2.0)  # Random speed
                # Spawn at start of road
                start_int = self.intersections[road.start_intersection_id]
                position = start_int.position
                
                # Determine direction based on road
                if road.start_intersection_id < road.end_intersection_id:
                    direction = Direction.EAST
                else:
                    direction = Direction.WEST
                
                car = Car(speed, position, direction)
                road.add_car(car)
                self.all_cars.append(car)
    
    def update_car_positions(self):
        """Update positions of all cars and check for collisions"""
        for road in self.roads.values():
            for car in road.cars[:]:  # Iterate over copy
                # Check if car should stop at intersection
                end_int = self.intersections[road.end_intersection_id]
                distance_to_intersection = abs(car.position[0] - end_int.position[0]) + abs(car.position[1] - end_int.position[1])
                
                # Determine if light is green based on car's direction
                is_green = False
                if car.direction in [Direction.NORTH, Direction.SOUTH]:
                    is_green = end_int.get_ns_state() == SignalState.GREEN
                else:  # EAST or WEST
                    is_green = end_int.get_ew_state() == SignalState.GREEN
                
                # Stop car if light is red and close to intersection
                if distance_to_intersection < 5 and not is_green:
                    car.is_stopped = True
                elif distance_to_intersection > 10:
                    car.is_stopped = False
                
                # Move car
                car.move()
                car.update_waiting_time()
                
                # Check if car passed intersection
                if distance_to_intersection < 2:
                    road.remove_car(car)
                    self.all_cars.remove(car)
                    self.cars_passed += 1
                    self.total_wait_time += car.waiting_time
    
    def update_intersections(self):
        """Update all intersection lights"""
        for intersection in self.intersections.values():
            intersection.update_lights()
    
    def calculate_score(self):
        """Calculate the current score"""
        # Points for cars that passed
        flow_points = self.cars_passed * 10
        
        # Penalty for waiting time
        wait_penalty = self.total_wait_time * 0.5
        
        # Penalty for collisions
        collision_penalty = self.collisions * 50
        
        # Penalty for current queue length
        total_queue = sum(road.get_queue_length() for road in self.roads.values())
        congestion_penalty = total_queue * 2
        
        self.score = max(0, flow_points - wait_penalty - collision_penalty - congestion_penalty)
    
    def get_game_stats(self) -> Dict:
        """Get current game statistics"""
        return {
            "tick": self.current_tick,
            "elapsed_time": self.current_tick / self.ticks_per_second,
            "score": int(self.score),
            "cars_passed": self.cars_passed,
            "active_cars": len(self.all_cars),
            "total_wait_time": self.total_wait_time,
            "collisions": self.collisions,
            "total_queue": sum(road.get_queue_length() for road in self.roads.values()),
        }
    
    def tick(self):
        """Execute one simulation tick (100ms)"""
        if not self.game_running:
            return
        
        # Core game loop
        self.spawn_cars()
        self.update_car_positions()
        self.update_intersections()
        self.calculate_score()
        
        self.current_tick += 1
        
        # Check if game is over
        if self.current_tick >= self.total_ticks:
            self.game_running = False
    
    def start_game(self):
        """Start the simulation"""
        self.game_running = True
        self.current_tick = 0
    
    def stop_game(self):
        """Stop the simulation"""
        self.game_running = False
    
    def set_traffic_light(self, intersection_id: int, light_type: str, state: SignalState, duration: int = None):
        """
        Manually set a traffic light
        
        Args:
            intersection_id: ID of the intersection
            light_type: "NS" or "EW"
            state: Signal state to set
            duration: Optional duration for this state
        """
        intersection = self.intersections.get(intersection_id)
        if intersection:
            if light_type == "NS":
                intersection.ns_light.set_state(state, duration)
            elif light_type == "EW":
                intersection.ew_light.set_state(state, duration)
    
    def __repr__(self):
        stats = self.get_game_stats()
        return f"SimulationEngine(tick={stats['tick']}, score={stats['score']}, cars={stats['active_cars']})"
