import re
import numpy as np
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class SemanticSimilarity:
    def __init__(self):
        self.vectorizer = CountVectorizer()

    def case_folding(self, text):
        text = text.lower()
        text = re.sub(r'https?://\S+|www\.\S+', ' ', text)
        text = re.sub(r'[-+]?[0-9]+', ' ', text)
        text = re.sub(r'[^\w\s]', ' ', text)
        text = text.strip()
        return text

    def tokenization(self, text):
        return word_tokenize(text)

    def stemming(self, word):
        factory = StemmerFactory()
        stemmer = factory.create_stemmer()
        return stemmer.stem(word)

    def remove_stopwords(self, tokens):
        stopword_list = set(stopwords.words('indonesian'))
        return [token for token in tokens if token not in stopword_list]

    def calculate_word_similarity_matrix(self, docs):
        word_vectors = self.vectorizer.fit_transform(docs).toarray()
        word_similarity_matrix = cosine_similarity(word_vectors)
        return word_similarity_matrix

    def calculate_similarity_score(self, sentence1, sentence2):
        sentence1 = self.case_folding(sentence1)
        sentence2 = self.case_folding(sentence2)

        tokens1 = self.tokenization(sentence1)
        tokens2 = self.tokenization(sentence2)

        stemmed_tokens1 = [self.stemming(token) for token in tokens1]
        stemmed_tokens2 = [self.stemming(token) for token in tokens2]

        tokens1 = self.remove_stopwords(stemmed_tokens1)
        tokens2 = self.remove_stopwords(stemmed_tokens2)

        processed_sentence1 = ' '.join(tokens1)
        processed_sentence2 = ' '.join(tokens2)

        docs = [processed_sentence1, processed_sentence2]
        M = self.calculate_word_similarity_matrix(docs)

        similarity_score = M[0][1]  # Assuming similarity score is the value at position (0, 1) in the matrix
        return similarity_score


'''true_sentences = [
    "algoritma adalah upaya dengan urutan operasi yang disusun secara logis dan sistematis untuk menyelesaikan suatu masalah untuk menghasilkan suatu output tertentu",
    "instruksi yang ditujukan ke komputer agar dirinya bisa menyelesaikan tugas yang diberikan",
    "algoritma merupakan urutan dari sejumlah langkah logis dan sistematis untuk memecahkan suatu masalah tertentu"
]

jawaban = ["algoritma merupakan urutan dari sejumlah langkah logis dan sistematis untuk memecahkan suatu masalah tertentu",
    "langkah langkah yang logis untuk menyelesaikan masalah secara sistematis",
    "Algoritma adalah urutan langkah-langkah logis penyelesaian masalah yang disusun secara sistematis dan logis.",
    "Algoritma adalah suatu urutan dari beberapa langkah yang logis guna menyelesaikan masalah",
    "Algoritma adalah langkah-langkah yang disusun secara tertulis dan berurutan untuk menyelesaikan suatu masalah",
    "Algoritma adalah langkah-langkah menyelesaikan masalah secara sistematis dan logis",
    "algoritma adalah langkah langkah yang disusun secara tertulis dan berurutan untuk menyelesaikan suatu masalah",
    "algortima merupakan suatu urutan langkah langkah untuk menyelesaikan suatu masalah dalam bentuk yang logis",
    "urutan perintah agar komputer bisa melakukan tugasnya",
    "Serangkaian tindakan acak yang diatur untuk menyelesaikan masalah dan menghasilkan output yang tidak pasti.",
    "Petunjuk yang diberikan kepada komputer untuk melakukan tugas tanpa tujuan atau hasil yang jelas.",
    "Petunjuk yang diberikan kepada komputer untuk mengeksekusi tugas-tugas secara acak.",
    "Serangkaian langkah terstruktur dan logis yang diatur untuk menyelesaikan suatu masalah dengan tujuan menghasilkan output yang spesifik.",
    "Instruksi yang ditujukan kepada komputer untuk menyelesaikan tugas yang telah ditetapkan dengan menggunakan urutan operasi yang sistematis.",
    "Rangkaian langkah-langkah logis dan terstruktur yang digunakan untuk memecahkan masalah tertentu.",
    "Suatu urutan operasi yang disusun secara sistematis dan logis untuk mencapai solusi dari suatu masalah.",
    "proses komputer dalam melakukan perhitungan untuk memecahkan masalah",
    "perintah yang dapat dimengerti oleh komputer",
    "susunan perintah yang digunakan untuk memecahkan sebuah atau beberapa masalah",
    "logika yang disusun secara sistematis untuk tujuan tertentu",
    "Instruksi yang diberikan kepada komputer agar dapat menyelesaikan tugas yang telah ditugaskan dengan menggunakan pendekatan langkah-langkah terurut dan logis.",
    "Sejumlah langkah logis dan terstruktur yang diatur secara sistematis untuk memecahkan suatu masalah dengan hasil output yang diinginkan.",
    "Rencana operasi yang disusun secara logis dan sistematis untuk menangani masalah dengan mencapai suatu output yang spesifik.",
    "Petunjuk yang tidak teratur diberikan kepada komputer untuk menyelesaikan tugas tanpa hasil yang pasti.",
    "Rencana langkah-langkah acak yang diatur secara tidak terstruktur untuk mencapai solusi yang tidak jelas.",
    "Urutan tindakan yang acak untuk mencapai hasil yang tidak jelas dalam penyelesaian masalah.",
    "algoritma merupakan instruksi yang disusun secara sistematis untuk bisa menyelesaikan tugas",
    "algoritma adalah perhitungan yang bertujuan mendapatkan hasil yang diinginkan",
    "algoritma adalah pemanfaatan komputer dengan cara memberi perintah yang logis",
    "cara kerja komputer dalam menyelesaikan tugasnya",
    "Rencana langkah-langkah acak yang diatur secara tidak terstruktur untuk menghasilkan solusi yang tidak jelas.",
    "Urutan operasi yang diorganisir secara sistematis dan logis untuk mencapai solusi dari suatu masalah."
]

nilai = []
calculator = SemanticSimilarity()
for j in range(len(jawaban)):
    scores = []
    for i in range(len(true_sentences)):
        similarity_score = calculator.calculate_similarity_score(true_sentences[i], jawaban[j])
        scores.append(similarity_score)
    hs = max(scores)
    print("hs jawaban[{}]: {}".format(j, hs))
    nilai.append(hs)

rounded_scores = [round(score, 2) for score in nilai]

print('nilai: ', rounded_scores)

true_scores = [10, 10, 10, 10, 9, 10, 9, 9, 9, 8, 8, 7, 8, 7, 10, 10, 8, 7, 9, 7, 10, 10, 9, 8, 7, 7, 10, 7, 8, 7, 7, 8]
true_scores_normalized = [(score - min(true_scores)) / (max(true_scores) - min(true_scores)) for score in true_scores]

print('nilai asli: ', true_scores_normalized)

# Menghitung MAE
mae = np.mean(np.abs(np.array(rounded_scores) - np.array(true_scores_normalized)))

print(f"Mean Absolute Error (MAE): {mae}")'''
