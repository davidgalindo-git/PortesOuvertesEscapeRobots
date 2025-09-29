import tkinter as tk
from tkinter import ttk

def show_scoreboard(root, high_scores, group_score):
    # Fenêtre popup
    win = tk.Toplevel(root)
    win.title("Scoreboard")
    win.geometry("500x400")

    # Score du groupe actuel
    tk.Label(win, text=f"Votre score : {group_score}", font=("Helvetica", 16, "bold")).pack(pady=10)

    # Tableau des meilleurs scores
    tk.Label(win, text="Classement :", font=("Helvetica", 14, "bold")).pack(pady=5)
    columns = ("rang", "groupe", "score")
    tree = ttk.Treeview(win, columns=columns, show="headings")
    tree.heading("rang", text="Rang")
    tree.heading("groupe", text="Groupe")
    tree.heading("score", text="Score")
    tree.pack(expand=True, fill="both", padx=10, pady=10)

    for i, (groupe, score) in enumerate(high_scores, start=1):
        tree.insert("", "end", values=(i, groupe, score))
