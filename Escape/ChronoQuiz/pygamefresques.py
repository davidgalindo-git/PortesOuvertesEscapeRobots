import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import os
from Admin.gestionsql import recuperation_frag,identification
import variable

class ChronoQuizGame:
    def __init__(self, parent_frame, generated_words=None, group_score=None,stop_callback=None):
        self.parent = parent_frame
        self.canvas = None
        self.zones = []
        self.etiquettes = []
        self.drag_data = {"widget": None}
        self.running = False
        self.generated_words = generated_words
        self.word_label = tk.Label(self.parent, text="", font=("Arial", 16, "italic"), fg="green", bg="white")
        self.group_score = group_score
        self.stop_callback = stop_callback

    # Données du quiz
    dates = [1936,1956,1981, 1991, 2007, "Actuellement"]
    number = ["1", "2", "3","4", "5", "6"]
    reponses_correctes = {
        1936: "5", "Actuellement": "3", 1956: "4",
        2007: "6", 1991: "1", 1981: "2"
    }
    images_paths = {
        "5": "Escape/ChronoQuiz/Turing.jpg", "3": "Escape/ChronoQuiz/IA.png", "4": "Escape/ChronoQuiz/Disquedur.jpg",
        "6": "Escape/ChronoQuiz/Iphone.jpg", "1": "Escape/ChronoQuiz/WWW.png", "2": "Escape/ChronoQuiz/IBM.jpg"
    }
    description = {
         "5": "Machine de Turing", "3": "L'intelligence Artificielle",
        "4": "Invention du disque dur", "6": "Premier iPhone",
        "1": "Naissance du World Wide Web", "2": "Premier IBM PC"
    }

    #Charger une image
    def charger_image(self, path):
        try:
            img = Image.open(path).resize((150, 150))
            return ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Erreur chargement image {path} : {e}")
            return None

    #Creation du dégradé en arrière plan, aider par Chatgpt
    def creer_degrade(self, canvas, width, height, color1, color2):
        r1, g1, b1 = canvas.winfo_rgb(color1)
        r2, g2, b2 = canvas.winfo_rgb(color2)
        r_ratio = (r2 - r1) / height
        g_ratio = (g2 - g1) / height
        b_ratio = (b2 - b1) / height
        for i in range(height):
            nr = int(r1 + (r_ratio * i)) >> 8
            ng = int(g1 + (g_ratio * i)) >> 8
            nb = int(b1 + (b_ratio * i)) >> 8
            color = f"#{nr:02x}{ng:02x}{nb:02x}"
            canvas.create_line(0, i, width, i, fill=color)

    def start(self):
        if self.canvas:
            self.canvas.pack_forget()
        for widget in self.parent.winfo_children():
            widget.destroy()
        self.word_label = tk.Label(self.parent, text="", font=("Arial", 16, "italic"), fg="green", bg="white")

        self.running = True
        self.canvas = tk.Canvas(self.parent, width=1600, height=900)
        self.canvas.pack(fill="both", expand=True)
        self.creer_degrade(self.canvas, 1600, 900, "#0000ff", "#00ffff")

        self.zones.clear()
        for i, year in enumerate(self.dates):
            tk.Label(self.canvas, text=str(year), font=("Arial", 14), bg="lightgray").place(x=250 + i * 180, y=40)
            frame = tk.Frame(self.canvas, width=150, height=150, bg="white", bd=2, relief="groove")
            frame.place(x=250 + i * 180, y=70)
            self.zones.append(frame)

        self.etiquettes.clear()
        self.drag_data = {"widget": None}

        random.shuffle(self.number)
        for i, desc in enumerate(self.number):
            img = self.charger_image(self.images_paths.get(desc, ""))
            label = tk.Label(self.canvas, image=img, text=desc, compound="top", bg="orange", font=("Arial", 12))
            label.image = img
            x_init = 250 + i *180
            y_init = 300
            label.place(x=x_init, y=y_init)
            label.x_init = x_init
            label.y_init = y_init
            label.bind("<Button-1>", self.start_drag)
            label.bind("<B1-Motion>", self.on_drag)
            label.bind("<ButtonRelease-1>", self.on_drop)
            self.etiquettes.append(label)

        btn_frame = tk.Frame(self.canvas, bg="lightgray")
        btn_frame.place(x=100, y=700)
        tk.Button(btn_frame, text="✅ Vérifier", command=self.verifier).pack(side="left", padx=10)
        tk.Button(btn_frame, text="🔁 Recommencer", command=self.recommencer).pack(side="left", padx=10)

        texte_descriptions = "\n".join(
            f"{desc} : {self.description.get(desc, 'Pas de description')}"
            for desc in sorted(self.description)
        )
        label_desc = tk.Label(self.canvas, text=texte_descriptions, wraplength=1500, bg="lightgray", font=("Arial", 12))
        label_desc.place(x=600, y=500)
        self.word_label.place(x=650, y=660)  # Affiche seulement si gagné
        self.word_label.config(text="")  # Caché au départ

    def stop(self):
        self.running = False
        if self.canvas:
            self.canvas.pack_forget()

    def pause(self):
        pass

    def resume(self):
        pass

    #Fonction pour le deplacement du clic gauche de la souris quand on commence à cliquer sur le clic gauche
    def start_drag(self, event):
        self.drag_data["widget"] = event.widget
        #Sauvegarde la position initiale
        self.drag_data["x_init"] = event.widget.winfo_x()
        self.drag_data["y_init"] = event.widget.winfo_y()

    #Fonction quand on reste appuyer sur le bouton gauche de la souris
    def on_drag(self, event):
        widget = self.drag_data["widget"]
        if widget and self.running:
            widget.place(x=event.x_root - self.parent.winfo_rootx(),
                         y=event.y_root - self.parent.winfo_rooty())

    #Fonction quand on lâche le bouton gauche de la souris
    def on_drop(self, event):
        widget = self.drag_data["widget"]
        if widget and self.running:
            dropped = False
            for zone in self.zones:
                zx, zy = zone.winfo_x(), zone.winfo_y()
                if abs(widget.winfo_x() - zx) < 75 and abs(widget.winfo_y() - zy) < 75:
                    # Vérifie si la zone est occupée
                    occupied = any(
                        hasattr(label, "zone_associee") and label.zone_associee == zone
                        for label in self.etiquettes if label != widget
                    )
                    if not occupied:
                        widget.place(x=zx, y=zy)
                        widget.zone_associee = zone
                        dropped = True
                    else:
                        messagebox.showinfo("Zone occupée", "Cette zone est déjà utilisée par une autre image.")
                    break

            if not dropped:
                # Revenir à la position initiale
                widget.place(x=self.drag_data["x_init"], y=self.drag_data["y_init"])
        self.drag_data["widget"] = None

    #Fonction pour vérifier si le quiz est correcte ou est faux
    def verifier(self):
        correct = True
        for i, zone in enumerate(self.zones):
            trouve = None
            for label in self.etiquettes:
                if hasattr(label, "zone_associee") and label.zone_associee == zone:
                    trouve = label
                    break
            if trouve and trouve.cget("text") == self.reponses_correctes[self.dates[i]]:
                trouve.config(fg="green")
            else:
                if trouve:
                    trouve.config(fg="red")
                    # Remettre l'étiquette à sa position initiale
                    trouve.place(x=trouve.x_init, y=trouve.y_init)

                    # Supprimer la zone associée car ce n'est pas la bonne
                    delattr(trouve, "zone_associee")



                correct = False
        if correct:
            messagebox.showinfo("Bravo", "Toutes les réponses sont correctes !")
            if self.generated_words and len(self.generated_words) > 1:
                code = recuperation_frag(variable.selected_group_id, "fragment2")
                messagebox.showinfo("Code", f"Voici le 2 ème code de l'énigme : {code}")
            if self.stop_callback:
                self.stop_callback()
        else:
            messagebox.showwarning("Erreur", "Certaines réponses sont incorrectes.")
            self.word_label.config(text="")  # Cacher si mauvaise réponse
         # **Appel du callback pour arrêter le score descendant**

    #Fonction pour recommencer le quiz et remet les widgets à leur place initiale
    def recommencer(self):
        for i, label in enumerate(self.etiquettes):
            label.place(x=250 + i * 180, y=300)
            label.config(fg="black")
            if hasattr(label, "zone_associee"):
                del label.zone_associee
