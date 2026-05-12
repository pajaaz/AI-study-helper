import tkinter as tk
from tkinter import ttk, messagebox
from text_processing import generate_summary
from generator import generate_questions
from database import save_to_db, get_history

class StudyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Pomocník pro učení - Verze 0.9 (Fáze 3)")
        self.root.geometry("900x700")
        
        # Stylování pro modernější vzhled
        style = ttk.Style()
        style.theme_use('clam')
        
        # Vytvoření záložek (Tabs)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Záložka 1: Učení
        self.tab_study = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_study, text='Učení & Analýza')
        
        # Záložka 2: Historie
        self.tab_history = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_history, text='Historie testů')
        
        self.setup_study_tab()
        self.setup_history_tab()
        
        # Status bar
        self.status_label = tk.Label(root, text="Aplikace připravena", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Načtení historie při startu
        self.refresh_history()

    def setup_study_tab(self):
        # Vstupní pole
        ttk.Label(self.tab_study, text="Vložte své poznámky pro analýzu:", font=("Arial", 11, "bold")).pack(pady=(10, 5), anchor="w", padx=10)
        self.text_input = tk.Text(self.tab_study, height=8, width=100)
        self.text_input.pack(padx=10, pady=5)
        
        # Tlačítko pro spuštění
        self.btn_process = tk.Button(self.tab_study, text="Zpracovat text (Shrnutí + Otázky)", command=self.process_text, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
        self.btn_process.pack(pady=10)
        
        # Rozdělení na dva sloupce pro výsledky (Shrnutí vlevo, Otázky vpravo)
        frame_results = ttk.Frame(self.tab_study)
        frame_results.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Levý sloupec - Shrnutí
        frame_summary = ttk.Frame(frame_results)
        frame_summary.pack(side='left', fill='both', expand=True, padx=(0, 5))
        ttk.Label(frame_summary, text="Shrnutí textu:", font=("Arial", 10, "bold")).pack(anchor="w")
        self.text_summary = tk.Text(frame_summary, height=12, bg="#f0f8ff")
        self.text_summary.pack(fill='both', expand=True)
        
        # Pravý sloupec - Otázky
        frame_questions = ttk.Frame(frame_results)
        frame_questions.pack(side='right', fill='both', expand=True, padx=(5, 0))
        ttk.Label(frame_questions, text="Kontrolní otázky:", font=("Arial", 10, "bold")).pack(anchor="w")
        self.text_questions = tk.Text(frame_questions, height=12, bg="#fffacd")
        self.text_questions.pack(fill='both', expand=True)

    def setup_history_tab(self):
        ttk.Label(self.tab_history, text="Uložené výsledky z předchozích učení:", font=("Arial", 11, "bold")).pack(pady=10, anchor="w", padx=10)
        
        # Tlačítko na obnovení
        ttk.Button(self.tab_history, text="Obnovit historii", command=self.refresh_history).pack(anchor="w", padx=10, pady=5)
        
        # Textové pole pro historii
        self.text_history = tk.Text(self.tab_history, height=30, width=100, bg="#f5f5f5")
        self.text_history.pack(padx=10, pady=5, fill='both', expand=True)

    def process_text(self):
        original_text = self.text_input.get("1.0", tk.END).strip()
        
        if len(original_text) < 20:
            messagebox.showwarning("Málo textu", "Vložte prosím delší text (alespoň 20 znaků).")
            return
            
        self.status_label.config(text="Zpracovávám text...")
        self.root.update()
        
        try:
            # 1. Generování shrnutí (z tvého starého modulu text_processing.py)
            summary = generate_summary(original_text)
            
            # 2. Generování otázek
            questions = generate_questions(original_text, num_questions=3)
            
            # 3. Zobrazení výsledků
            self.text_summary.delete("1.0", tk.END)
            self.text_summary.insert(tk.END, summary)
            
            self.text_questions.delete("1.0", tk.END)
            self.text_questions.insert(tk.END, questions)
            
            # 4. Uložení do databáze
            save_to_db(original_text, summary, questions)
            
            # Obnovení zobrazení historie
            self.refresh_history()
            
            self.status_label.config(text="Hotovo! Výsledky uloženy do databáze.")
        except Exception as e:
            self.status_label.config(text="Chyba při zpracování")
            messagebox.showerror("Chyba", str(e))
            
    def refresh_history(self):
        self.text_history.delete("1.0", tk.END)
        history_records = get_history()
        
        if not history_records:
            self.text_history.insert(tk.END, "Zatím žádná historie.")
            return
            
        for record in history_records:
            record_id, summary, questions, created_at = record
            self.text_history.insert(tk.END, f"--- Záznam #{record_id} ({created_at}) ---\n")
            self.text_history.insert(tk.END, f"[SHRNUTÍ]:\n{summary}\n\n")
            self.text_history.insert(tk.END, f"[OTÁZKY]:\n{questions}\n")
            self.text_history.insert(tk.END, "="*60 + "\n\n")