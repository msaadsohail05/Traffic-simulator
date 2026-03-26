"""
Standalone example: Run a headless simulation
Demonstrates the simulation engine in action
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from simulation_engine import SimulationEngine
from entities import SignalState


def run_headless_simulation(duration=30, verbose=True):
    """
    Run a headless simulation without UI
    
    Args:
        duration: Duration in seconds
        verbose: Print stats every second
    """
    print("="*60)
    print("HEADLESS TRAFFIC SIMULATION")
    print("="*60)
    print(f"Duration: {duration} seconds")
    print()
    
    # Create engine and setup network
    engine = SimulationEngine(game_duration=duration, tick_interval=100)
    engine.setup_grid_network()
    
    # Print initial state
    print("Intersections:")
    for inter_id, inter in engine.intersections.items():
        print(f"  {inter}")
    print("\nRoads:")
    for road_id, road in engine.roads.items():
        print(f"  {road}")
    print()
    print("-"*60)
    print("Starting simulation...")
    print("-"*60 + "\n")
    
    # Start game
    engine.start_game()
    last_second = 0
    
    # Simulation loop
    while engine.game_running:
        # Run tick
        engine.tick()
        
        # Print stats every second
        if verbose:
            current_second = engine.current_tick // engine.ticks_per_second
            if current_second != last_second:
                stats = engine.get_game_stats()
                print(f"[{stats['elapsed_time']:5.1f}s] Score: {stats['score']:6} | "
                      f"Cars: {stats['active_cars']:2} | Passed: {stats['cars_passed']:2} | "
                      f"Queue: {stats['total_queue']:2} | Wait: {stats['total_wait_time']:6.0f}")
                last_second = current_second
    
    # Print final stats
    print()
    print("-"*60)
    print("SIMULATION COMPLETE")
    print("-"*60)
    stats = engine.get_game_stats()
    print(f"Final Score:      {stats['score']}")
    print(f"Cars Passed:      {stats['cars_passed']}")
    print(f"Active Cars:      {stats['active_cars']}")
    print(f"Total Wait Time:  {stats['total_wait_time']:.1f}s")
    print(f"Collisions:       {stats['collisions']}")
    print(f"Final Queue Len:  {stats['total_queue']}")
    print("="*60 + "\n")


def run_controlled_simulation(duration=30):
    """
    Run simulation with manual traffic light control
    
    Args:
        duration: Duration in seconds
    """
    print("="*60)
    print("CONTROLLED TRAFFIC SIMULATION")
    print("="*60)
    print("Automatically alternating traffic lights every 10 seconds")
    print()
    
    engine = SimulationEngine(game_duration=duration, tick_interval=100)
    engine.setup_grid_network()
    engine.start_game()
    
    light_switch_interval = 100  # 10 seconds (100 * 100ms)
    
    while engine.game_running:
        # Switch lights every 10 seconds
        if engine.current_tick % light_switch_interval == 0 and engine.current_tick > 0:
            # Switch lights at all intersections
            for inter_id, inter in engine.intersections.items():
                if engine.current_tick % (light_switch_interval * 2) == 0:
                    engine.set_traffic_light(inter_id, "NS", SignalState.GREEN, 90)
                    engine.set_traffic_light(inter_id, "EW", SignalState.RED, 90)
                else:
                    engine.set_traffic_light(inter_id, "NS", SignalState.RED, 90)
                    engine.set_traffic_light(inter_id, "EW", SignalState.GREEN, 90)
        
        engine.tick()
        
        # Print status every second
        if engine.current_tick % engine.ticks_per_second == 0:
            stats = engine.get_game_stats()
            light_mode = "NS" if (engine.current_tick // light_switch_interval) % 2 == 0 else "EW"
            print(f"[{stats['elapsed_time']:5.1f}s] {light_mode} GREEN | Score: {stats['score']:6} | "
                  f"Queue: {stats['total_queue']:2} | Passed: {stats['cars_passed']:2}")
    
    print()
    stats = engine.get_game_stats()
    print(f"Final Score: {stats['score']}")
    print("="*60 + "\n")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Traffic Simulator - Headless Mode")
    parser.add_argument("--duration", type=int, default=30, help="Simulation duration in seconds")
    parser.add_argument("--mode", choices=["headless", "controlled"], default="headless",
                       help="Simulation mode")
    parser.add_argument("--quiet", action="store_true", help="Reduce output verbosity")
    
    args = parser.parse_args()
    
    if args.mode == "controlled":
        run_controlled_simulation(args.duration)
    else:
        run_headless_simulation(args.duration, verbose=not args.quiet)
