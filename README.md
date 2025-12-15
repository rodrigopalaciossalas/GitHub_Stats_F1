# 🏎️ F1 GitHub Stats Racer

**Visualize your GitHub Repository Activity as a Live F1 Race!**

This Python project turns your GitHub repositories into F1 cars that race against each other based on commit activity.
It features **High-Quality Visuals** (4x Anti-Aliasing), **Live Leaderboards**, and **Interactive Events**.

![Demo](https://via.placeholder.com/800x400?text=F1+GitHub+Stats+Demo)

## 🚀 Features

*   **Live Racing**: Cars move based on real repository commit counts (`main.py`) or mock data (`test_race.py`).
*   **Premium Visuals**:
    *   **SSAA (SuperSampling Anti-Aliasing)**: Tracks are rendered at 4K resolution and smooth-scaled for perfect edges.
    *   **Smart Animations**: Smooth leaderboard reordering and car movement interpolation.
    *   **Particle Systems**: Smoke and fire effects for retired cars.
*   **Dynamic Events**:
    *   Overtakes are logged in a scrolling "Race Control" feed.
    *   **Manual Safety Car / Crash**: Trigger interactive retirements manually (Test Mode only).

## 🛠️ Installation

1.  **Clone the repo**:
    ```bash
    git clone https://github.com/yourusername/GitHub_Stats_F1.git
    cd GitHub_Stats_F1
    ```

2.  **Install Dependencies**:
    The project relies on `pygame` for visualization and `PyGithub` for data fetching.
    ```bash
    pip install pygame PyGithub numpy imageio
    ```

3.  **Configuration**:
    Create a `.env` file or export environment variables for your GitHub credentials (optional for Test Mode):
    ```bash
    export GITHUB_TOKEN="your_token_here"
    export GITHUB_USERNAME="your_username"
    ```

## 🏁 Usage

### 1. Test Mode (No API Required)

Run a simulated race with mock data to test visuals and controls:

```bash
python test_race.py
```

*   **Controls**:
    *   `ENTER`: Trigger a **Crash/Engine Failure** for the last place car (Smoke & Fire effect!).
    *   `SPACE`: Trigger a random "Chaos" event (stats shuffle).

### 2. Live Mode (Real GitHub Data)

Visualize your actual GitHub repositories:

```bash
python main.py
```

*   The script fetches your top repositories.
*   Speeds are calculated based on `total_commits`.
*   The race runs continuously on a random F1 circuit generated at startup.

## 🎨 Customization

*   **Circuits**: The system randomly selects simplified layouts of famous tracks (Monaco, Spa, Silverstone, etc.).
*   **Teams**: Colors are automatically assigned to repositories to mimic F1 teams (Red, Teal, Navy, Orange, etc.).

## 📂 Project Structure

*   `main.py`: Entry point for real data mode.
*   `test_race.py`: Entry point for mock simulation mode.
*   `visualizer.py`: Core rendering engine (SSAA, Particles, UI).
*   `race_engine.py`: Logic for track generation (~Math related).
*   `car.py`: Car object logic and physics.

---
*Created with Python & Pygame for F1 Fans.* 🏎️💨
