from operator import mod
import os
import random
import pandas as pd
from PIL import Image
from numpy import asarray, expand_dims
import matplotlib.pyplot as plt
from keras.models import load_model
import cv2
from keras_facenet import FaceNet
from scipy.spatial.distance import cosine
import pickle
import numpy as np
from tensorflow.keras.preprocessing import image

def modelling(user):
    # Dataset
    user = user.lower()
    root_dir = 'database'
    path = os.path.join(root_dir, user)

    dataset_path = os.path.join(root_dir, user, 'image')
    model_path = os.path.join(root_dir, user, 'model')

    names = []
    nums = []
    data = {'Name of class': [], 'Number of samples': []}

    for i, class_dir in enumerate(os.listdir(path)):
        if os.path.isdir(os.path.join(path, class_dir)):
            image_dir = os.path.join(path, class_dir)
            nums.append(len(os.listdir(image_dir)))
            names.append(class_dir)

    data['Name of class'] += names
    data['Number of samples'] += nums

    df = pd.DataFrame(data)
    print(df)

    '''# Mendapatkan path gambar di dalam class "Andhar"
    class_dir = os.path.join(root_dir, user)
    image_dir = os.path.join(class_dir, 'image')
    image_files = [file for file in os.listdir(image_dir) if file.endswith('.jpg') or file.endswith('.jpeg') or file.endswith('.png')]

    # Memilih secara acak 5 gambar
    selected_images = random.sample(image_files, 5)

    # Menampilkan gambar secara acak
    plt.figure(figsize=(10, 10))
    for i, image_file in enumerate(selected_images):
        image_path = os.path.join(image_dir, image_file)
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        plt.subplot(1, 5, i+1)
        plt.imshow(image)
        plt.axis('off')

    plt.show()'''

    # get list of image file paths and labels
    image_paths = []
    labels = []

    # Mendapatkan path gambar di dalam kelas "Andhar"
    class_dir = os.path.join(root_dir, user)
    image_dir = os.path.join(class_dir, 'image')
    for subdir, dirs, files in os.walk(image_dir):
        for file in files:
            if file.endswith('.jpg') or file.endswith('.jpeg') or file.endswith('.png'):
                image_path = os.path.join(subdir, file)
                image_paths.append(image_path)
                labels.append(user)

    # Load FaceNet model
    model_facenet = FaceNet()

    # load cascade classifier for face detection
    face_cascade = cv2.CascadeClassifier('models/haarcascade_frontalface_default.xml')

    # Define a function to extract embeddings from an image
    def get_embedding(img_path):
        # Read image
        img = cv2.imread(img_path)
        
        # Detect faces
        wajah = face_cascade.detectMultiScale(img, 1.1, 4)

        # If no face is detected, skip to next image
        if len(wajah) == 0:
            return None

        # Extract face region
        x1, y1, width, height = wajah[0]
        x1, y1 = abs(x1), abs(y1)
        x2, y2 = x1 + width, y1 + height
        img = img[y1:y2, x1:x2]
        
        # Convert image to RGB format
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Resize image to (160, 160)
        img = cv2.resize(img, (224, 224))
        
        # Convert image to tensor
        img = img.astype(np.float32)
        img = np.expand_dims(img, axis=0)
        
        # Embed face using model
        embedding = model_facenet.embeddings(img)[0, :]
        
        return embedding

    # Iterate through all images in image_paths
    embeddings = []
    for img_path in image_paths:
        # Extract embedding from image and append to list
        embedding = get_embedding(img_path)
        
        # Check if embedding is None
        if embedding is None:
            continue
            
        embeddings.append(embedding)

    label_dict = {}
    for label, embedding in zip(labels, embeddings):
        if label not in label_dict:
            label_dict[label] = []
        label_dict[label].append(embedding)

    # Membuat direktori 'model' jika belum ada
    model_dir = os.path.join(root_dir, user, 'model')
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)

    # Menyimpan label_dict ke file pickle di direktori 'model'
    label_file = os.path.join(model_dir, 'label_' + user + '.pickle')
    with open(label_file, 'wb') as handle:
        pickle.dump(label_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

    return dataset_path, model_path
