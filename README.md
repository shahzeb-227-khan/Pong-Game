# 🎮 Shahzeb Pong Game

A polished and interactive **Pong game built using Python and Pygame**, developed with clean structure, modern game mechanics, sound design, and multiple gameplay modes.

This project goes beyond a basic Pong clone by introducing **AI gameplay**, **two-player support**, **dynamic ball physics**, and **professional audio handling** such as background music ducking and mute controls.

---

## 🚀 Features

- 🧠 **AI Mode** – Play against a responsive computer opponent  
- 👥 **Two-Player Mode** – Local multiplayer using keyboard controls  
- 🎯 **Dynamic Ball Physics** – Ball angle changes based on paddle hit position  
- 🔊 **Sound Effects (MP3)**  
  - Paddle hit sound  
  - Scoring sound  
  - Game over sound  
- 🎵 **Background Music**
  - Looping gameplay music  
  - Audio ducking so hit sounds stay prominent  
- ⏸️ **Pause / Resume System**
- 🔇 **Mute Toggle**
- 🔁 **Restart Anytime**
- 🏆 **Win Condition System**
- 🧼 Clean, readable, and extensible codebase

---

## 🎮 Controls

### Gameplay
| Action | Key |
|------|-----|
| Move Player 1 Up | `W` |
| Move Player 1 Down | `S` |
| Move Player 2 Up | `↑` |
| Move Player 2 Down | `↓` |

### Game Controls
| Action | Key |
|------|-----|
| Start Game | `SPACE` |
| Pause / Resume | `P` |
| Restart Game | `R` |
| Mute / Unmute | `M` |
| Quit Game | `ESC` |

### Mode Selection (Before Starting)
| Mode | Key |
|----|----|
| Play vs AI | `1` |
| Two Players | `2` |

---

## 🗂 Project Structure

```

pong-game/
│── pong.py
│── sounds/
│     ├── bg_music.mp3
│     ├── hit.mp3
│     ├── success.mp3
│     └── gameover.mp3

````

---

## 🛠 Requirements

- Python **3.8+**
- Pygame

Install Pygame using:
```bash
pip install pygame
````

---

## ▶️ How to Run

```bash
python pong.py
```

Make sure the `sounds/` folder is in the same directory as `pong.py`.

---

## 🧠 Technical Highlights

* Uses **state-based game flow** (start, pause, game over)
* Implements **safe sound loading** to avoid runtime crashes
* Background music ducking ensures sound clarity
* AI paddle logic reacts only when the ball moves toward it
* Designed for easy future expansion (menus, difficulty levels, power-ups)

---



<img width="1195" height="938" alt="image" src="https://github.com/user-attachments/assets/835bf18d-7c06-4f6b-893c-f0276d21dadb" />



---

## 📜 License

This project is released under the **MIT License**.
You are free to use, modify, and distribute it with attribution.

---

## 👤 Author

**Shahzeb**
Developed as a professional Python & Pygame project.

---

## ⭐ Acknowledgements

Inspired by the classic Pong arcade game, reimagined with modern Python game development practices.

