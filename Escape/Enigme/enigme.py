import tkinter as tk
import sys
import os
import variable
from Admin.gestionsql import  recuperation_frag

# Chemin vers le dossier où se trouve codes.py (même dossier que enigme.py)
current_dir = os.path.dirname(os.path.abspath(__file__))

# S'assure que ce dossier est dans sys.path pour l'import
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from codes import main as get_random_words  # import après modification du sys.path


class EnigmesGame:
    def __init__(self, parent,correct_words):
        self.parent = parent
        # Les bons mots (3 pièces à trouver)
        code1= recuperation_frag(variable.selected_group_id, "fragment1")
        code2= recuperation_frag(variable.selected_group_id, "fragment2")
        code3= recuperation_frag(variable.selected_group_id, "fragment3")
        self.correct_words = [code1, code2, code3]
        self.frame = tk.Frame(self.parent, bg="white")



        self.title_lbl = tk.Label(self.frame,
                                  text="Entrez les pièces de l'enigme que vous avez trouvées",
                                  font=("Helvetica", 18, "bold"), bg="white")
        self.title_lbl.pack(pady=20)

        self.entry_frame = tk.Frame(self.frame, bg="white")
        self.entry_frame.pack(pady=20)
        self.entries = []
        for _ in range(3):
            entry = tk.Entry(self.entry_frame, font=("Helvetica", 16), width=15, justify='center')
            entry.pack(side='left', padx=15)
            self.entries.append(entry)

        self.validate_btn = tk.Button(self.frame, text="Valider", font=("Helvetica", 14, "bold"),
                                      width=10, command=self.validate_entries)
        self.validate_btn.pack(pady=20)

        self.feedback_label = tk.Label(self.frame, text="", font=("Helvetica", 14), bg="white")
        self.feedback_label.pack()

        self.started = False

    def start(self):
        if not self.started:
            self.frame.pack(fill="both", expand=True)
            self.started = True
        else:
            self.frame.pack(fill="both", expand=True)
        # Reset les champs et feedback à chaque démarrage
        self.reset_game()

    def validate_entries(self):
        all_correct = True
        for i in range(3):
            user_input = self.entries[i].get().strip().upper()
            if user_input == self.correct_words[i].upper():
                self.entries[i].config(bg="lightgreen")
            else:
                self.entries[i].config(bg="tomato")
                all_correct = False

        if all_correct:
            self.feedback_label.config(text="Bravo ! Vous avez trouvé toutes les pièces.", fg="green")
        else:
            self.feedback_label.config(text="Certaines réponses sont incorrectes. Réessayez.", fg="red")

    def reset_game(self):
        for entry in self.entries:
            entry.delete(0, tk.END)
            entry.config(bg="white")
        self.feedback_label.config(text="")
