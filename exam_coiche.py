import tkinter as tk
import datetime
from exam_sheet import ExamSheet


class Exam(tk.Frame):
    def __init__(self,root, main_panel, user):
        self.root =root
        self.main_panel = main_panel
        self.user = user
        self.create_widgets()


    def create_widgets(self):
        self.exam_panel = tk.Frame(self.main_panel, width=950, height=450, bg="white")
        self.exam_panel.pack(pady=(50, 0))

        self.coiche_exam()
    def show_examsheet(self):
        # Membuat instance dari DataForm dengan parent data_window
        self.exam_panel.destroy()
        self.getExamSheet = ExamSheet(self.root, self.main_panel, self.user)

    def coiche_exam(self):
        self.canvas_1 = tk.Canvas(self.exam_panel, width=610, height=60, bg="#29AAE2")
        self.canvas_1.place(x=170, y=25)

        self.canvas_2 = tk.Canvas(self.exam_panel, width=610, height=60, bg="#D3D3D3")
        self.canvas_2.place(x=170, y=105)

        self.canvas_3 = tk.Canvas(self.exam_panel, width=610, height=60, bg="#D3D3D3")
        self.canvas_3.place(x=170, y=185)

        self.canvas_4 = tk.Canvas(self.exam_panel, width=610, height=60, bg="#D3D3D3")
        self.canvas_4.place(x=170, y=265)

        self.coiche_1 = tk.Canvas(self.canvas_1, width=600, height=50, bg="white")
        self.coiche_1.place(x=5, y=5)

        self.coiche_2 = tk.Canvas(self.canvas_2, width=600, height=50, bg="white")
        self.coiche_2.place(x=5, y=5)

        self.coiche_3 = tk.Canvas(self.canvas_3, width=600, height=50, bg="white")
        self.coiche_3.place(x=5, y=5)

        self.coiche_4 = tk.Canvas(self.canvas_4, width=600, height=50, bg="white")
        self.coiche_4.place(x=5, y=5)

        x_button = 600-93-5
        y_button = (50-38)/2

        self.button_1 = tk.Button(self.coiche_1, text='Kerjakan', font=("Arial", 16), bg="#29AAE2", fg="#ffffff", border=0, cursor="hand2", command=self.show_examsheet)
        self.button_1.place(x=x_button, y=y_button)

        self.button_2 = tk.Button(self.coiche_2, text='Kerjakan', font=("Arial", 16), bg="#D3D3D3", fg="#ffffff", border=0, cursor="hand2")
        self.button_2.place(x=x_button, y=y_button)

        self.button_3 = tk.Button(self.coiche_3, text='Kerjakan', font=("Arial", 16), bg="#D3D3D3", fg="#ffffff", border=0, cursor="hand2")
        self.button_3.place(x=x_button, y=y_button)

        self.button_4 = tk.Button(self.coiche_4, text='Kerjakan', font=("Arial", 16), bg="#D3D3D3", fg="#ffffff", border=0, cursor="hand2")
        self.button_4.place(x=x_button, y=y_button)

        y_label = (50-30)/2
        label_1 = tk.Label(self.coiche_1, text="Data Science", font=("Arial", 16), bg="white", fg="#29AAE2")
        label_1.place(x=5, y=y_label)

        label_2 = tk.Label(self.coiche_2, text="Computer Vision", font=("Arial", 16), bg="white", fg="#D3D3D3")
        label_2.place(x=5, y=y_label)

        label_3 = tk.Label(self.coiche_3, text="Reinforce Learning", font=("Arial", 16), bg="white", fg="#D3D3D3")
        label_3.place(x=5, y=y_label)

        label_4 = tk.Label(self.coiche_4, text="Deployment", font=("Arial", 16), bg="white", fg="#D3D3D3")
        label_4.place(x=5, y=y_label)

        x_today = 600-93-5-55-10
        y_today = (50-24)/2
        label_today = tk.Label(self.coiche_1, text='Hari ini', font=("Arial", 12), bg="white", fg="#29AAE2")
        label_today.place(x=x_today, y=y_today)

        today = datetime.date.today()

        day_2 = today + datetime.timedelta(days=1)
        day_2_formatted = day_2.strftime("%d-%m-%Y")

        day_3 = today + datetime.timedelta(days=2)
        day_3_formatted = day_3.strftime("%d-%m-%Y")

        day_4 = today + datetime.timedelta(days=3)
        day_4_formatted = day_4.strftime("%d-%m-%Y")

        x_day = 600-93-5-88-10
        y_day = (50-24)/2
        label_day_2 = tk.Label(self.coiche_2, text=day_2_formatted, font=("Arial", 12), bg="white", fg="#D3D3D3")
        label_day_2.place(x=x_day, y=y_day)

        label_day_3 = tk.Label(self.coiche_3, text=day_3_formatted, font=("Arial", 12), bg="white", fg="#D3D3D3")
        label_day_3.place(x=x_day, y=y_day)

        label_day_4 = tk.Label(self.coiche_4, text=day_4_formatted, font=("Arial", 12), bg="white", fg="#D3D3D3")
        label_day_4.place(x=x_day, y=y_day)


'''root = tk.Tk()
# atur ukuran jendela aplikasi
root.geometry("1000x700")

# atur warna background jendela
root.configure(bg="white")
exam = Exam(root)
root.mainloop()'''
