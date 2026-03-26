#!/usr/bin/env python
"""
Smart Traffic Control Simulator - Main Entry Point
Play the interactive traffic control game
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from game import TrafficSimulatorGame


def main():
    """Main entry point"""
    try:
        game = TrafficSimulatorGame()
        game.run()
    except KeyboardInterrupt:
        print("\n\nGame interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
