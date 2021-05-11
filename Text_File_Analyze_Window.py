import string
import pandas as pd
import pickle

from pathlib import Path
from PyQt5.QtWidgets import QFileDialog, QVBoxLayout, QWidget, QLabel, QPushButton
from PyQt5.QtCore import Qt, QSize
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize, RegexpTokenizer
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer

class Text_File_Analyze_Window(QWidget):
    def select_file(self):
        global filename
        file_name = QFileDialog()
        file_name.setFileMode(QFileDialog.ExistingFiles)
        filename = file_name.getOpenFileNames(self, "Open files", "C:/Users/Anup/Desktop/speech_to_text")
        no_of_files = len(filename[0])
        filename = filename[0]
        self.selected_files_Label.setText(str(no_of_files)+" files are selected")
        index = 0
        while no_of_files != 0:
            index = index + 1
            no_of_files = no_of_files - 1
        return filename

    def Analyze_multiple_files(self):
        index = 0
        no_of_files = len(filename)
        while no_of_files != 0:
            self.nltk_file_Audio(filename[index])
            index = index + 1
            no_of_files = no_of_files - 1
    
    def nltk_file_Audio(self, AUDIO_FILE):
        print("\nfile_name : " + Path(AUDIO_FILE).stem)
        text = open(AUDIO_FILE, encoding='utf-8').read()
        lower_case = text.lower()
        cleaned_text = lower_case.translate(str.maketrans('', '', string.punctuation))

        # Using word_tokenize because it's faster than split()
        tokenized_words = word_tokenize(cleaned_text, "english")

        # Removing Stop Words
        final_words = []
        for word in tokenized_words:
            if word not in stopwords.words('english'):
                final_words.append(word)

        # Lemmatization - From plural to single + Base form of a word (example better-> good)
        lemma_words = []
        for word in final_words:
            word = WordNetLemmatizer().lemmatize(word)
            lemma_words.append(word)

        keywords = open("keywords.txt", encoding='utf-8').read()
        keywords = keywords.lower()
        keywords = list(keywords.split("\n"))
        
        list3 = set(lemma_words)&set(keywords)
        list4 = sorted(list3, key = lambda k : lemma_words.index(k))
        print("Antinational Word Count : "+str(len(list4)))

        self.sentiment_analyse(cleaned_text)
        self.classify(text)
        self.status_Label.setText("Analyze Completed!!!")

    def sentiment_analyse(self, sentiment_text):
        score = SentimentIntensityAnalyzer().polarity_scores(sentiment_text)
        if score['neg'] > score['pos']:
            print("Sentiment : Negative Sentiment")
        elif score['neg'] < score['pos']:
            print("Sentiment : Positive Sentiment")
        else:
            print("Sentiment : Neutral Sentiment")

    def classify(self, text):
        data = pd.read_csv("new_train.csv")
        data_df = pd.DataFrame(data, columns=['id', 'comment_text', 'threat'])
        X_train = data_df['comment_text'].to_list()
        tokenizer = RegexpTokenizer(r"\w+")
        en_stopwords = set(stopwords.words('english'))
        ps = PorterStemmer()

        def getCleanedText(text):
            text = text.lower()

            tokens = tokenizer.tokenize(text)
            new_tokens = [token for token in tokens if token not in en_stopwords]

            stemmed_tokens = [ps.stem(tokens) for tokens in new_tokens]
            clean_text = " ".join(stemmed_tokens)

            return clean_text

        X_test = text
        X_clean = [getCleanedText(i) for i in X_train]
        Xt_clean = [getCleanedText(X_test)]

        cv = TfidfVectorizer(ngram_range=(1, 2))
        x_vec = cv.fit_transform(X_clean).toarray()
        xt_vec = cv.transform(Xt_clean).toarray()

        from sklearn.linear_model import LogisticRegression
        # model = LogisticRegression().fit(x_vec, Y_train)
        filename = "logistic.sav"
        # pickle.dump(model, open(filename, 'wb'))
        loaded_model = pickle.load(open(filename, 'rb'))
        y_pred = loaded_model.predict(xt_vec)
        if (y_pred[0] == 1):
            print("Threatful Text")
        else:
            print("Not Threatful Text")

    def Select_TextFile_ButtonClicked(self):
        self.selected_files_Label.setText("")
        self.status_Label.setText("")
        self.select_file()

    def AnalyzeButtonClicked(self):
        self.Analyze_multiple_files()

    def ResultButtonClicked(self):
        print("ResultButtonClicked")

    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        self.verticalLayout = QVBoxLayout(self)
        
        self.Select_TextFile_Button = QPushButton()
        self.Select_TextFile_Button.setMinimumSize(QSize(200, 40))
        self.Select_TextFile_Button.setStyleSheet("font: 75 16pt \"Times New Roman\";")
        self.verticalLayout.addWidget(self.Select_TextFile_Button, 0, Qt.AlignHCenter)
        self.Select_TextFile_Button.setText("Select Text File")

        #listener
        self.Select_TextFile_Button.clicked.connect(lambda: self.Select_TextFile_ButtonClicked())

        self.selected_files_Label = QLabel()
        self.selected_files_Label.setStyleSheet("font: italic 14pt \"Times New Roman\";")
        self.verticalLayout.addWidget(self.selected_files_Label, 0, Qt.AlignHCenter)
        self.selected_files_Label.setText("")

        self.AnalyzeButton = QPushButton()
        self.AnalyzeButton.setMinimumSize(QSize(200, 40))
        self.AnalyzeButton.setStyleSheet("font: 75 16pt \"Times New Roman\";")
        self.verticalLayout.addWidget(self.AnalyzeButton, 0, Qt.AlignHCenter)
        self.AnalyzeButton.setText("Analyze")
        
        #listener
        self.AnalyzeButton.clicked.connect(lambda: self.AnalyzeButtonClicked())

        self.status_Label = QLabel()
        self.status_Label.setStyleSheet("font: 14pt \"Times New Roman\";")
        self.verticalLayout.addWidget(self.status_Label, 0, Qt.AlignHCenter)
        self.status_Label.setText("")

        self.ResultButton = QPushButton()
        self.ResultButton.setMinimumSize(QSize(200, 35))
        self.ResultButton.setStyleSheet("font: 75 16pt \"Times New Roman\";")
        self.verticalLayout.addWidget(self.ResultButton, 0, Qt.AlignRight)
        self.ResultButton.setText("Result")
        
        #listener
        self.ResultButton.clicked.connect(lambda: self.ResultButtonClicked())