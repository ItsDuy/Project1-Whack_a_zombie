# Whack‑a‑Zombie

A simple **Whack‑a‑Mole–style** game built with Pygame. Left‑click to whack zombies and score as many points as you can before time runs out.

---

## Requirements
- **Python** 3.10+ (3.11/3.12 recommended)
- Packages listed in `requirements.txt` (e.g. `pygame`, etc.)

---

## Setup & Run

### 1) Create a virtual environment
**macOS / Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell)**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 2) Install dependencies
```bash
pip install -r requirements.txt
```

### 3) Start the game
```bash
python3 run.py
```
> On Windows you can also use `python run.py` or `py run.py`.

---

## Project Structure (suggested)

```
project/
├─ run.py
├─ requirements.txt
├─ docker-compose.yml       # (if using Docker)
├─ Dockerfile               # (if using Docker)
├─ requirements.txt
├─ src/
│  ├─ whack_a_zombie.py      # Game loop, input/events, collision, zombie respawn
│  ├─ background.py          # Draws tiled background, grass, and holes
│  ├─ zombies.py             # Zombie sprites/animation (idle/death), stay timer bar
│  ├─ cursor.py              # Hammer cursor & click animation
│  ├─ ScoreBoard.py          # Score, miss counter, countdown timer
│  ├─ SoundManager.py        # Music & sound effects
│  └─ ReplayBoard.py         # Game Over panel with Replay/Menu
└─ assets/
   ├─ Fonts/Minecraft.ttf
   ├─ Sounds/
   │  ├─ Music/BackGroundMusic.wav
   │  └─ Sfx/{Hit.wav, Miss.wav}
   └─ images/
      ├─ background/{tile1..tile9.png, grass1.png, grass2.png, hole.png}
      ├─ zombies/
      │  ├─ idle/*.png
      │  └─ death/*.png
      └─ cursor/{hammer0.png, hammer1.png}
```

### Example `run.py` (if you don’t have one yet)
```python
# run.py
from src.whack_a_zombie import main

if __name__ == "__main__":
    main()
```

---

## Controls
- **Left Mouse**: Whack a zombie
- **R**: Restart (in‑game or from the Game Over screen)
- **M**: Menu (shown on the final screen; currently a placeholder)

---

## Assets Notes
- Font: `assets/Fonts/Minecraft.ttf` (falls back to a system font if missing).
- Audio: background music at `assets/Sounds/Music/BackGroundMusic.wav` and SFX at `assets/Sounds/Sfx/{Hit.wav, Miss.wav}`.
- Background tiles/grass/hole images under `assets/images/background/`.
- Zombie sprites under `assets/images/zombies/{idle,death}/`.
- Hammer cursor images under `assets/images/cursor/`.

Make sure these paths exist to avoid load errors.


---

## Credits / Attributions
This project uses third‑party assets. Full attributions and licenses are listed in **[CREDITS.md](./CREDITS.md)**.  
When required by the asset’s license, the original license files are included inside the corresponding `assets/*` folders.

Short summary (replace placeholders with actual info):
- **Font:** “Minecraft.ttf” by <Author/Studio>, licensed under <License>. Source: <URL>. Changes: <e.g., subset/rename>.
- **Tiles/Background:** "Post-apocalypse Pixel Art Asset Pack (16×16 Tileset)" by [TheLazyStone](https://thelazystone.itch.io/)
  License: CC0 1.0 — https://creativecommons.org/publicdomain/zero/1.0/
  Source: https://thelazystone.itch.io/post-apocalypse-pixel-art-asset-pack
  Changes: resized 16×16→64×64
- **Audio (BGM/SFX):** “BackGroundMusic.wav”, “Hit.wav”, “Miss.wav” by DCAudio, <License>. Source: <URL>(https://terrorbytegames.itch.io/zombie-massacre-sound-effects-starter-pack). Changes: <e.g., normalized>.

---

## Troubleshooting
- **No window / display error**: Run on a machine with a GUI (not headless); update your graphics driver if needed.
- **No sound**: Check OS audio output; you can disable BGM or tweak mixer init in `SoundManager.py`.
- **Missing files**: Verify asset file names and folder structure.

---

## License
For learning/non‑commercial use (adjust as you like).

Have fun! 🎯
