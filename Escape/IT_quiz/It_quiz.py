import tkinter as tk
from tkinter import messagebox
from Escape.Enigme.codes import main as get_random_words
import csv
import random
import os
from Admin.gestionsql import recuperation_frag
import variable
class ITQuizGame:
    def __init__(self, parent, generated_words=None, group_score=None, stop_callback=None):

        self.parent = parent
        self.frame = tk.Frame(self.parent, bg="white")
        self.score = 0
        self.current_question = 0
        self.success_goal = 33.33
        self.generated_words = generated_words
        self.group_score = group_score

        self.final_result_label = tk.Label(self.frame, text="", font=("Helvetica", 14, "bold"), fg="darkgreen",bg="white")
        self.final_result_label.pack(pady=(10, 5))

        csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "IT_quiz_data.csv")
        self.questions = self.load_questions_from_csv(csv_path)

        self.word_hint_label = tk.Label(self.frame,
                                        font=("Helvetica", 14, "italic"),
                                        fg="darkgreen",
                                        bg="white")

        self.info_label = tk.Label(self.frame, text="", font=("Helvetica", 12), fg="blue", bg="white")
        self.question_label = tk.Label(self.frame, text="", wraplength=580, font=("Helvetica", 14), bg="white")
        self.answer_var = tk.StringVar(value="")

        self.radio_buttons = [tk.Radiobutton(self.frame, text="", variable=self.answer_var, value=val,
                                             font=("Helvetica", 12), bg="white") for val in ['a', 'b', 'c', 'd']]

        self.submit_btn = tk.Button(self.frame, text="Valider", command=self.submit_answer, font=("Helvetica", 12))
        self.feedback_label = tk.Label(self.frame, text="", font=("Helvetica", 12), bg="white")
        self.restart_btn = tk.Button(self.frame, text="Recommencer", command=self.restart_quiz, font=("Helvetica", 10))

        self.info_label.pack(pady=(10, 0))
        self.question_label.pack(pady=20)
        for rb in self.radio_buttons:
            rb.pack(anchor='w', padx=50, pady=2)
        self.submit_btn.pack(pady=20)
        self.feedback_label.pack()
        self.restart_btn.place(x=500, y=10, width=90, height=30)

        self.started = False

    def start(self):
        if not self.started:
            self.frame.pack(fill="both", expand=True)
            self.started = True
            self.update_info_label()
            self.display_question()
        else:
            self.frame.pack(fill="both", expand=True)

    def update_info_label(self):
        percent_score = (self.score / len(self.questions)) * 100 if self.questions else 0
        self.info_label.config(text=f"Score: {self.score}/{len(self.questions)} ({percent_score:.0f}%) | Objectif: {self.success_goal}%")

    def display_question(self):
        self.answer_var.set("")
        self.feedback_label.config(text="")
        self.update_info_label()
        q = self.questions[self.current_question]
        self.question_label.config(text=f"Question {self.current_question + 1} : {q['question']}")
        options = q["options"]
        for i, key in enumerate(['a', 'b', 'c', 'd']):
            self.radio_buttons[i].config(text=f"{key}) {options[key]}")
        self.submit_btn.config(state="normal")

    def submit_answer(self):
        selected = self.answer_var.get()
        if not selected:
            messagebox.showwarning("Attention", "Veuillez sélectionner une réponse.")
            return
        correct = self.questions[self.current_question]["answer"]
        if selected == correct:
            self.score += 1
            self.feedback_label.config(text="Bonne réponse !", fg="green")
        else:
            correct_text = self.questions[self.current_question]["options"][correct]
            self.feedback_label.config(text=f"Mauvaise réponse. La bonne réponse était: {correct}) {correct_text}", fg="red")

        self.submit_btn.config(state="disabled")
        self.update_info_label()
        self.parent.after(1500, self.next_question)

    def next_question(self):
        self.current_question += 1
        if self.current_question == len(self.questions):
            self.show_result()
        else:
            self.display_question()

    def show_result(self):
        percent_score = (self.score / len(self.questions)) * 100
        result_text = f"Quiz terminé !\nVotre score: {self.score} sur {len(self.questions)} ({percent_score:.2f}%)."

        if percent_score >= self.success_goal:
            result_text += "\n\nFélicitations, vous avez atteint l'objectif !"
            code = recuperation_frag(variable.selected_group_id, "fragment1")
            if self.generated_words:
                result_text += f"\n\nVoici le Premier code de l'énigme : {code}"
        else:
            result_text += "\n\nVous n'avez pas atteint l'objectif. Bonne chance la prochaine fois !"

        self.final_result_label.config(
            text=result_text,
            fg="darkgreen" if percent_score >= self.success_goal else "red"
        )

        # ✅ Stop le score descendant si callback défini
        if self.group_score and hasattr(self.group_score, "set"):
            pass  # tu gardes ton score de groupe si tu veux
        if hasattr(self, "stop_callback") and self.stop_callback:
            self.stop_callback()

    def restart_quiz(self):
        self.score = 0
        self.current_question = 0
        for rb in self.radio_buttons:
            rb.config(state="normal")
        self.submit_btn.config(state="normal")
        self.feedback_label.config(text="")
        self.display_question()

    def load_questions_from_csv(self, filename):
        questions = []
        try:
            with open(filename, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    question = {
                        "question": row["question"],
                        "options": {
                            "a": row["answer a"],
                            "b": row["answer b"],
                            "c": row["answer c"],
                            "d": row["answer d"]
                        },
                        "answer": row["right answer"].strip().lower()
                    }
                    questions.append(question)
            return random.sample(questions, 6)
        except Exception as e:
            messagebox.showerror("Erreur", f"Chargement échoué : {e}")
            return []
