import tkinter as tk
import numpy as np
import cv2
from keras_facenet import FaceNet
from keras.models import load_model
from PIL import Image, ImageTk
from tensorflow.keras.preprocessing import image
import pickle
from scipy.spatial.distance import cosine
import time
import datetime
from exam_coiche import Exam
from tkinter import messagebox

class LiveCam(tk.Tk):
    def __init__(self, root, main_panel, nama):
        self.root = root
        self.main_panel = main_panel
        self.user = nama
        self.create_widgets()
        self.load_data(self.user)
        self.show_live_cam()
        self.show_exam()

    def show_exam(self):
        self.exam_coiche = Exam(self.root, self.main_panel, self.user)

        
    def create_widgets(self):
        # atur ukuran layar
        screen_height = self.main_panel.winfo_screenheight()
        # membuat frame untuk menampilkan video
        width=480
        height=320
        self.camera_canvas = tk.Canvas(self.main_panel, width=width, height=height, bg="white")
        
        self.camera_canvas.place(x=20, y=screen_height-height-20, width=width, height=height)

        loading_cam_label = tk.Label(self.camera_canvas, text="Memuat kamera . . .", font=("Arial", 12), bg="white", fg="black")
        loading_cam_label.pack(pady=150)

        self.camera_canvas.update()  # Memperbarui tampilan canvas

        loading_cam_label.pack_forget()

        # Membuat objek kamera
        self.camera = cv2.VideoCapture(0)

    def show_live_cam(self):
        ret, frame_cv2 = self.camera.read()
        if ret:
            frame_cv2 = cv2.flip(frame_cv2, 1) # melakukan flip secara horizontal
            frame_cv2 = cv2.resize(frame_cv2, (480, 320))
            frame_cv2 = cv2.cvtColor(frame_cv2, cv2.COLOR_BGR2RGB)

            # Extract embedding from frame
            embedding = self.get_embedding_live(frame_cv2, self.model)
            st = time.time()
            pred = self.get_anti_spoofing(frame_cv2, self.model_anti_spoofing)
            et = time.time()

            elapsed_time = et - st
            print('Execution time spoffing:', elapsed_time, 'seconds')
            print('nama terdaftar:', self.user)

            # Check if embedding is None
            if embedding is None:
                self.label_text = "Tidak Terdeteksi"
            else:
                # Perform face recognition
                self.label_text, label_data1, score1 = self.is_match(embedding, self.label_dict)
                # Mengubah nilai teks pada objek tk.StringVar

            
            self.label_text_var = tk.StringVar()
            self.label_text_var.set(self.label_text)
            self.label_text_var_value = self.label_text_var.get()
            print('update: ', self.label_text_var_value)

            if self.label_text_var.get() != self.user:
                message = "Anda terdeteksi melakukan kecurangan.\nPastikan wajah anda terekam asli dan jelas di kamera."
                messagebox.showwarning("Peringatan", message)

            if pred is None:
                label_pred_text = "Tidak Terdeteksi"
            else:
                label_id = pred[0].tolist()
                label_class= label_id.index(max(label_id))
                print(label_class)
                if label_class==1:
                    label_pred_text = 'spoof'
                else:
                    label_pred_text = 'real'
            
            self.label_pred = tk.StringVar()
            self.label_pred.set(label_pred_text)
            label_pred_value = self.label_pred.get()
            print('update: ', label_pred_value)

            if self.label_pred.get() != "real":
                message = "Anda terdeteksi melakukan kecurangan.\nPastikan wajah anda terekam asli dan jelas di kamera."
                messagebox.showwarning("Peringatan", message)


            # Draw label on frame with red color
            cv2.putText(frame_cv2, self.label_text, (10, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 255), 2)
            cv2.putText(frame_cv2, label_pred_text, (10, 310), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 255), 2)

            # Konversi frame OpenCV menjadi objek gambar PIL
            image = Image.fromarray(frame_cv2)

            # Konversi gambar PIL menjadi format yang dapat ditampilkan di Tkinter
            photo = ImageTk.PhotoImage(image)

            # Menampilkan gambar di canvas
            self.camera_canvas.create_image(0, 0, anchor="nw", image=photo)
            self.camera_canvas.image = photo

        self.main_panel.after(10, self.show_live_cam)

    def load_data(self, user):
        # load model
        self.model_anti_spoofing = load_model('models/model_antispoof.h5')

        # Memuat file label_dict.pickle
        with open('database/'+user+'/model/label_'+user+'.pickle', 'rb') as handle:
            self.label_dict = pickle.load(handle)

        # Load FaceNet model
        self.model = FaceNet()

        # load cascade classifier for face detection
        self.face_cascade = cv2.CascadeClassifier('models/haarcascade_frontalface_default.xml')

    def get_anti_spoofing(self, frame, model):
        # Deteksi wajah menggunakan Haar Cascade Classifier
        faces = self.face_cascade.detectMultiScale(frame, 1.1, 4)
        # Jika tidak ada wajah yang terdeteksi, kembalikan None
        # If no face is detected, return None
        if len(faces)>0:
            x1, y1, width, height = faces[0]
        else:
            return None

        # Extract face region
        x1, y1 = abs(x1), abs(y1)
        x2, y2 = x1 + width, y1 + height
        face = frame[y1:y2, x1:x2]
        
        # Konversi wajah menjadi array numpy
        img = image.array_to_img(face, scale=False)
        img = img.resize((323, 323))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)

        # Preprocessing gambar
        x /= 255.0

        # Prediksi kelas gambar
        pred = model.predict(x)

        return pred

    # Define a function to extract embeddings from a frame
    def get_embedding_live(self, frame, model):
        # Detect faces
        wajah = self.face_cascade.detectMultiScale(frame, 1.1, 4)

        # If no face is detected, return None
        if len(wajah)>0:
            x1, y1, width, height = wajah[0]
        else:
            return None

        # Extract face region
        x1, y1 = abs(x1), abs(y1)
        x2, y2 = x1 + width, y1 + height
        face = frame[y1:y2, x1:x2]

        # Convert face to RGB format
        face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)

        # Resize face to (160, 160)
        face = cv2.resize(face, (323, 323))

        # Convert face to tensor
        face = face.astype(np.float32)
        face = np.expand_dims(face, axis=0)

        # Embed face using model
        embedding = model.embeddings(face)[0, :]

        return embedding

    def is_match(self, known_embedding, label_dict=None, threshold=0.4):
        if label_dict is None:
            label_dict = self.label_dict
        label_match = []
        score_match = []
        
        label_true = []
        score_true = []

        for label, embeddings_list in label_dict.items():
            for i, embedding in enumerate(embeddings_list):
                if len(embedding) == 0:
                    continue
                    
                scores = cosine(known_embedding, embedding)
                label_match.append(label)
                score_match.append(scores)

        if score_match:
            min_index = np.argmin(score_match)
            label = label_match[min_index]
            score = score_match[min_index]
            if score <= threshold:
                label_data = label
                label_true.append(label)
                score_true.append(score)
            else:
                label_data = 'Tidak Terdaftar'
        else:
            label_data = 'Tidak terdeteksi'

        return label_data, label, score

'''root = tk.Tk()
main_panel = tk.Frame(root, width=950, height=550, bg="white")
main_panel.pack(expand=True, fill=tk.BOTH)

nama = "zain arif"
live_cam = LiveCam(root, main_panel, nama)

root.mainloop()'''