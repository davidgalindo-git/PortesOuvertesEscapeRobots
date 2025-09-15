from tkinter import *
from tkinter import messagebox
import tkinter.font
import tkinter as tk
from tkinter import ttk
from gestionsql import *

def creer ():
    name = entry_name_group.get()
    print(name)
    create_group(name)

groups = read_data()


inter = Tk()
inter.geometry("400x500")
inter.title('Gestion de groupe enigme')
inter.configure(bg="#FFFFFF")

tk.Label(inter, text="Nom du nouveau groupe :", font=("Arial", 12)).grid(row=1, column=5, padx=5, pady=2)
entry_name_group = tk.Entry(inter, font=("Arial", 12))
entry_name_group.grid(row=1, column=5, padx=5, pady=2)

bouton_creer = tk.Button(inter, text="Créer", command=creer, bg="green", fg="white")
bouton_creer.grid(row=2, columnspan=3, pady=5, padx=5)

colonnes_groupes = ("ID", "Groupe", "Code")
tableau_groupes = ttk.Treeview(inter, columns=colonnes_groupes, show="headings")

tableau_groupes.grid(row=3, column=1, columnspan=10, padx=10, pady=10, sticky="nsew")

for col in colonnes_groupes:
    tableau_groupes.heading(col, text=col)
    tableau_groupes.column(col, width=100)

for ligne in groups:
    tableau_groupes.insert("", tk.END, values=ligne)



inter.mainloop()