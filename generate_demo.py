
import config
from src.visualizer import Visualizer
from src.race_engine import RaceEngine
from src.car import Car
import random

# Mock para simular objeto Repository de PyGithub (copiado de test_race.py)
class MockRepo:
    def __init__(self, name, lang, total_commits):
        self.name = name
        self.language = lang
        self.total_commits = total_commits
        self.total = total_commits
        
    def get_stats_commit_activity(self):
        return [type('obj', (object,), {'total': int(self.total_commits/52), 'days': [0]*7}) for _ in range(52)]

def main():
    print("--- Generating F1 Stats GIF Demo ---")
    
    # Datos de ejemplo
    dummy_repos = [
        MockRepo("Red Bull Racing", "Python", 5000),
        MockRepo("Ferrari", "C++", 4800),
        MockRepo("Mercedes AMG", "Java", 4600),
        MockRepo("McLaren", "JavaScript", 4000),
        # Menos coches para que se vea claro
        MockRepo("Aston Martin", "C", 3800),
        MockRepo("Alpine", "Python", 3000),
    ]
    
    # Cargar circuito
    engine = RaceEngine(config.YEAR)
    if not engine.load_circuit():
        print("Error loading circuit")
        return
        
    track_coords = engine.get_track_points()
    track_len = len(track_coords)
    
    cars = []
    for i, repo in enumerate(dummy_repos):
        c = Car(repo, track_len, i)
        c.total_stats_commits = repo.total
        c.speed = 2.0 + (c.total_stats_commits * 0.005) 
        cars.append(c)
        
    vis = Visualizer(track_coords)
    
    # Capturar 180 frames (aprox 6 segundos a 30fps)
    frames_to_capture = 180
    print(f"Capturing {frames_to_capture} frames...")
    
    for frame in range(frames_to_capture):
        # Update logic
        for car in cars:
            car.speed = 0.5 + (car.total_stats_commits * 0.0005)
            car.update()
        
        # Simular evento visual en frame 60
        if frame == 60:
            vis.add_event("DEMO: Race Started!")
        if frame == 120:
             vis.add_event("DEMO: Max Verstappen leads!")
             
        vis.draw(cars)
        vis.clock.tick(60) # Mantener ritmo de renderizado aunque no afecte GIF directo
        
    print("Saving GIF...")
    vis.save_gif()
    vis.close()
    print("Done!")

if __name__ == "__main__":
    main()
