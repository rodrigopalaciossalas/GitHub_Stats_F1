import config
from src import data_manager
from src.race_engine import RaceEngine
from src.car import Car
from src.visualizer import Visualizer
import sys
import os

def main():
    print("--- Generating F1 Stats GIF (Production) ---")
    
    if not config.GITHUB_TOKEN:
        print("WARNING: GITHUB_TOKEN not found in environment. Data fetch might fail if not authenticated.")
    
    try:
        if not data_manager.verify_connection():
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

    engine = RaceEngine(config.YEAR)
    if not engine.load_circuit():
        print("Error loading circuit. Defaulting/Exiting.")
        sys.exit(1)
        
    track_coords = engine.get_track_points()
    track_len = len(track_coords)
    
    cars = []
    
    sorted_repos = sorted(repos_stats, key=lambda x: x['total_commits'], reverse=True)
    grid_data = sorted_repos[:10]
    
    print(f"Race Grid: {len(grid_data)} cars.")
    
    for i, repo in enumerate(grid_data):
        car = Car(repo, track_len, i)
        cars.append(car)
        
    vis = Visualizer(track_coords, engine.circuit_name)
    
    slowest_car = cars[-1]
    required_frames = int(track_len / slowest_car.speed)
    
    buffer_frames = 60 
    frames_to_capture = required_frames + buffer_frames
    
    print(f"Slowest Car: {slowest_car.name} (Speed: {slowest_car.speed:.4f})")
    print(f"Track Length: {track_len}")
    print(f"Simulating {frames_to_capture} frames (~{frames_to_capture/config.FPS:.1f}s) for 1 full lap.")
    
    for frame in range(frames_to_capture):
        for car in cars:
            car.update()
            
        vis.draw(cars)
        
        if frame == 30:
             vis.add_event(f"START: Race for {config.GITHUB_USERNAME}")
        
        vis.clock.tick(60)
        
    vis.save_gif()
    vis.close()
    print("Generation Complete.")

if __name__ == "__main__":
    main()
