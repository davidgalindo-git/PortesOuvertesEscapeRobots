import tkinter as tk
from tkinter import messagebox
import sys
import os
import variable
from Admin.gestionsql import recuperation_frag, validation_code, \
    get_groups_with_scores  # validation_code doit exister dans gestionsql
from Escape.scoreboard import show_scoreboard

# Chemin vers le dossier où se trouve codes.py (même dossier que enigme.py)
current_dir = os.path.dirname(os.path.abspath(__file__))

# S'assure que ce dossier est dans sys.path pour l'import
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from codes import main as get_random_words  # import après modification du sys.path


class EnigmesGame:
    def __init__(self, parent, correct_words=None, group_score=None):
        """
        parent: frame d'affichage (game_frame)
        correct_words: (optionnel) données générées
        group_score: IntVar passé depuis ScriptLauncherApp (recommandé)
        """
        self.parent = parent
        self.group_score = group_score  # IntVar ou None (fallback disponible)
        # Récupérer les fragments stockés en BDD (peut retourner None si manquant)
        code1 = recuperation_frag(variable.selected_group_id, "fragment1")
        code2 = recuperation_frag(variable.selected_group_id, "fragment2")
        code3 = recuperation_frag(variable.selected_group_id, "fragment3")
        # Normaliser (éviter None)
        self.correct_words = [(code1 or ""), (code2 or ""), (code3 or "")]
        # debug
        # print("Correct words from DB:", self.correct_words)

        self.frame = tk.Frame(self.parent, bg="white")

        self.title_lbl = tk.Label(
            self.frame,
            text="Entrez les pièces de l'enigme que vous avez trouvées",
            font=("Helvetica", 18, "bold"),
            bg="white"
        )
        self.title_lbl.pack(pady=20)

        self.entry_frame = tk.Frame(self.frame, bg="white")
        self.entry_frame.pack(pady=20)
        self.entries = []
        for _ in range(3):
            entry = tk.Entry(self.entry_frame, font=("Helvetica", 16), width=15, justify='center')
            entry.pack(side='left', padx=15)
            self.entries.append(entry)

        self.validate_btn = tk.Button(
            self.frame,
            text="Valider",
            font=("Helvetica", 14, "bold"),
            width=10,
            command=self.validate_entries
        )
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
        # Récupération des inputs
        frag1 = self.entries[0].get().strip()
        frag2 = self.entries[1].get().strip()
        frag3 = self.entries[2].get().strip()

        # Vérification visuelle (pré-calcul) : comparer en insensitive case
        all_correct_local = True
        for i, user_entry in enumerate([frag1, frag2, frag3]):
            correct = (self.correct_words[i] or "").strip()
            if user_entry.strip().upper() == correct.upper():
                self.entries[i].config(bg="lightgreen")
            else:
                self.entries[i].config(bg="tomato")
                all_correct_local = False

        if not all_correct_local:
            self.feedback_label.config(text="Certaines réponses sont incorrectes. Réessayez.", fg="red")
            return

        # Si on arrive ici, localement tout est correct → on enregistre le score final en BDD
        # Récupérer le score final depuis la variable passée (préféré)
        final_score = None
        if self.group_score is not None:
            try:
                final_score = int(self.group_score.get())
            except Exception:
                final_score = None

        # fallback : tenter d'accéder à l'objet app attaché à la root (si tu as utilisé root.app = self)
        if final_score is None:
            try:
                root = self.parent.winfo_toplevel()
                app = getattr(root, "app", None)
                if app is not None and hasattr(app, "group_score"):
                    final_score = int(app.group_score.get())
            except Exception:
                final_score = None

        # Dernier fallback : récupérer le score déjà en BDD (non recommandé)
        if final_score is None:
            # on peut récupérer le score existant en BDD
            from Admin.gestionsql import recuperation_score
            final_score = recuperation_score(variable.selected_group_id) or 0

        # Appeler la fonction de validation qui enregistre le score final
        ok, saved_score = validation_code(variable.selected_group_id, frag1, frag2, frag3, final_score)

        if ok:
            self.feedback_label.config(text=f"Bravo ! Code correct. Score enregistré : {saved_score}", fg="green")
            # Optionnel : désactiver le bouton pour éviter re-soumission
            self.validate_btn.config(state="disabled")
            root = self.parent.winfo_toplevel()
            show_scoreboard(
                root,
                high_scores=get_groups_with_scores(),
                group_score=saved_score
            )
        else:
            # Théoriquement on n'arrive pas ici puisque on a déjà validé localement, mais on garde sécurité
            self.feedback_label.config(text="Erreur lors de l'enregistrement du score. Réessayez.", fg="red")

    def reset_game(self):
        for entry in self.entries:
            entry.delete(0, tk.END)
            entry.config(bg="white")
        self.feedback_label.config(text="")
        # réactiver le bouton
        try:
            self.validate_btn.config(state="normal")
        except Exception:
            pass
