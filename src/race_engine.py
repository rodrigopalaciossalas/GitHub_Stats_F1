import fastf1
import numpy as np
import pandas as pd
import config

# Habilitar caché para no descargar datos cada vez
fastf1.Cache.enable_cache('cache') 

class RaceEngine:
    def __init__(self, year=2023):
        # Lista de circuitos para rotación aleatoria (Off-Season)
        self.circuits = ["Monaco", "Spa", "Monza", "Silverstone", "Suzuka", "Bahrain", "Zandvoort"]
        # Selección aleatoria
        self.circuit_name = np.random.choice(self.circuits)
        self.year = year
        self.track_coords = None
        self.track_length = 0
        
    def load_circuit(self):
        """Carga los datos de telemetría del circuito especificado."""
        print(f"Cargando datos del circuito: {self.circuit_name} {self.year}...")
        try:
            # Usamos la sesión de clasificación (Qualifying) que suele ser la más rápida/limpia
            session = fastf1.get_session(self.year, self.circuit_name, 'Q')
            session.load()
            
            # Obtenemos la vuelta más rápida de cualquier piloto para tener la trazada ideal
            lap = session.laps.pick_fastest()
            telemetry = lap.get_telemetry()
            
            # Extraemos X, Y
            self.track_coords = np.array(list(zip(telemetry['X'], telemetry['Y'])))
            
            # Normalizar coordenadas para que quepan en nuestra pantalla
            self._normalize_coordinates()
            
            print(f"Circuito cargado. Puntos de trazada: {len(self.track_coords)}")
            return True
        except Exception as e:
            print(f"Error cargando circuito: {e}")
            return False

    def _normalize_coordinates(self):
        """Ajusta las coordenadas X,Y del mundo real a la pantalla de Pygame."""
        if self.track_coords is None:
            return

        min_x, min_y = np.min(self.track_coords, axis=0)
        max_x, max_y = np.max(self.track_coords, axis=0)
        
        # Paneles UI ocupan espacio:
        # Izquierda: 300px (Eventos)
        # Derecha: 300px (Leaderboard)
        # Zona segura: x=320 a x=SCREEN_WIDTH-320
        
        left_panel_w = 320
        right_panel_w = 320
        top_margin = 80
        bottom_margin = 80
        
        safe_width = config.SCREEN_WIDTH - left_panel_w - right_panel_w
        safe_height = config.SCREEN_HEIGHT - top_margin - bottom_margin
        
        # Factores de escala
        scale_x = safe_width / (max_x - min_x)
        scale_y = safe_height / (max_y - min_y)
        scale = min(scale_x, scale_y) # Mantener proporción
        
        # Centrar en la zona segura
        # 1. Escalar y llevar a 0,0
        self.track_coords[:, 0] = (self.track_coords[:, 0] - min_x) * scale
        self.track_coords[:, 1] = (self.track_coords[:, 1] - min_y) * scale
        
        # 2. Centrar en el rectangulo safe
        real_w = (max_x - min_x) * scale
        real_h = (max_y - min_y) * scale
        
        offset_x = left_panel_w + (safe_width - real_w) / 2
        offset_y = top_margin + (safe_height - real_h) / 2
        
        self.track_coords[:, 0] += offset_x
        self.track_coords[:, 1] += offset_y
        
        # Invertir Y porque en pantallas la Y crece hacia abajo (pero mantenemos el offset relativo)
        # Ojo: Invertir Y requiere hacerlo respecto al centro o altura total.
        # Mejor invertimos antes del offset final o recalculamos.
        # Simplificación: Invertimos primero localmente.
        self.track_coords[:, 1] = config.SCREEN_HEIGHT - self.track_coords[:, 1] # Flip básico
        # Re-ajustar Y para que caiga en zona (esto es un poco hacky con el flip, 
        # mejor solo flipear y luego centrar, pero fastf1 coords a veces son raras. 
        # Asumiremos que el flip basic funciona y luego centramos si fuera necesario, 
        # pero el codigo anterior flipeaba al final.
        # Vamos a re-centrar Y después del flip para asegurar:
        min_y_new = np.min(self.track_coords[:, 1])
        max_y_new = np.max(self.track_coords[:, 1])
        real_h_new = max_y_new - min_y_new
        
        target_y_center = config.SCREEN_HEIGHT / 2
        current_y_center = min_y_new + real_h_new / 2
        diff_y = target_y_center - current_y_center
        self.track_coords[:, 1] += diff_y

    def load_next_circuit(self):
        """Selecciona un nuevo circuito aleatorio y lo carga."""
        self.circuit_name = np.random.choice(self.circuits)
        return self.load_circuit()

    def get_track_points(self):
        return self.track_coords

    def get_month_markers(self):
        """Devuelve una lista de (index, nombre_mes) distribuidos por la pista."""
        if self.track_coords is None:
            return []
            
        months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", 
                  "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
        
        markers = []
        total_points = len(self.track_coords)
        
        # Asumimos que la pista es un bucle que representa un año (counter-clockwise o clockwise)
        # Dividimos los puntos equitativamente
        for i, month in enumerate(months):
            idx = int((i / 12) * total_points)
            # Ajustar coordenada para el texto
            x, y = self.track_coords[idx]
            markers.append({
                "index": idx,
                "label": month,
                "coords": (x, y)
            })
            
        return markers
        
if __name__ == "__main__":
    # Test simple
    engine = RaceEngine(config.CIRCUIT, config.YEAR)
    engine.load_circuit()
