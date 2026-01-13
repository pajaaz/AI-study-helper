import tkinter as tk
from tkinter import messagebox
from text_processing import generate_summary

class StudyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Pomocník pro učení - Verze 0.1")
        self.root.geometry("800x600")
        
        # Nadpis
        self.label_title = tk.Label(root, text="Vložte své poznámky:", font=("Arial", 12, "bold"))
        self.label_title.pack(pady=5)
        
        # Vstupní pole
        self.text_input = tk.Text(root, height=10, width=90)
        self.text_input.pack(pady=5)
        
        # Tlačítko pro akci
        self.btn_summarize = tk.Button(root, text="Vytvořit shrnutí (AI)", command=self.run_summary, bg="lightblue", height=2)
        self.btn_summarize.pack(pady=10)
        
        # Výstupní pole
        self.label_output = tk.Label(root, text="Shrnutí textu:", font=("Arial", 12, "bold"))
        self.label_output.pack(pady=5)
        
        self.text_output = tk.Text(root, height=8, width=90, bg="#f0f0f0")
        self.text_output.pack(pady=5)
        
        # Status bar
        self.status_label = tk.Label(root, text="Připraveno", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

    def run_summary(self):
        # Načtení textu
        original_text = self.text_input.get("1.0", tk.END).strip()
        
        if not original_text:
            messagebox.showwarning("Varování", "Vložte prosím nějaký text.")
            return
            
        self.status_label.config(text="Zpracovávám text...")
        self.root.update()
        
        # Volání logiky z druhého modulu
        try:
            summary = generate_summary(original_text)
            
            # Vypsání výsledku
            self.text_output.delete("1.0", tk.END)
            self.text_output.insert(tk.END, summary)
            self.status_label.config(text="Hotovo (Shrnutí vygenerováno)")
        except Exception as e:
            self.status_label.config(text="Chyba při zpracování")
            messagebox.showerror("Chyba", str(e))