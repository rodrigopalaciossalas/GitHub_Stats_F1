import os
from dotenv import load_dotenv

load_dotenv()

# Configuración de GitHub
# Para obtener un token: https://github.com/settings/tokens
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME", "rodrigopalaciossalas")

# Configuración de F1
YEAR = 2024
CIRCUIT = "Monaco" # Usaremos "Monaco" por defecto, pero FastF1 soporta todos

# Configuración Visual
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 30
OUTPUT_GIF_NAME = "f1_stats.gif"
