import tkinter as tk
from collections import defaultdict
import pandas as pd
from corection_answer import SemanticSimilarity
import os


class ExamSheet(tk.Frame):
    def __init__(self, root, main_panel, user):
        super().__init__(main_panel)
        self.root =root
        self.main_panel = main_panel
        self.user = user
        self.text_values = {}  # Dictionary untuk menyimpan teks di tk.Text
        self.jawaban = []
        self.scores = []
        self.nilai = []
        self.semantic_sim = SemanticSimilarity()

        self.create_widgets()

    def create_widgets(self):
        self.exam_panel = tk.Frame(self.main_panel, width=970, height=450, bg="white")
        self.exam_panel.pack(pady=(50, 0))

        self.form_answer()
        self.display_answering()

        self.jawaban_dict = defaultdict(str)

    def next_button_clicked(self):
        # Menyimpan teks dari input saat ini ke variabel jawaban yang sesuai
        essay_text = self.essay_input.get("1.0", "end-1c")
        self.jawaban_dict[self.current_index + 1] = essay_text

        self.current_index = (self.current_index + 1) % len(self.questions)  # Menggunakan modulus untuk mengulang dari awal jika mencapai pertanyaan terakhir
        self.current_question.set(self.questions[self.current_index])
        self.essay_input.delete("1.0", "end")  # Menghapus teks pada input

        # Mengisi kembali input teks dengan jawaban yang sudah ada
        previous_answer = self.jawaban_dict[self.current_index + 1]
        self.essay_input.insert("1.0", previous_answer)

        self.color_button()

    def color_button(self):
        for i in range(1, 6):
            if i in self.jawaban_dict and self.jawaban_dict[i] != "":
                getattr(self, f"display_{i}").configure(bg="#29AAE2")  # Mengatur warna latar belakang tombol menjadi biru
            else:
                getattr(self, f"display_{i}").configure(bg="#D3D3D3")  # Mengatur warna latar belakang tombol menjadi abu-abu

    def show_question(self, question_index):
        # Menyimpan teks dari input saat ini ke variabel jawaban yang sesuai
        essay_text = self.essay_input.get("1.0", "end-1c")
        self.jawaban_dict[self.current_index + 1] = essay_text

        self.current_index = question_index - 1  # Mengubah current_index sesuai dengan nomor pertanyaan yang dipilih
        self.current_question.set(self.questions[self.current_index])
        self.essay_input.delete("1.0", "end")  # Menghapus teks pada input

        # Mengisi kembali input teks dengan jawaban yang sudah ada
        previous_answer = self.jawaban_dict[self.current_index + 1]
        self.essay_input.insert("1.0", previous_answer)

        self.color_button()

    def get_scores(self,):
        self.next_button_clicked()
        for i in range(1, 6):
            if self.jawaban_dict[i]:
                get_jawaban = self.jawaban_dict[i]
                self.jawaban.append(get_jawaban)
                print(f"jawaban_{i} =", self.jawaban_dict[i])
            else:
                get_jawaban = "belum diisi"
                self.jawaban.append(get_jawaban)
                print(f"jawaban_{i} = belum diisi")

        for i in range(len(self.jawaban)):
            scores = []
            for j in range(len(list(self.answer_master[i]))):
                similarity_score = self.semantic_sim.calculate_similarity_score(list(self.answer_master[i].values())[j], self.jawaban[i])
                scores.append(similarity_score)
            highscore = max(scores)
            if highscore > 0.75:
                nilai = "Sangat Baik"
            elif highscore < 0.4:
                nilai = "Kurang Baik"
            else:
                nilai = "Baik"
            print("highscore jawaban[{}]: {}".format(i, highscore))
            print("nilai jawaban[{}]: {}".format(i, nilai))
            self.scores.append(highscore)
            self.nilai.append(nilai)

        df = pd.DataFrame({"Pertanyaan": self.questions, "Jawaban": self.jawaban, "Score": self.scores, "Nilai": self.nilai})
        print(df)

        dataset_dir = os.path.join("database", self.user, "result")
        if not os.path.exists(dataset_dir):
            os.makedirs(dataset_dir)

        # Simpan dataframe ke file Excel di dalam folder yang ditentukan
        file_path = os.path.join(dataset_dir, "result_"+self.user+".xlsx")
        df.to_excel(file_path, index=False)

        self.root.destroy()
                

    def form_answer(self):
        self.answer_canvas = tk.Canvas(self.exam_panel, width=620, height=390, bg="#29AAE2")
        self.answer_canvas.place(x=0, y=20)

        self.input_canvas = tk.Canvas(self.answer_canvas, width=610, height=380, bg="white")
        self.input_canvas.place(x=5, y=5)

        # Daftar pertanyaan
        self.questions = [
            "1. Apa yang dimaksud dengan data cleansing dalam data science?",
            "2. Apa yang dimaksud dengan supervised learning dalam machine learning?",
            "3. Apa yang dimaksud dengan overfitting dalam konteks model machine learning?",
            "4. Apa yang dimaksud dengan regresi linear dalam analisis statistik?",
            "5. Apa yang dimaksud dengan big data dalam konteks data science?"
        ]


        self.answer_master = {
            0: {
                "Definisi 1": "Data cleansing adalah proses membersihkan dan menghilangkan data yang tidak valid atau korup.",
                "Definisi 2": "Data cleansing adalah tahap pembersihan data dari kecacatan, kesalahan, atau duplikasi.",
                "Definisi 3": "Data cleansing adalah langkah-langkah untuk memastikan kebersihan dan kualitas data."
            },
            1: {
                "Definisi 1": "Supervised learning adalah metode di mana model belajar dari data berlabel.",
                "Definisi 2": "Supervised learning adalah teknik di mana model mempelajari hubungan antara fitur dan label yang telah diberikan.",
                "Definisi 3": "Supervised learning adalah teknik pembelajaran di mana model mencari pola atau hubungan antara fitur input dan label output yang sudah diketahui."
            },
            2: {
                "Definisi 1": "Overfitting terjadi ketika model machine learning terlalu 'terlatih' pada data pelatihan, sehingga tidak dapat melakukan generalisasi dengan baik pada data baru.",
                "Definisi 2": "Overfitting adalah kondisi di mana model machine learning terlalu kompleks dan terlalu cocok dengan data pelatihan, sehingga kinerjanya menurun saat diuji dengan data baru.",
                "Definisi 3": "Overfitting terjadi saat model machine learning terlalu spesifik untuk data pelatihan dan kehilangan kemampuan untuk mengenali pola umum dalam data."
            },
            3: {
                "Definisi 1": "Regresi linear adalah metode statistik untuk memodelkan hubungan linier antara variabel dependen dan satu atau lebih variabel independen.",
                "Definisi 2": "Regresi linear adalah teknik analisis statistik yang digunakan untuk memprediksi nilai variabel dependen berdasarkan variabel independen dengan menggunakan persamaan garis lurus.",
                "Definisi 3": "Regresi linear adalah pendekatan statistik yang digunakan untuk memahami dan menggambarkan hubungan linear antara variabel-variabel dalam suatu data set."
            },
            4: {
                "Definisi 1": "Big data adalah istilah yang digunakan untuk menggambarkan volume besar, kecepatan tinggi, dan keragaman data yang tidak bisa diolah dengan metode tradisional.",
                "Definisi 2": "Big data mengacu pada kumpulan data yang sangat besar dan kompleks yang memerlukan teknik-teknik khusus untuk diproses, dianalisis, dan diekstraksi informasinya.",
                "Definisi 3": "Big data merujuk pada data dalam skala yang sangat besar yang melibatkan ukuran, kompleksitas, dan kecepatan pemrosesan yang melebihi kapabilitas alat dan metode tradisional."
            }
        }

        self.current_index = 0

        # Pertanyaan saat ini
        self.current_question = tk.StringVar()
        self.current_question.set(self.questions[self.current_index])

        # Membuat label pertanyaan
        label_question = tk.Label(self.input_canvas, textvariable=self.current_question)
        label_question.place(x=20, y=20)

        # Membuat input teks
        self.essay_input = tk.Text(self.input_canvas, height=12, width=72, bg="#D3D3D3")
        self.essay_input.place(x=(620-580)/2, y=310-180-20)

        # Membuat tombol "Selanjutnya"
        next_button = tk.Button(self.input_canvas, text="Selanjutnya", font=("Arial", 16), bg="#29AAE2", fg="#ffffff", border=0, cursor="hand2", command=self.next_button_clicked)
        next_button.place(x=610-122-15, y=380-38-15)

    def display_answering(self):
        self.display = tk.Canvas(self.exam_panel, width=310, height=390, bg="#29AAE2")
        self.display.place(x=650, y=20)

        self.display_canvas = tk.Canvas(self.display, width=300, height=380, bg="white")
        self.display_canvas.place(x=5, y=5)

        self.display_1 = tk.Button(self.display_canvas, text='1', font=("Arial", 20), width=4, height=2, bg="#D3D3D3", fg="#ffffff", cursor="hand2", command=lambda: self.show_question(1))
        self.display_1.place(x=20, y=15)     

        self.display_2 = tk.Button(self.display_canvas, text='2', font=("Arial", 20), width=4, height=2, bg="#D3D3D3", fg="#ffffff", cursor="hand2", command=lambda: self.show_question(2))
        self.display_2.place(x=114, y=15)

        self.display_3 = tk.Button(self.display_canvas, text='3', font=("Arial", 20), width=4, height=2, bg="#D3D3D3", fg="#ffffff", cursor="hand2", command=lambda: self.show_question(3))
        self.display_3.place(x=208, y=15)

        self.display_4 = tk.Button(self.display_canvas, text='4', font=("Arial", 20), width=4, height=2, bg="#D3D3D3", fg="#ffffff", cursor="hand2", command=lambda: self.show_question(4))
        self.display_4.place(x=20, y=114)

        self.display_5 = tk.Button(self.display_canvas, text='5', font=("Arial", 20), width=4, height=2, bg="#D3D3D3", fg="#ffffff", cursor="hand2", command=lambda: self.show_question(5))
        self.display_5.place(x=114, y=114)

        self.button_finish = tk.Button(self.display_canvas, text='Selesai', font=("Arial", 16), bg="#29AAE2", fg="#ffffff", border=0, cursor="hand2", command=self.get_scores)
        self.button_finish.place(x=300-84-15, y=380-38-15)

        

'''if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("1000x600")
    root.title("Exam Answer Sheet")
    main_panel = tk.Frame(root, bg="#F0F0F0")
    main_panel.pack(fill='both', expand=True)

    app = ExamSheet(root, main_panel, 'ainun')
    app.pack(fill='both', expand=True)

    root.mainloop()'''
