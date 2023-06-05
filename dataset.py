import tkinter as tk
import cv2
from PIL import Image, ImageTk
import os
import pandas as pd
import modelling_facenet
from main import MainClass


class GetDataset(tk.Frame):
    def __init__(self, root, main_panel, email, nama):
        super().__init__(root)
        self.root = root
        self.main_panel = main_panel
        self.email = email
        self.user = nama
        self.widget()

    # Memanggil fungsi show_frame() untuk memulai tampilan feed kamera
        self.show_frame()

    def widget(self):
        # Membuat frame baru untuk ucapan selamat
        self.getdataset_panel = tk.Frame(self.main_panel, bg="white")
        self.getdataset_panel.pack(fill="both", expand=True)

        # Membuat objek Canvas di tengah main panel
        self.canvas = tk.Canvas(self.getdataset_panel, width=300, height=40, bg="white", highlightthickness=0)
        self.canvas.pack(pady=(80,0))

        title_label = tk.Label(self.canvas, text="Rekam Data Wajah Peserta", font=("Arial", 16), bg="white", fg="#29AAE2", cursor="hand2")
        title_label.pack(padx=20)

        loading_cam_label = tk.Label(self.canvas, text="Memuat kamera . . .", font=("Arial", 12), bg="white", fg="black", cursor="hand2")
        loading_cam_label.pack(pady=40)

        self.canvas.update()  # Memperbarui tampilan canvas

        loading_cam_label.pack_forget()

        # Membuat objek Canvas di tengah main panel
        self.canvas_cam = tk.Canvas(self.getdataset_panel, width=300, height=200, bg="white", highlightthickness=0)
        self.canvas_cam.pack(pady=(20,0))

        # Membuat objek kamera
        self.camera = cv2.VideoCapture(0)

        self.start_button = tk.Button(self.getdataset_panel, text='Mulai', font=("Arial", 16), width=25, bg="#29AAE2", fg="#ffffff", border=0, cursor="hand2", command=self.show_instructions)
        self.start_button.pack(pady=(20,0))

        self.label_capture = tk.Label(self.getdataset_panel, text='Sedang mengambil gambar', font=("Arial", 12), width=25, bg="white", fg="black")
        self.label_capture.pack(pady=(30,0))
        self.label_capture.pack_forget()

        self.finish_button = tk.Button(self.getdataset_panel, text='Selesai', font=("Arial", 16), width=25, bg="#29AAE2", fg="#ffffff", border=0, cursor="hand2")
        self.finish_button.pack(pady=(20,0))
        self.finish_button.pack_forget()

        # Variabel untuk menyimpan frame yang akan ditangkap
        self.captured_frames = []
        self.capture_count = 0

    def show_mainpage (self):
        # Membuat instance dari MainClass
        self.main = MainClass(self.email)

    # Fungsi untuk melakukan penangkapan frame selama 10 detik
    def start_capture(self):
        self.start_button.pack_forget()
        self.label_capture.pack(pady=(30,0))

        if self.capture_count < 10:
            _, frame = self.camera.read()
            frame = cv2.resize(frame, (1280, 720))  # Ubah ukuran frame menjadi 1280x720
            self.captured_frames.append(frame)
            self.capture_count += 1
            self.label_capture.config(text="Ambil Gambar Frame ke: {}".format(self.capture_count))
            print("Frame captured:", self.capture_count)
            self.canvas_cam.after(1000, self.start_capture)  # Melanjutkan penangkapan setelah 1 detik
        else:
            self.capture_count = 0
            print("All frames captured.")
            self.label_capture.config(text="Ambil Gambar Selesai")
            self.popup_capture_selesai()

    # Fungsi untuk menampilkan frame kamera di canvas_cam
    def show_frame(self):
        _, frame = self.camera.read()
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (300, 200))
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        photo = ImageTk.PhotoImage(image)

        self.canvas_cam.create_image(0, 0, anchor="nw", image=photo)
        self.canvas_cam.image = photo

        self.canvas_cam.after(10, self.show_frame)

    def show_instructions(self):
        instructions = """Pengambilan Gambar Wajah Peserta

1. Gambar akan diambil selama 10 detik
2. Pastikan wajah terlihat jelas dengan cahaya yang cukup
3. Tidak ada benda yang menghalangi wajah
4. Pastikan bagian mata, mulut, dan hidung terlihat
5. Bisa melakukan gerakan dari posisi lain seperti tengok kanan dan kiri asalkan poin no 4 terpenuhi"""

        popup = tk.Toplevel(self.getdataset_panel)
        popup.title("Petunjuk Pemakaian")

        label = tk.Label(popup, text=instructions, justify="left")
        label.pack(padx=20, pady=20)

        button_ok = tk.Button(popup, text="Oke", command=lambda: [popup.destroy(), self.start_capture()])
        button_ok.pack(pady=10)

        # Memposisikan popup di tengah layar
        popup.geometry("+{}+{}".format(int(self.getdataset_panel.winfo_screenwidth() / 2 - popup.winfo_reqwidth() / 2),
                                      int(self.getdataset_panel.winfo_screenheight() / 2 - popup.winfo_reqheight() / 2)))


    def popup_capture_selesai(self):
        popup = tk.Toplevel(self.getdataset_panel)
        popup.title("Capture Selesai")

        label = tk.Label(popup, text="Apakah wajah sudah terlihat jelas pada gambar yang sudah diambil berikut?.", justify="left")
        label.pack(padx=20, pady=20)

        frame_container = tk.Frame(popup)
        frame_container.pack(padx=20, pady=10)

        num_rows = 2
        num_cols = 5

        for i, frame in enumerate(self.captured_frames):
            # Konversi frame BGR OpenCV menjadi gambar PIL
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image)

            # Resize gambar sesuai ukuran yang diinginkan
            target_width = 300 // num_cols
            target_height = 200 // num_rows
            image = image.resize((target_width, target_height))

            # Konversi gambar PIL menjadi format yang dapat ditampilkan di Tkinter
            photo = ImageTk.PhotoImage(image)

            # Menampilkan gambar di label
            label_frame = tk.Label(frame_container, image=photo)
            label_frame.image = photo
            row = i // num_cols
            col = i % num_cols
            label_frame.grid(row=row, column=col, padx=5, pady=5)

        button_ok = tk.Button(popup, text="Oke", command=lambda: [popup.destroy(), self.save_frames(self.captured_frames)])
        button_ok.pack(side="right", padx=5, pady=10)

        button_cancel = tk.Button(popup, text="Batal", command=lambda: [popup.destroy(), self.cancel_save_frames()])
        button_cancel.pack(side="right", padx=5, pady=10)

        # Memposisikan popup di tengah layar
        popup.geometry("+{}+{}".format(int(self.getdataset_panel.winfo_screenwidth() / 2 - popup.winfo_reqwidth() / 2),
                                      int(self.getdataset_panel.winfo_screenheight() / 2 - popup.winfo_reqheight() / 2)))



    def save_frames(self, frames):
        # Membuat direktori "dataset/user/image" jika belum ada
        dataset_dir = os.path.join("database", self.user, "image")
        if not os.path.exists(dataset_dir):
            os.makedirs(dataset_dir)

        for i, frame in enumerate(frames):
            # Menentukan path file untuk setiap frame
            file_path = os.path.join(dataset_dir, f"frame_{i}.jpg")

            # Menyimpan frame sebagai gambar dengan format JPEG
            cv2.imwrite(file_path, frame)

        self.label_capture.config(text="Sedang membuat model . . .")
        self.getdataset_panel.update()
        self.get_model(self.user)
        self.label_capture.pack_forget()
        self.finish_button.pack(pady=(20,0))
        self.save_data()
        print("Frames berhasil disimpan di:", dataset_dir)
        self.root.destroy()
        self.show_mainpage()

    def get_model(self, user):
        self.dataset, self.model = modelling_facenet.modelling(user)

    def save_data(self):
        list_data = {'nama': [self.user],
                  'dataset': [self.dataset],
                  'model': [self.model]}

        df_new = pd.DataFrame(list_data)

        # Mengubah path file jika diperlukan
        file_path = 'registrations.xlsx'
        if not os.path.isabs(file_path):
            file_path = os.path.join(os.getcwd(), file_path)

        if os.path.isfile(file_path):
            # Load data dari file
            df_existing = pd.read_excel(file_path)

            # Menggunakan indeks sebagai kunci untuk memperbarui nilai
            df_existing.set_index('nama', inplace=True)
            df_new.set_index('nama', inplace=True)
            df_existing.update(df_new)

            # Mengembalikan indeks ke kolom
            df_existing.reset_index(inplace=True)

            # Menyimpan data yang diperbarui
            df_existing.to_excel(file_path, index=False)
            print("Data berhasil diperbarui di:", file_path)
        else:
            df_new.to_excel(file_path, index=False)
            print("Data baru berhasil disimpan di:", file_path)

    def cancel_save_frames(self):
        self.label_capture.pack_forget()
        self.start_button.pack(pady=(20,0))

    