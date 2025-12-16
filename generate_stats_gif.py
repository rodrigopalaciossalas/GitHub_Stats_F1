
import config
from src import data_manager
from src.race_engine import RaceEngine
from src.car import Car
from src.visualizer import Visualizer
import sys
import os

def main():
    print("--- Generating F1 Stats GIF (Production) ---")
    
    # 1. Check for Token (Required by data_manager)
    if not config.GITHUB_TOKEN:
        print("WARNING: GITHUB_TOKEN not found in environment. Data fetch might fail if not authenticated.")
    
    # 2. Get Data
    try:
        # Note: verify_connection() prints successful login
        if not data_manager.verify_connection():
             # If check fails but we want to try anyway (maybe connection error handling is strict), we could continue.
             # But let's respect the check.
             print("Authentication failed. Check GITHUB_TOKEN.")
             sys.exit(1)
             
        repos_stats = data_manager.get_repository_stats()
        if not repos_stats:
            print("No repositories found or error during fetch.")
            sys.exit(1)
            
    except Exception as e:
        print(f"Error fetching data: {e}")
        sys.exit(1)
        
    print(f"Loaded {len(repos_stats)} repositories for the race.")

    # 3. Load Circuit
    engine = RaceEngine(config.YEAR)
    if not engine.load_circuit():
        print("Error loading circuit. Defaulting/Exiting.")
        sys.exit(1)
        
    track_coords = engine.get_track_points()
    track_len = len(track_coords)
    
    # 4. Initialize Cars
    cars = []
    
    # Sort by total_commits desc to get the fastest repos
    sorted_repos = sorted(repos_stats, key=lambda x: x['total_commits'], reverse=True)
    # Limit to top 10
    grid_data = sorted_repos[:10]
    
    print(f"Race Grid: {len(grid_data)} cars.")
    
    for i, repo in enumerate(grid_data):
        car = Car(repo, track_len, i)
        cars.append(car)
        
    # 5. Initialize Visualizer
    # SDL_VIDEODRIVER=dummy should be set in environment for headless
    vis = Visualizer(track_coords)
    
    # 6. Run Simulation for GIF
    # Calculate duration based on the slowest car (last in grid) to complete 1 lap
    # Speed formula in Car: 0.5 + (commits * 0.0005)
    slowest_car = cars[-1]
    # Time = Distance / Speed
    required_frames = int(track_len / slowest_car.speed)
    
    # Add buffer (e.g., 2 seconds) to show the finish line crossing clearly
    buffer_frames = 60 
    frames_to_capture = required_frames + buffer_frames
    
    print(f"Slowest Car: {slowest_car.name} (Speed: {slowest_car.speed:.4f})")
    print(f"Track Length: {track_len}")
    print(f"Simulating {frames_to_capture} frames (~{frames_to_capture/config.FPS:.1f}s) for 1 full lap.")
    
    for frame in range(frames_to_capture):
        # Update Cars
        for car in cars:
            # We use the same update logic as main.py but without retirement/overtake logic complexity for the GIF
            # or maybe we DO want it? 
            # Let's keep it simple: Move cars based on speed.
            
            # Recalculate speed (constant here, but good practice if logic changes)
            # Car speed in Car.__init__ is: 0.5 + (commits * 0.0005)
            # main.py updates it too.
            car.update()
            
        # Draw
        vis.draw(cars)
        
        # Add visual flair events occasionally
        if frame == 30:
             vis.add_event(f"START: Race for {config.GITHUB_USERNAME}")
        
        vis.clock.tick(60) # Sync speed
        
    # 7. Save
    vis.save_gif()
    vis.close()
    print("Generation Complete.")

if __name__ == "__main__":
    main()
