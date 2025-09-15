import tkinter as tk
from tkinter import ttk

class ScoreboardWindow:
    def __init__(self, parent, high_scores=None, group_score=None):
        # Nouvelle fenêtre secondaire (Toplevel)
        self.window = tk.Toplevel(parent)
        self.window.title("Scoreboard")
        self.window.geometry("600x400")
        self.window.configure(bg="#f0f0f0")

        # Score du groupe actuel
        if group_score is not None:
            tk.Label(
                self.window,
                text="Votre Score Total",
                font=("Helvetica", 20, "bold"),
                bg="#f0f0f0"
            ).pack(pady=10)

            tk.Label(
                self.window,
                text=f"{group_score}",
                font=("Helvetica", 48, "bold"),
                bg="#f0f0f0",
                fg="blue"
            ).pack(pady=20)

        # Classement
        tk.Label(
            self.window,
            text="Classement des Meilleurs Scores",
            font=("Helvetica", 16, "bold"),
            bg="#f0f0f0"
        ).pack(pady=10)

        columns = ("rang", "nom_groupe", "score")
        tree = ttk.Treeview(self.window, columns=columns, show="headings", height=10)
        tree.heading("rang", text="Rang")
        tree.heading("nom_groupe", text="Groupe")
        tree.heading("score", text="Score")
        tree.pack(expand=True, fill="both", padx=20, pady=10)



        # Ajouter données de classement
        if high_scores:
            for i, (nom, score) in enumerate(high_scores):
                tree.insert("", tk.END, values=(i + 1, nom, score))

        # Bouton fermer
        tk.Button(
            self.window,
            text="Fermer",
            command=self.window.destroy,
            font=("Helvetica", 12),
            bg="#FFFDD0"
        ).pack(pady=20)

# Fonction pratique pour ouvrir la fenêtre
def show_scoreboard(parent, high_scores=None, group_score=None):
    ScoreboardWindow(parent, high_scores, group_score)