import config
import pygame
import random
from src.visualizer import Visualizer
from src.race_engine import RaceEngine
from src.car import Car

# Mock para simular objeto Repository de PyGithub
class MockRepo:
    def __init__(self, name, lang, total_commits):
        self.name = name
        self.language = lang
        self.total_commits = total_commits
        self.total = total_commits
        
    def get_stats_commit_activity(self):
        # Simular lista de stats (último año)
        # La clase Car suma 'stat.total'
        # Creamos una lista dummy
        return [type('obj', (object,), {'total': int(self.total_commits/52), 'days': [0]*7}) for _ in range(52)]

def main():
    print("--- TEST MODE: F1 Race Animations ---")
    
    # 1. Crear Fake Data (Top Cars)
    # F1 Team Colors Colors logic in Car class: 
    # 0=RedBull, 1=Mercedes, 2=Ferrari, 3=McLaren...
    
    dummy_repos = [
        MockRepo("Red Bull Racing", "Python", 5000),
        MockRepo("Ferrari", "C++", 4800),
        MockRepo("Mercedes AMG", "Java", 4600),
        MockRepo("McLaren", "JavaScript", 4000),
        MockRepo("Aston Martin", "C", 3800),
        MockRepo("Alpine", "Python", 3000),
        MockRepo("Williams", "Rust", 2500),
        MockRepo("AlphaTauri", "Go", 2000),
        MockRepo("Alfa Romeo", "C#", 1500),
        MockRepo("Haas", "Shell", 1000),
    ]
    
    # 2. Setup
    engine = RaceEngine(config.YEAR)
    if not engine.load_circuit():
        print("Error loading circuit")
        return
        
    track_coords = engine.get_track_points()
    track_len = len(track_coords)
    
    cars = []
    for i, repo in enumerate(dummy_repos):
        # Car.__init__ llama a repo.get_stats_commit_activity
        # Necesita car_index para el color
        c = Car(repo, track_len, i)
        # Sobreescribir total exacto para el test
        c.total_stats_commits = repo.total
        # Recalcular velocidad base
        c.speed = 2.0 + (c.total_stats_commits * 0.005) 
        cars.append(c)
        
    vis = Visualizer(track_coords)
    
    running = True
    frame_count = 0
    
    print("Simulación iniciada. Presiona SPACE para forzar un adelantamiento masivo.")
    
    while running:
        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Chaos mode: Randomize a bit
                    for c in cars:
                        c.total_stats_commits = random.randint(1000, 6000)
                    vis.add_event("CHAOS: All stats randomized!")
                elif event.key == pygame.K_RETURN:
                    # SIMULATE RETIREMENT (User Request)
                    # Buscar coche que NO este ya retirado para no buguear
                    active_cars = [c for c in cars if not c.is_retired]
                    if active_cars:
                        sorted_active = sorted(active_cars, key=lambda c: c.total_stats_commits, reverse=True)
                        loser = sorted_active[-1]
                        
                        loser.is_retired = True
                        loser.retirement_timer = 300 # 5 segundos a 60fps
                        vis.add_event(f"CRASH: {loser.name} engine failure!")

        # --- UPDATE TEST LOGIC ---
        frame_count += 1
        
        # 1. Simular Adelantamiento (Cada 2 segundos)
        if frame_count % 120 == 0:
            # Elegir un coche random que no sea el 1ro y darle commits para que suba
            # Orden actual
            sorted_cars = sorted(cars, key=lambda c: c.total_stats_commits, reverse=True)
            if len(sorted_cars) > 1:
                idx = random.randint(1, len(sorted_cars)-1)
                attacker = sorted_cars[idx]
                target = sorted_cars[idx-1]
                
                # Darle suficientes commits para pasar al de adelante + un poco
                diff = target.total_stats_commits - attacker.total_stats_commits
                boost = diff + 50
                attacker.total_stats_commits += boost
                
                vis.add_event(f"TEST: {attacker.name} is pushing hard! (+{boost})")

        # 2. Simular Fallo Técnico (Cada 10 segundos)
        if frame_count % 600 == 0:
             # El último coche se retira y entra uno nuevo
             sorted_cars = sorted(cars, key=lambda c: c.total_stats_commits, reverse=True)
             loser = sorted_cars[-1]
             
             vis.add_event(f"FAILURE: {loser.name} engine smoke!")
             
             # Reemplazar con nuevo (nombre random)
             new_name = f"Rookie_{random.randint(100,999)}"
             loser.name = new_name
             loser.total_stats_commits = random.randint(3000, 4500) # Entra fuerte
             vis.add_event(f"NEW ENTRY: {new_name} joins the track.")

        # update cars logic
        # Detect Overtakes for visualizer event feed
        # (Copiar lógica de main.py si queremos eventos reales de adelantamiento en el feed)
        
        for car in cars:
            # Si está retirado, gestionamos su salida
            if car.is_retired:
                car.retirement_timer -= 1
                if car.retirement_timer <= 0:
                     # Tiempo cumplido, reemplazar coche
                     new_name = f"Rookie_{random.randint(100,999)}"
                     vis.add_event(f"RETIRED: {car.name} removed.")
                     vis.add_event(f"NEW ENTRY: {new_name} joins.")
                     
                     car.name = new_name
                     car.total_stats_commits = random.randint(2000, 3000)
                     car.is_retired = False
                     car.speed = 0.5 + (car.total_stats_commits * 0.0005)
                continue # No se mueve (Speed=0 efecto visual)

            # Update speed based on new commits (Faster check)
            car.speed = 0.5 + (car.total_stats_commits * 0.0005)
            car.update()
            
        vis.draw(cars)
        vis.clock.tick(60)

    vis.close()

if __name__ == "__main__":
    main()
