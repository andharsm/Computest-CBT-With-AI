import tkinter as tk
from turtle import width
from about import AboutUs
from login_regis import LoginForm
from about import AboutUs
from PIL import ImageTk, Image

def on_panel_clicked(event):
    # Menghilangkan fokus dari login_email
    root.focus()

root = tk.Tk()

# atur judul jendela aplikasi
root.title("CBT Apps")

# Nonaktifkan tombol resize
root.resizable(False, False)

w = 900
h = 520

# atur ukuran jendela aplikasi
root.geometry("900x520")

# atur warna background jendela
root.configure(bg="white")

# atur form muncul di tengah layar
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_cordinate = int((screen_width / 2) - (w / 2))
y_cordinate = int((screen_height / 2) - (h / 2))
root.geometry("{}x{}+{}+{}".format(w, h, x_cordinate, y_cordinate))

# Membuat panel biru
blue_panel = tk.Frame(root, width=300, height=520, bg="#29AAE2")
blue_panel.pack(side="left")
blue_panel.bind('<Button-1>', on_panel_clicked)

def show_aboutpage():
        # Membuat instance dari MainClass
    AboutUs(root)

# Membuat panel dengan latar belakang biru sebagai tempat menampilkan tombol
button_pannel = tk.Frame(blue_panel, bg="red", width=156, height=35)
button_pannel.place(x=5, y=5)

# Memuat gambar
image = Image.open("images/computest_white_resized.png")
photo = ImageTk.PhotoImage(image)

# Membuat tombol dengan gambar
label_button = tk.Button(blue_panel, relief=tk.FLAT, bg="#29AAE2", cursor='hand2',
                         image=photo, width=156, height=35, command=show_aboutpage)
label_button.image = photo  # Memastikan gambar tetap terlihat
label_button.place(x=5, y=5)


label_button.update()
w = label_button.winfo_width()
h = label_button.winfo_height()

print(w,h)

# Membuka gambar menggunakan PIL
image = Image.open("images/banner_resized.png")

# Membuat objek PhotoImage dari gambar
photo = ImageTk.PhotoImage(image)

# Membuat label dengan gambar
label = tk.Label(blue_panel, image=photo, bd=0)
label.place(x=0, y=220)

# Membuat panel utama
main_panel = tk.Frame(root, bg="white")
main_panel.pack(fill="both", expand=True)
main_panel.bind('<Button-1>', on_panel_clicked)

# Membuat form login
login_form = LoginForm(root, blue_panel, main_panel)

root.mainloop()
