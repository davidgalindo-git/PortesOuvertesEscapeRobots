import tkinter as tk
import sys
import variable
import os
from Admin.gestionsql import recuperation_frag
# Préparation du chemin pour importer d’autres fichiers si besoin
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)


class PasswordGame:
    def __init__(self, parent, correct_password,generated_words=None, stop_callback=None):
        self.parent = parent
        self.correct_password = correct_password


        self.frame = tk.Frame(self.parent, bg="white")

        self.title_lbl = tk.Label(self.frame,
                                  text="Entrez le code du puzzle",
                                  font=("Helvetica", 18, "bold"), bg="white")
        self.title_lbl.pack(pady=20)

        self.entry = tk.Entry(self.frame, font=("Helvetica", 16), width=20, justify='center')  # show="*" supprimé
        self.entry.pack(pady=10)

        self.validate_btn = tk.Button(self.frame, text="Valider", font=("Helvetica", 14, "bold"),
                                      width=10, command=self.validate_entry)
        self.validate_btn.pack(pady=20)

        self.feedback_label = tk.Label(self.frame, text="", font=("Helvetica", 14), bg="white")
        self.feedback_label.pack()

        self.started = False
        self.generated_words = generated_words
        self.stop_callback = stop_callback


    def start(self):
        if not self.started:
            self.frame.pack(fill="both", expand=True)
            self.started = True
        else:
            self.frame.pack(fill="both", expand=True)
        self.reset_game()

    def validate_entry(self):
        # Appelle la méthode show_result qui fait toute la logique d'affichage
        self.show_result()

    def show_result(self):
        user_input = self.entry.get().strip().lower()
        if user_input == self.correct_password.lower():
            result_text = "Mot de passe correct !\n\nFélicitations, vous avez réussi le puzzle."
            code = recuperation_frag(variable.selected_group_id, "fragment3")
            if self.generated_words:
                result_text += f"\n\nVoici le Dernier code de l'énigme : {code}"
            self.feedback_label.config(text=result_text, fg="darkgreen")
            self.entry.config(bg="lightgreen")
            if callable(self.stop_callback):
                self.stop_callback()
        else:
            result_text = "Mot de passe incorrect.\n\nRéessayez encore !"
            self.feedback_label.config(text=result_text, fg="red")
            self.entry.config(bg="tomato")

    def reset_game(self):
        self.entry.delete(0, tk.END)
        self.entry.config(bg="white")
        self.feedback_label.config(text="", fg="black")


class PuzzleGame:
    def __init__(self, parent, correct_password="hardware", generated_words=None,group_score=None,stop_callback=None):
        self.game = PasswordGame(parent, correct_password, generated_words=generated_words,stop_callback=stop_callback)
        self.group_score = group_score

    def start(self):
        self.game.start()

