from tkinter import *
from tkinter import ttk, filedialog
import speech_recognition as sr
from os import path

def select_file():
    global filename
    filename = filedialog.askopenfilenames(initialdir=".")
    no_of_files = len(filename)
    file_path.config(text=(str(no_of_files)+" files are selected"))
    index = 0
    while no_of_files != 0:
        print(filename[index])
        index = index + 1
        no_of_files = no_of_files - 1
    return filename

def Recognize_multiple_files():
    index = 0
    no_of_files = len(filename)
    while no_of_files != 0:
        Recognize_file_Audio(filename[index])
        index = index + 1
        no_of_files = no_of_files - 1

def Recognize_file_Audio(AUDIO_FILE):
    r = sr.Recognizer()
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source, duration=5)
        try:
            print("Google Speech Recognition thinks you said: " + r.recognize_google(audio))
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
        num = len(AUDIO_FILE)
        ind = num - 1
        filename1 = ""
        while AUDIO_FILE[ind] != '.':
            ind = ind - 1
        ind = ind - 1
        while AUDIO_FILE[ind] != '/':
            filename1 = AUDIO_FILE[ind] + filename1
            ind = ind - 1
        filename1 = filename1 + ".txt"
        print(filename1)
        text_file = open(filename1, "w")
        text_file.write("%s" % r.recognize_google(audio))
        label3.config(text="Recognize Completed!!!")
        text_file.close()

root = Tk()
root.title("Recognition System")
root.geometry("500x300")

fm = Frame(root)

header = Label(fm, text="Select Recognitions file!", font=("Helvetica", 18, 'bold'))
header.pack(side=TOP, expand=YES)

btn1 = Button(fm, text='Add file', command=select_file, font=("Helvetica", 14))
btn1.pack(side=TOP, expand=YES)

file_path = ttk.Label(fm, text="None of file selected!", font=("Helvetica", 12, 'italic'))
file_path.pack(side=TOP, expand=YES)

btn2 = Button(fm, text='Recognize', command=Recognize_multiple_files, font=("Helvetica", 14))
btn2.pack(side=TOP, expand=YES)

label3 = ttk.Label(fm, text="", font=("Helvetica", 20, 'bold'))
label3.pack(side=TOP, expand=YES)

fm.pack(fill=BOTH, expand=YES)

root.mainloop()