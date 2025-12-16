import random

class Car:
    def _get_f1_color(self, index):
        colors = [
            (6, 0, 239),
            (255, 40, 0),
            (0, 210, 190),
            (255, 128, 0),
            (0, 111, 98),
            (0, 144, 255),
            (0, 90, 255),
            (240, 240, 240),
            (82, 226, 82),
            (22, 51, 237),
        ]
        return colors[index % len(colors)]

    def __init__(self, repo_data, track_length, car_index):
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
