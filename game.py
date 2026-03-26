"""
Game controller and CLI interface for traffic simulator
"""
import time
import os
try:
    from .simulation_engine import SimulationEngine
    from .entities import SignalState
except ImportError:
    from simulation_engine import SimulationEngine
    from entities import SignalState


class TrafficSimulatorGame:
    """Main game controller"""
    
    def __init__(self):
        self.engine = SimulationEngine(game_duration=180, tick_interval=100)
        self.engine.setup_grid_network()
        self.running = False
    
    def display_title(self):
        """Display game title"""
        print("\n" + "="*60)
        print("      SMART TRAFFIC CONTROL SIMULATOR")
        print("="*60)
        print("Objective: Control traffic lights to maximize flow")
        print("Duration: 3 minutes")
        print("="*60 + "\n")
    
    def display_menu(self):
        """Display main menu"""
        print("\n--- MAIN MENU ---")
        print("1. Start Game")
        print("2. Settings")
        print("3. Help")
        print("4. Exit")
        print("\nEnter choice (1-4): ", end="")
    
    def display_game_hud(self, clear_screen=True):
        """Display heads-up display during gameplay"""
        if clear_screen:
            os.system('cls' if os.name == 'nt' else 'clear')
        stats = self.engine.get_game_stats()
        
        print("\n" + "="*60)
        print("  TRAFFIC SIMULATOR - IN PROGRESS")
        print("="*60)
        print(f"Time: {stats['elapsed_time']:.1f}s / {self.engine.game_duration}s")
        print(f"Score: {stats['score']}")
        print(f"Cars Passed: {stats['cars_passed']}")
        print(f"Active Cars: {stats['active_cars']}")
        print(f"Queue Length: {stats['total_queue']}")
        print(f"Total Wait Time: {stats['total_wait_time']}")
        print(f"Collisions: {stats['collisions']}")
        print("="*60)
        print("\nIntersections:")
        for int_id, intersection in self.engine.intersections.items():
            print(f"  {intersection}")
        print("\n--- CONTROLS ---")
        print("Commands:")
        print("  light <int_id> <NS/EW> <GREEN/RED> - Set traffic light")
        print("  quit - Exit game")
        print("\nExample: light 1 NS GREEN\n")
    
    def process_command(self, command: str):
        """Process player command during game"""
        parts = command.strip().split()
        
        if not parts:
            return
        
        if parts[0].lower() == "quit":
            self.engine.stop_game()
            return
        
        if parts[0].lower() == "light" and len(parts) >= 4:
            try:
                int_id = int(parts[1])
                light_type = parts[2].upper()
                state = SignalState[parts[3].upper()]
                self.engine.set_traffic_light(int_id, light_type, state, duration=15)
                print(f"✓ Set intersection {int_id} {light_type} to {state.value}")
            except (ValueError, KeyError, IndexError):
                print("✗ Invalid command. Use: light <int_id> <NS/EW> <GREEN/RED>")
            return
        
        print(f"✗ Unknown command: {command}")
    
    def run_game(self):
        """Main game loop"""
        self.engine.start_game()
        tick_count = 0
        
        print("\n🎮 Game Started! Control traffic lights to maximize flow.\n")
        
        while self.engine.game_running:
            # Display HUD once at the start
            if tick_count == 0:
                self.display_game_hud()
            
            # Get user input
            try:
                command = input("Enter command: ").strip()
                if command:
                    self.process_command(command)
                    # Redisplay HUD after command (without clearing)
                    self.display_game_hud(clear_screen=False)
            except (EOFError, KeyboardInterrupt):
                print("\nExiting game...")
                self.engine.stop_game()
                break
            
            # Run multiple simulation ticks to simulate time passing
            for _ in range(10):  # Run 10 ticks (1 second) per input
                if not self.engine.game_running:
                    break
                self.engine.tick()
                tick_count += 1
            
            # Show periodic stats
            if tick_count % 50 == 0:  # Every 5 seconds
                stats = self.engine.get_game_stats()
                print(f"[Time: {stats['elapsed_time']:.1f}s] Score: {stats['score']} | Cars: {stats['active_cars']} | Queue: {stats['total_queue']}")
        
        self.display_game_over()
    
    def display_game_over(self):
        """Display game over screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
        stats = self.engine.get_game_stats()
        
        print("\n" + "="*60)
        print("              GAME OVER")
        print("="*60)
        print(f"Final Score: {stats['score']}")
        print(f"Cars Passed: {stats['cars_passed']}")
        print(f"Total Wait Time: {stats['total_wait_time']:.1f}s")
        print(f"Collisions: {stats['collisions']}")
        print("="*60 + "\n")
    
    def display_help(self):
        """Display help information"""
        print("\n" + "="*60)
        print("              HELP")
        print("="*60)
        print("""
OBJECTIVE:
Control traffic lights at intersections for 3 minutes to:
  • Maximize traffic flow (+points)
  • Minimize congestion (-points)
  • Reduce waiting time (-points)
  • Prevent collisions (-points)

GAMEPLAY:
1. Cars spawn randomly from roads
2. They move toward intersections
3. You control traffic lights (NS/EW)
4. System tracks flow, delays, and collisions

SCORING:
  • +10 points per car that passes through
  • -0.5 points per tick of wait time
  • -50 points per collision
  • -2 points per car in queue

COMMANDS:
  light <intersection_id> <NS/EW> <GREEN/RED>
    Example: light 1 NS GREEN
    
  quit - Exit game early

TIPS:
  • Alternate traffic lights to prevent gridlock
  • Monitor queue lengths
  • Plan light changes ahead of time
  • Balance flow between directions

ENTITIES:
  • Car: Moves on roads, waits at lights
  • Road: Connects intersections, has lanes
  • Intersection: Has traffic lights (NS & EW)
  • Traffic Light: GREEN or RED signal
        """)
        print("="*60 + "\n")
    
    def display_settings(self):
        """Display settings menu"""
        print("\n" + "="*60)
        print("              SETTINGS")
        print("="*60)
        print("1. Game Duration (current: 3 minutes)")
        print("2. Difficulty")
        print("3. Back to Main Menu")
        print("\nNote: Settings customization coming in future updates")
        print("="*60 + "\n")
    
    def run(self):
        """Main game loop"""
        self.display_title()
        
        while True:
            self.display_menu()
            choice = input().strip()
            
            if choice == "1":
                self.run_game()
            elif choice == "2":
                self.display_settings()
            elif choice == "3":
                self.display_help()
            elif choice == "4":
                print("Thanks for playing! Goodbye!\n")
                break
            else:
                print("✗ Invalid choice. Please enter 1-4.")


def main():
    """Entry point"""
    game = TrafficSimulatorGame()
    game.run()


if __name__ == "__main__":
    main()
