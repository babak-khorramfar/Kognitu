# Kognitu

AI-powered layout generator for physical game boards  
Generates interactive, creative board layouts for children using a language model.  
Designed to promote coordination, creativity, and movement-based learning in a playful way.

---

## 🚀 Features

- **Dynamic layout generation** via Hugging Face Transformers  
- **Graphical rendering** of game boards with PyQt5  
- **Modular MVC architecture** for easy extension  
- **Cross-platform executable** (Windows/macOS/Linux) via PyInstaller

---

## 🛠 Installation

1. **Clone the repository** and navigate into it  
   ```bash
   git clone https://github.com/<YourUser>/Kognitu.git
   cd Kognitu
   ```
2. **Create and activate a virtual environment**  
   ```bash
   python -m venv venv
   # Windows CMD
   venv\Scripts\activate.bat
   # PowerShell
   .\venv\Scripts\Activate.ps1
   # macOS/Linux
   source venv/bin/activate
   ```
3. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

---

## 🎮 Usage

- **Run the application**  
  ```bash
  python main.py
  ```
- In the GUI:
  1. Click **Generate Challenge** or  
  2. **Create Custom Layout**  
  3. View, accept, or edit the layout

---

## 📁 Project Structure

```
Kognitu/
├── controller/       # Controllers & business logic
├── model/            # Data models (Board, Tile)
├── view/             # GUI components (Window, Canvas)
├── utils/            # Config & helper functions
├── resources/        # Assets (icons, fonts)
├── main.py           # Entry point
└── requirements.txt  # Python dependencies
```

---

## 🤝 Contributing

1. Fork & clone the repo  
2. Create a new branch  
3. Commit your changes  
4. Open a pull request

---

## 📝 License

© 2025 Babak Khorramfar
