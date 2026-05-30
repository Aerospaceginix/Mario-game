# Super Mario-Style Retro Platformer

A complete, playable, and side-scrolling 2D Mario-style platformer built entirely in Python using the `tkinter` library. This project features retro pixel art, physics-based movement, and multiple game mechanics.

## 🚀 Features

- **Retro Pixel Art Visuals**: Custom-built pixel engine that renders Mario, enemies (Turtles), piranha plants, and textured environments programmatically.
- **Dynamic Full-Screen Mode**: Automatically detects your screen resolution and scales the game accordingly.
- **Physics Engine**: Realistic gravity, horizontal friction, and a **Double-Jump** mechanic.
- **Side-Scrolling Camera**: Smoothly tracks the player forward through an expanded level (4000+ pixels wide).
- **Classic Enemies & Hazards**:
  - **Patrolling Turtles**: Smart edge-detection AI prevents them from falling off platforms.
  - **Animated Piranha Plants**: Pop up from pipes to surprise the player.
  - **Pits & Gaps**: Navigational hazards that require precise jumping.
- **Save the Queen**: Reach the end of the map to rescue the trapped Queen from her cage!

## 🎮 Controls

- **Left/Right Arrow Keys**: Walk / Run
- **Up Arrow / Spacebar**: Jump (Double-tap for Double-Jump)
- **'R' Key**: Restart the level
- **'Esc' Key**: Exit the game

## 🛠️ Installation & Running

This game is designed to be compatible with **Python 3.10 through 3.14+** and requires **no external dependencies** (it uses the built-in `tkinter` library).

1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/mario-retro-platformer.git
   cd mario-retro-platformer
   ```

2. Run the game:
   ```bash
   python mario_game.py
   ```

## 📸 Screenshots

![Main Gameplay](Screenshot%202026-05-31%20025102.png)
*Mario navigating through the retro world.*

![Turtles and Hazards](Screenshot%202026-05-31%20025121.png)
*Be careful of the patrolling turtles and piranha plants!*

![Victory Sequence](Screenshot%202026-05-31%20025206.png)
*VICTORY! The Queen has been rescued from her cage.*

## 📜 Technical Details

The game is contained entirely within a single script (`mario_game.py`). It uses a custom `create_pixel_image` function that converts pixel grids (nested lists) into Tkinter `PhotoImage` objects at startup, ensuring high performance even in a standard library GUI environment.
