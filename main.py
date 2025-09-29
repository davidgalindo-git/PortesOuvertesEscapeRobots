"""
Projet: Portes Ouvertes SI-CA1a Robots
Autheurs: Imad El Khattabi, Mouldi Achouri, Gaëtan Gendroz,
Anthony Simond, David Galindo
Fichier: main.py
Version: 2.0
Date: 16.06.2025
Description: Lance le programme principal avec les 3 activités de la première partie du jeu.
"""

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from Escape.Enigme.codes import main as get_generated_words
import os
import importlib.util
import sys
from Admin.gestionsql import identification, create_group,get_all_group_names
from Escape.scoreboard import show_scoreboard
import variable
class ScriptLauncherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lanceur de Jeux Interactifs")
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg="#f0f0f0")
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        # Préparation pour le lancement des fichiers indépendants
        self.scripts = {
            "IT Quiz": {
                "module_path": os.path.join(self.base_dir, "Escape", "IT_quiz", "IT_quiz.py"),
                "image_path": os.path.join(self.base_dir, "images", "itquiz.jpg")
            },
            "ChronoQuiz": {
                "module_path": os.path.join(self.base_dir, "Escape", "ChronoQuiz", "pygamefresques.py"),
                "image_path": os.path.join(self.base_dir, "images", "ChronoQuiz.jpg")
            },
            "Enigmes": {
                "module_path": os.path.join(self.base_dir, "Escape", "Enigme", "enigme.py"),
                "image_path": os.path.join(self.base_dir, "images", "enigmes.png")
            },
            "Puzzle": {
                "module_path": os.path.join(self.base_dir, "Escape", "Puzzle", "PuzzleIT.py"),
                "image_path": os.path.join(self.base_dir, "images", "Puzzle.png")
            }
        }

        self.loaded_images = {}
        self.games_instances = {}
        self.current_game_key = None
        self.start_score = 1000
        self.score_var = tk.IntVar(value=self.start_score)
        self.score_job = None
        self.group_score = self.score_var  # pour passer facilement aux jeux
        self.generated_code = get_generated_words()

        # Suivi des succès de chaque jeu
        self.games_success = {
            "IT Quiz": False,
            "ChronoQuiz": False,
            "Puzzle": False
        }

        self.create_interface()

        self.root.bind("<Escape>", lambda e: self.root.attributes("-fullscreen", False))

        # Initialise le score à 1000


        # Création des frames tkinter
    def create_interface(self):
        # Frame HUD au dessus des activités
        self.top_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.top_frame.pack(side="top", fill="x", padx=20, pady=20)

        # Configure les colonnes : gauche (boutton "quit"), centre (titre), droite (scores)
        self.top_frame.grid_columnconfigure(0, weight=0)  # Quit stays left
        self.top_frame.grid_columnconfigure(1, weight=1)  # Title expands (center)
        self.top_frame.grid_columnconfigure(2, weight=0)  # Scores hug right
        self.top_frame.grid_columnconfigure(3, weight=0)

        # "Quit" frame and button
        quit_frame = tk.Frame(self.top_frame, bg="#f0f0f0")
        quit_frame.grid(row=0, column=0, sticky="w", pady=20)

        self.quit_btn = tk.Button(quit_frame, text="❌ Quitter le jeu", command=self.root.quit, fg="red")
        self.quit_btn.pack()

        # Titre
        title_label = tk.Label(self.top_frame, text="🎮 Choisissez votre jeu", font=("Helvetica", 24, "bold"), bg="#f0f0f0")
        title_label.grid(row=0, column=1, sticky="n", pady=20)

        # Score actuel

        score_label = tk.Label(self.top_frame, bg="#f0f0f0", text="Score : ", font=("Helvetica", 24, "bold"))
        score_label.grid(row=0, column=2, sticky="e", padx=5)
        self.score_number = tk.Label(self.top_frame, bg="#f0f0f0",font=("Helvetica", 24, "bold"),textvariable=self.score_var)  # ✅ lié au score_var
        self.score_number.grid(row=0, column=3, sticky="w", padx=5)

        # High score
        high_score_label = tk.Label(self.top_frame, bg="#f0f0f0", text="High Score : ", font=("Helvetica", 24, "bold"))
        high_score_label.grid(row=1, column=2, sticky="e", padx=5)
        high_score_number = tk.Label(self.top_frame, bg="#f0f0f0", text="", font=("Helvetica", 24, "bold"))
        high_score_number.grid(row=1, column=3, sticky="w", padx=5)

        # Boutton Scoreboard
        scoreboard_btn_frame = tk.Frame(self.top_frame, bg="#f0f0f0")
        scoreboard_btn_frame.grid(row=0, column=4, sticky="n", pady=20, padx=50)

        self.scoreboard_btn = tk.Button(scoreboard_btn_frame, text="Scoreboard", bg="#FFFDD0", width=20, height=2,
                                    command=lambda: show_scoreboard(self.root))


        self.scoreboard_btn.pack()

        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(expand=True, fill="both")

        menu_frame = tk.Frame(main_frame, bg="#f0f0f0", width=180)
        menu_frame.pack(side="left", fill="y", padx=10, pady=10)
        menu_frame.pack_propagate(False)


        for name, info in self.scripts.items():
            photo = None
            if os.path.exists(info["image_path"]):
                img = Image.open(info["image_path"]).resize((100, 100), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                self.loaded_images[name] = photo

            btn = tk.Button(menu_frame, image=photo, text=name, compound="top",
                            font=("Helvetica", 12), width=150, height=150,
                            command=lambda n=name: self.launch_game(n),
                            bg="#ffffff", relief="raised", bd=2)
            btn.pack(pady=10, fill="x")

        self.content_frame = tk.Frame(main_frame, bg="white", bd=2, relief="sunken")
        self.content_frame.pack(side="left", expand=True, fill="both", padx=10, pady=10)

    # Démarrer le score descendant
    def start_score_descendant(self):
        if self.score_job is None:  # seulement si le timer n’est pas actif
            self._score_tick()

    def _score_tick(self):
        self.score_var.set(self.start_score)
        self.start_score -= 1
        if self.start_score >= 0:
            self.score_job = self.root.after(1000, self._score_tick)

    # Arrêter le score
    def stop_score_descendant(self):
        if self.score_job:
            self.root.after_cancel(self.score_job)
            self.score_job = None

    def make_success_callback(self, game_key):
        def callback():
            self.games_success[game_key] = True
            self.stop_score_descendant()  # Stop seulement quand les 3 jeux réussis

        return callback

    # Lance le jeu
    def launch_game(self, game_key):
        jeux_avec_score = ["IT Quiz", "ChronoQuiz", "Puzzle"]

        # Ne démarre le score que si le jeu fait partie de ceux avec score
        # et qu'il n'a pas encore été réussi
        if self.score_job is None and game_key in jeux_avec_score and not self.games_success[game_key]:
            self.start_score_descendant()

        if self.current_game_key == game_key:
            return

        if self.current_game_key and self.current_game_key in self.games_instances:
            data = self.games_instances[self.current_game_key]
            data["frame"].pack_forget()

        if game_key in self.games_instances:
            self.games_instances[game_key]["frame"].pack(fill="both", expand=True)
            self.current_game_key = game_key
            return

        if game_key == "Enigmes":
            enigme_dir = os.path.dirname(self.scripts[game_key]["module_path"])
            if enigme_dir not in sys.path:
                sys.path.insert(0, enigme_dir)

        info = self.scripts[game_key]
        module_path = info["module_path"]
        if not os.path.exists(module_path):
            messagebox.showerror("Erreur", f"Script introuvable :\n{module_path}")
            return

        try:
            module_name = os.path.splitext(os.path.basename(module_path))[0]
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            game_frame = tk.Frame(self.content_frame, bg="white")
            game_frame.pack(fill="both", expand=True)

            game_instance = None
            success_callback = self.make_success_callback(game_key)

            # Lance le jeu choisi
            if hasattr(module, "ChronoQuizGame") and game_key == "ChronoQuiz":
                game_instance = module.ChronoQuizGame(
                    game_frame,
                    generated_words=self.generated_code,
                    group_score=self.group_score,
                    stop_callback=success_callback # ✅ callback pour arrêter le score
                )
                game_instance.start()
            elif hasattr(module, "ITQuizGame") and game_key == "IT Quiz":
                success_callback = self.make_success_callback("IT Quiz")  # crée le callback
                game_instance = module.ITQuizGame(
                    game_frame,
                    generated_words=self.generated_code,
                    group_score=self.group_score,
                    stop_callback=success_callback  # passe le callback correct
                )
                game_instance.start()

            elif hasattr(module, "main"):
                module.main(game_frame)
            elif hasattr(module, "EnigmesGame") and game_key == "Enigmes":
                game_instance = module.EnigmesGame(game_frame,correct_words=self.generated_code)
                game_instance.start()


            elif hasattr(module, "PuzzleGame") and game_key == "Puzzle":

                game_instance = module.PuzzleGame(

                    game_frame,

                    correct_password="hardware",

                    generated_words=self.generated_code,

                    group_score=self.group_score,

                    stop_callback=success_callback
                )

                game_instance.start()
            else:
                messagebox.showerror("Erreur", "Module de jeu incompatible ou introuvable")
                game_frame.destroy()
                return

            self.games_instances[game_key] = {"frame": game_frame, "instance": game_instance}
            self.current_game_key = game_key

        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de charger le jeu :\n{e}")

    # Revenir au menu
    def return_to_menu(self):
        if self.current_game_key and self.current_game_key in self.games_instances:
            data = self.games_instances[self.current_game_key]
            if data["instance"] and hasattr(data["instance"], "stop"):
                data["instance"].stop()
            data["frame"].pack_forget()
        self.current_game_key = None

def show_final_scores(self):
    # Cacher l'interface de sélection des jeux
    self.content_frame.pack_forget()

    # Créer une nouvelle fenêtre pour les scores
    score_frame = tk.Frame(self.root, bg="#f0f0f0")
    score_frame.pack(expand=True, fill="both")

    # Afficher le score du groupe
    group_score = self.get_group_total_score() # Une fonction à implémenter pour récupérer le score total
    tk.Label(score_frame, text="Votre Score Total", font=("Helvetica", 20, "bold"), bg="#f0f0f0").pack(pady=10)
    tk.Label(score_frame, text=f"{group_score}", font=("Helvetica", 48, "bold"), bg="#f0f0f0", fg="blue").pack(pady=20)

    # Afficher le classement
    high_scores = self.get_high_scores() # Une fonction à implémenter pour récupérer le top 3 des scores
    tk.Label(score_frame, text="Classement des Meilleurs Scores", font=("Helvetica", 16, "bold"), bg="#f0f0f0").pack(pady=10)

    # Utiliser un Treeview pour le classement
    from tkinter import ttk
    columns = ('rang', 'nom_groupe', 'score')
    tree = ttk.Treeview(score_frame, columns=columns, show='headings')
    tree.heading('rang', text='Rang')
    tree.heading('nom_groupe', text='Groupe')
    tree.heading('score', text='Score')
    tree.pack(pady=10)

    for i, (nom, score) in enumerate(high_scores):
        tree.insert('', tk.END, values=(i + 1, nom, score))

    # Bouton de retour ou de fin
    tk.Button(score_frame, text="Retour au menu principal", command=self.return_to_menu, font=("Helvetica", 12)).pack(pady=20)


class LoginFrame(tk.Frame):
    def __init__(self, root, on_login_success):
        super().__init__(root)
        self.root = root
        self.on_login_success = on_login_success

        tk.Label(self, text="Nom du groupe :", font=("Arial", 12)).pack(pady=10)
        self.entry_group = tk.Entry(self, font=("Arial", 12))
        self.entry_group.pack(pady=5)

        tk.Button(self, text="Se connecter", font=("Arial", 16),
                  command=self.verify_group, bg="green", fg="white").pack(pady=10)

        def creer():
            name = self.entry_group.get()
            print(name)
            create_group(name)
            self.on_login_success()



        tk.Button(self, text="Nouveau Groupe",font=("Arial", 16), command=creer, bg="blue", fg="white").pack(pady=10)


        self.status_label = tk.Label(self, text="", fg="red", font=("Arial", 10))
        self.status_label.pack()


    #Fonction pour vérifier si un groupe existe deja ou pas.
    def verify_group(self):
        name = self.entry_group.get()
        group_id = identification(name)
        if group_id:
            variable.selected_group_id = group_id
            self.on_login_success()
        else:
            self.status_label.config(text="Groupe introuvable ❌")

def main():#Création de la fenetre de login
    root = tk.Tk()
    root.geometry("800x600")
    root.title("Connexion groupe")

    def start_launcher():
        for widget in root.winfo_children():
            widget.destroy()
        ScriptLauncherApp(root)

    LoginFrame(root, on_login_success=start_launcher).pack(fill="both", expand=True)
    root.mainloop()





if __name__ == "__main__":
    main()
