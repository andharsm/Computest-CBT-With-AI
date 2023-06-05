import tkinter as tk
from PIL import ImageTk, Image

class AboutUs:
    def __init__(self, master):
        self.root = tk.Toplevel(master)
        self.photo_logo_computest = None
        self.photo_logo = None  # Menambahkan atribut untuk menyimpan referensi gambar logo
        self.photo = None 
        self.show_main()

    def show_main(self):
        # Atur ukuran layar
        # Atur warna background jendela
        self.root.configure(bg="white")

        # Atur form muncul di tengah layar
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_cordinate = int((screen_width / 2) - (900 / 2))
        y_cordinate = int((screen_height / 2) - (520 / 2))
        self.root.geometry("{}x{}+{}+{}".format(900, 520, x_cordinate, y_cordinate))

        # Membuka gambar menggunakan PIL
        logo_1 = Image.open("images/computest_blue_resized.png")

        # Membuat objek PhotoImage dari gambar
        self.photo_logo_computest = ImageTk.PhotoImage(logo_1)

        # Membuat label dengan gambar
        logo_computest = tk.Label(self.root, image=self.photo_logo_computest, bd=0)
        logo_computest.place(x=50, y=25)

        # Membuka gambar menggunakan PIL
        logo = Image.open("images/logo_orbit_resized.png")

        # Membuat objek PhotoImage dari gambar
        self.photo_logo = ImageTk.PhotoImage(logo)

        # Membuat label dengan gambar
        logo_orbit = tk.Label(self.root, image=self.photo_logo, bd=0)
        logo_orbit.place(x=900-50-156, y=25)

        content = """Computest adalah solusi inovatif yang dirancang untuk mengatasi masalah yang dihadapi dalam ujian berbasis komputer (CBT). Dalam menghadapi maraknya joki dan kecurangan yang dilakukan oleh peserta, kami berkomitmen untuk memberikan solusi yang efektif dengan menerapkan teknologi kecerdasan buatan (AI) pada CBT.
        
        Computest hadir untuk meminimalisir subjektivitas dan meningkatkan efektivitas dalam pengawasan serta pengoreksian hasil ujian. Dengan menggunakan teknologi terkini seperti Computer Vision dan Natural Language Processing, kami memberikan standar keamanan tinggi untuk memastikan integritas dan validitas setiap ujian. Kami berdedikasi penuh untuk menyediakan platform yang andal, akurat, dan inovatif untuk mendukung sistem evaluasi yang adil dan transparan."""

        label = tk.Label(self.root, text=content, wraplength=800, justify='center', bg='white')
        label.place(x=50, y=80)

        # Membuka gambar menggunakan PIL
        image = Image.open("images/banner_aboutus_resize.png")

        # Membuat objek PhotoImage dari gambar
        self.photo = ImageTk.PhotoImage(image)

        # Membuat label dengan gambar
        baner_anggota = tk.Label(self.root, image=self.photo, bd=0)
        baner_anggota.place(x=0, y=240)

        # Menjalankan event loop Tkinter
        self.root.mainloop()