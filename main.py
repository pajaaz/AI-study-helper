import tkinter as tk
from ui_module import StudyApp
from database import init_db

if __name__ == "__main__":
    # Inicializace databáze při startu
    init_db()
    
    # Spuštění UI
    root = tk.Tk()
    app = StudyApp(root)
    root.mainloop()