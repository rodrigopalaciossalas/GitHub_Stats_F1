import random

class Car:
    # F1 Team Colors
    def _get_f1_color(self, index):
        colors = [
            (6, 0, 239),    # Navy
            (255, 40, 0),   # Red
            (0, 210, 190),  # Teal
            (255, 128, 0),  # Orange
            (0, 111, 98),   # Green
            (0, 144, 255),  # Blue
            (0, 90, 255),   # Royal Blue
            (240, 240, 240),# White
            (82, 226, 82),  # Neon Green
            (22, 51, 237),  # Blue
        ]
        return colors[index % len(colors)]

    def __init__(self, repo_data, track_length, car_index):
        # Support both Data Manager and Mock Objects
        if isinstance(repo_data, dict):
            self.name = repo_data["name"]
            self.language = repo_data["language"]
            self.total_stats_commits = repo_data["total_commits"]
        else:
            self.name = repo_data.name
            self.language = repo_data.language
            self.total_stats_commits = repo_data.total_commits
            
        self.track_length = track_length
        self.position = 0.0 
        self.lap = 0
        
        self.is_retired = False
        self.retirement_timer = 0
        
        self.color = self._get_f1_color(car_index)
        
        # Base Speed Calculation (Slower for visualization)
        self.speed = 0.5 + (self.total_stats_commits * 0.0005) 

    def update(self):
        self.position += self.speed
        
        if self.position >= self.track_length:
            self.position -= self.track_length
            self.lap += 1

    def get_coords_index(self):
        return int(self.position) % int(self.track_length)
        
    def get_visual_radius(self):
        return 8
