import config
import data_manager
import race_engine
from car import Car
from visualizer import Visualizer
import sys
import pygame
import random

def main():
    print("--- GitHub F1 Race ---")
    
    # 1. Obtener Datos
    if not data_manager.verify_connection():
        print("Error: No se puede conectar a GitHub.")
        return

    repos_stats = data_manager.get_repository_stats()
    if not repos_stats:
        print("No se encontraron repositorios.")
        return

    # 2. Cargar Circuito
    engine = race_engine.RaceEngine(config.YEAR)
    if not engine.load_circuit():
        print("Error cargando circuito.")
        return
        
    track_coords = engine.get_track_points()
    markers = engine.get_month_markers()

    # 3. Inicializar Coches
    cars = []
    track_len = len(track_coords)
    # Solo tomamos los primeros 20 coches para la parrilla de F1 (10 equipos x 2)
    # O si el usuario tiene menos, pues menos.
    grid_data = repos_stats[:20]
    
    for i, repo in enumerate(grid_data):
        # Pasamos índice 'i' para asignar equipo
        car = Car(repo, track_len, i)
        cars.append(car)
        
    # 4. Simulación Visual (Bucle Infinito)
    vis = Visualizer(track_coords)
    
    print("Iniciando carrera continua...")
    running = True
    
    # Para detectar adelantamientos (rankings)
    # Lista de IDs ordenados por commits
    previous_rank = sorted(cars, key=lambda c: c.total_stats_commits, reverse=True)
    
    while running:
        # Check eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                 pass
                 # No manual controls in Live Mode

        # Detectar Adelantamientos (Visual feed)
        current_rank = sorted(cars, key=lambda c: c.total_stats_commits, reverse=True)
        
        for i, car in enumerate(current_rank):
            old_idx = -1
            for idx, old_c in enumerate(previous_rank):
                if old_c.name == car.name:
                    old_idx = idx
                    break
            
            if i < old_idx: # Subió de puesto
                 vis.add_event(f"OVERTAKE: {car.name} P{old_idx+1} -> P{i+1}")
                  
        previous_rank = current_rank[:]

        # Actualizar Coches
        for car in cars:
             # Gestionar retiro
            if getattr(car, 'is_retired', False):
                car.retirement_timer -= 1
                if car.retirement_timer <= 0:
                     # Reemplazo por Rookie
                     new_name = f"Rookie_{random.randint(100,999)}"
                     vis.add_event(f"RETIRED: {car.name} replaced by {new_name}")
                     car.name = new_name
                     car.total_stats_commits = random.randint(100, 1000) # Reset simple
                     car.is_retired = False
                     car.speed = 0.5 + (car.total_stats_commits * 0.0005)
                continue

            # Velocidad basada en Commits (Lenta)
            car.speed = 0.5 + (car.total_stats_commits * 0.0005)
            car.update() 
        
        # Dibujar
        vis.draw(cars)
        
        # 60 FPS
        vis.clock.tick(60)
            
    vis.close()
    print("Simulación finalizada.")

if __name__ == "__main__":
    main()
