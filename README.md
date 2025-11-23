🎮 Connect Four — Enhanced Tkinter Game

A polished and feature-rich **Connect Four desktop game** built using **Python (Tkinter)**.
This upgraded edition comes with improved visuals, sound effects, save/load support, hover indicators, and a scoreboard — providing a complete and fun gameplay experience.

---

## 🚀 Features

### 🖥️ Modern UI

* Smooth board design with shadows & glossy disc effects
* Hover preview shows where the next disc will drop
* Clean, responsive layout

### 🔊 Sound Effects

* Disc drop sound
* Win sound sequence
* Automatic fallback to system bell if sound module unavailable

### 🏆 Scoreboard

* Tracks wins for **Red** and **Yellow** players
* Score persists during the app session

### 💾 Save & Load Game

* Saves current board, player turn, and score into
  **`connect4_save.json`**
* Load anytime to continue where you left off

### 🔁 Game Controls

* Restart game button
* Hover highlight
* Smooth disc placement
* Handles invalid moves (full columns)

---

## 📂 Project Structure

```
Connect-Four-Game/
│
├── ConnectFourGame.py      # Main game script
├── connect4_save.json      # Auto-created on save
└── README.md               # Project documentation
```

---

## ▶️ How to Run

Make sure Python 3 is installed.

### **Run normally:**

```bash
python ConnectFourGame.py
```

### **Run without showing console (Windows):**

```bash
pythonw ConnectFourGame.py
```

---

## 🎯 How to Play

* Red moves first
* Click on a column to drop your disc
* First player to connect **4 discs** horizontally, vertically, or diagonally wins
* Use **Restart** to reset the board
* Use **Save** and **Load** to continue later

---

## 🛠️ Tech Stack

* **Python 3**
* **Tkinter** (GUI)
* **Winsound** (Windows sound module, optional)
* **JSON** (save/load system)

---

## 📸 Screenshots (Add here later)

```
![Game Preview](preview.png)
```

*(You can add a screenshot PNG inside your repo and name it `preview.png`.)*

---

## 🤝 Author

**Syed Roshan**
💻 Computer Science Engineering Student
🔗 GitHub: [SyedRoshannn](https://github.com/SyedRoshannn)

---

## ⭐ Contribute & Support

If you like this project:

* ⭐ Star the repository
* 🍴 Fork it
* 🐛 Report issues
* 🚀 Suggest improvements
