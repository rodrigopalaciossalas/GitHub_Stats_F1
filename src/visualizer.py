import pygame
import config
import imageio
import numpy as np
import random

class Visualizer:
    def __init__(self, track_coords, circuit_name="Unknown"):
        pygame.init()
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        pygame.display.set_caption("GitHub F1 Stats Race - Live")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 16, bold=True)
        self.title_font = pygame.font.SysFont("Arial", 28, bold=True)
        self.small_font = pygame.font.SysFont("Arial", 12)
        
        self.track_coords = track_coords
        self.circuit_name = circuit_name
        self.frames = []
        self.events = [] 
        self.particles = {} 
        
        self.scale_factor = 4
        self.hd_res = (config.SCREEN_WIDTH * self.scale_factor, config.SCREEN_HEIGHT * self.scale_factor)
        self.track_surface = pygame.Surface(self.hd_res)
        
    def draw(self, cars):
        self.track_surface.fill((20, 20, 20)) 
        
        if len(self.track_coords) > 1:
            scaled_points = (self.track_coords * self.scale_factor).tolist()
            if len(scaled_points) > 2:
                w_base = 14 * self.scale_factor
                r_base = 7 * self.scale_factor
                pygame.draw.lines(self.track_surface, (220, 220, 220), True, scaled_points, w_base)
                for p in scaled_points:
                    pygame.draw.circle(self.track_surface, (220, 220, 220), (int(p[0]), int(p[1])), r_base)

                w_road = 10 * self.scale_factor
                r_road = 5 * self.scale_factor
                pygame.draw.lines(self.track_surface, (40, 40, 45), True, scaled_points, w_road)
                for p in scaled_points:
                    pygame.draw.circle(self.track_surface, (40, 40, 45), (int(p[0]), int(p[1])), r_road)
            
            start_x, start_y = scaled_points[0]
            pygame.draw.line(self.track_surface, (255, 255, 255), (start_x-(8*self.scale_factor), start_y), (start_x+(8*self.scale_factor), start_y), 3*self.scale_factor)
            
        smooth_view = pygame.transform.smoothscale(self.track_surface, (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        self.screen.blit(smooth_view, (0, 0))

        for car in cars:
            idx = car.get_coords_index()
            if idx < len(self.track_coords):
                x, y = self.track_coords[idx]
                
                if getattr(car, 'is_retired', False):
                     pygame.draw.circle(self.screen, (30, 30, 30), (int(x), int(y)), 8)
                     
                     if car.name not in self.particles:
                         self.particles[car.name] = []
                     
                     p_list = self.particles[car.name]
                     
                     if random.random() < 0.2: 
                         p_list.append({
                             'x': x, 'y': y, 
                             'vx': random.uniform(-0.5, 0.5), 'vy': random.uniform(-1.5, -0.5), 
                             'life': 60, 'color': (100, 100, 100), 'size': random.randint(4, 7)
                         })
                     if random.random() < 0.1:
                         p_list.append({
                             'x': x + random.uniform(-3, 3), 'y': y + random.uniform(-3, 3),
                             'vx': random.uniform(-0.3, 0.3), 'vy': random.uniform(-1.0, 0.0),
                             'life': 30, 'color': (255, random.randint(60, 140), 0), 'size': random.randint(3, 5)
                         })
                         
                     for p in p_list[:]:
                         p['x'] += p['vx']
                         p['y'] += p['vy']
                         p['life'] -= 1
                         p['size'] += 0.05
                         
                         if p['life'] <= 0:
                             p_list.remove(p)
                             continue
                             
                         pygame.draw.circle(self.screen, p['color'], (int(p['x']), int(p['y'])), int(p['size']))
                         
                else:
                    if car.name in self.particles:
                        del self.particles[car.name]
                        
                    radius = car.get_visual_radius()
                    pygame.draw.circle(self.screen, car.color, (int(x), int(y)), radius)

        self._draw_ui(cars)

        pygame.display.flip()
        
        view = pygame.surfarray.array3d(self.screen)
        view = view.transpose([1, 0, 2])
        self.frames.append(view)

    def _draw_ui(self, cars):
        panel_x = config.SCREEN_WIDTH - 300
        stats_text = self.font.render(f"Circuit: {self.circuit_name}", True, (150, 150, 150))
        self.screen.blit(stats_text, (panel_x + 20, 50))
        
        event_x = 20
        e_y = 50
        title_e = self.font.render("RACE CONTROL", True, (255, 255, 255))
        self.screen.blit(title_e, (event_x, 20))
        
        for i, msg in enumerate(self.events): 
             col = (255, 255, 255)
             lbl = self.small_font.render(f"> {msg}", True, col)
             self.screen.blit(lbl, (event_x, e_y + (i*25)))

        sorted_cars = sorted(cars, key=lambda c: c.total_stats_commits, reverse=True)
        
        if not hasattr(self, 'car_row_y'):
            self.car_row_y = {}
            
        base_y = 100
        row_height = 40
        
        self.screen.blit(self.font.render("Pos", True, (100,100,100)), (panel_x + 10, base_y - 20))
        self.screen.blit(self.font.render("Repository", True, (100,100,100)), (panel_x + 50, base_y - 20))
        
        for i, car in enumerate(sorted_cars[:12]):
            target_y = base_y + (i * row_height)
            
            current_y = self.car_row_y.get(car.name, target_y)
            
            diff = target_y - current_y
            if abs(diff) < 0.5:
                current_y = target_y
            else:
                current_y += diff * 0.1
            
            self.car_row_y[car.name] = current_y
           
            color = car.color
            name = car.name
            if len(name) > 22: name = name[:19] + "..."
            
            rank_text = self.font.render(f"{i+1}.", True, (255, 255, 255))
            self.screen.blit(rank_text, (panel_x + 10, current_y))
            
            pygame.draw.rect(self.screen, color, (panel_x + 35, current_y + 2, 12, 12))
            
            name_text = self.font.render(name, True, (255, 255, 255))
            self.screen.blit(name_text, (panel_x + 55, current_y))
            
            comm_text = self.font.render(f"{car.total_stats_commits}", True, (255, 200, 0))
            self.screen.blit(comm_text, (panel_x + 240, current_y))

    def add_event(self, text):
        """Añade un mensaje al feed (FIFO, Max 5)."""
        self.events.append(text)
        if len(self.events) > 5:
            self.events.pop(0)

    def save_gif(self):
        if not self.frames:
            print("No frames to save.")
            return
            
        print(f"Saving GIF ({len(self.frames)} frames)... this might take a moment.")
        try:
            imageio.mimsave(config.OUTPUT_GIF_NAME, self.frames, fps=config.FPS, loop=0)
            print(f"GIF saved to {config.OUTPUT_GIF_NAME}")
        except Exception as e:
            print(f"Error saving GIF: {e}")
        
    def close(self):
        pygame.quit()
