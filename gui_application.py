import tkinter
import numpy as np
from tkinter import filedialog
from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk
from openpyxl.workbook.workbook import Workbook
import pandas as pd
from openpyxl import load_workbook
from extractimageframe import extractimageframe
from thread_checkattendance import *
# from thread_processing_photoset import main_processing_photoset
import time
from loadresult import loadresult
from thread_processing_photoset import *


root = tkinter.Tk()
big_frame = ttk.Frame(root)
big_frame.pack(fill='both', expand=True)

b = ttk.Label(big_frame, text="", width=100, borderwidth=10)
b.pack()
describe = ttk.Label(
    big_frame, text="PROJECT: COMBINING VIDEO CLASS SOLUTION WITH FACE RECOGNITION SOLUTION", width=100, borderwidth=5)
describe.pack()
student = ttk.Label(
    big_frame, text="STUDENT: HOANG THI THU - 207239", width=100, borderwidth=5)
student.pack()
subject = ttk.Label(
    big_frame, text="SUBJECT: ADVANCED PROJECR FOR AI",  width=100, borderwidth=5)
subject.pack()
a = ttk.Label(big_frame, text="", width=100, borderwidth=10)
a.pack()

logo = Image.open(
    '/workspace/AdvanceProjectforAIConvergence/coding/python/logo.png')
logo = ImageTk.PhotoImage(logo)
logo_label = ttk.Label(image=logo)
logo_label.pack()


def show_progressbar(x_window):
    my_progress = ttk.Progressbar(
        x_window, orient=HORIZONTAL, length=400, mode='determinate')
    my_progress.pack(pady=20)


def close_app(window):
    window.destroy


def openfile():
    filename = filedialog.askopenfilename()
    return filename


def browse_button():
    filename = filedialog.askdirectory()
    print(filename)
    return filename


def load_excel(excel_path):
    try:
        df = pd.read_excel(excel_path)
    except ValueError:
        ttk.messagebox.showerror("Information", "The file is invalid")
        return None
    except FileNotFoundError:
        ttk.messagebox.showerror(
            "Information", f'No such file as {excel_path}')

    return df


def open_root_close_win(root, wd):
    wd.destroy()
    root.update()
    root.deiconify()


def PROCESSING_DATA(root):
    root.withdraw()
    wd = tkinter.Tk()
    wd.title("PROCESSING DATA STAGE")
    wd.geometry("800x500")

    button_photoset = ttk.Button(
        wd, text="PROCESSING IMAGES SET", command=lambda: processing_photoset(wd))
    button_photoset.pack()

    button_recoredvideo = ttk.Button(
        wd, text="PROCESSING RECORDED VIDEO", command=lambda: processing_recordedvideo(wd))
    button_recoredvideo.pack()

    button_finish = ttk.Button(
        wd, text="FINISH", command=lambda: open_root_close_win(root, wd))
    button_finish.pack()

    style_one = ttk.Style(wd)
    style_one.theme_use('clam')
    style_one.configure('TButton', background='grey', foreground='white',
                        width=50, height=50, borderwidth=5, focusthickness=5, focuscolor='Black')
    style_one.map('TButton', background=[('active', 'brown')])


def processing_photoset(wd):
    filename = browse_button()
    pikle_datafile = main_processing_photoset(photoset_path=filename, n_thread=5)
    if pikle_datafile is not None:
        ttk.Label(wd, text="IMAGES SET IS PROCESSED",
                  width=100, borderwidth=10).pack()
        ttk.Label(wd, text="PROCESSED PHOTOSET FILE: {}".format(
            pikle_datafile), width=100, borderwidth=10).pack()


def processing_recordedvideo(wd):

    filename = openfile()
    img_frames_path, num_img_frames = extractimageframe(recorded_path=filename)
    if img_frames_path is not None:
        ttk.Label(wd, text="RECORDED VIDEO IS PROCESSED",
                  width=100, borderwidth=10).pack()
        ttk.Label(wd, text="IMAGE FRAMES FILE: {}".format(
            img_frames_path), width=100, borderwidth=10).pack()

    if num_img_frames is not None:
        ttk.Label(wd, text="NUMBER OF IMAGE FRAMES: {}".format(
            num_img_frames), width=100, borderwidth=10).pack()


def CHECK_ATTENDANCE(root):
    root.withdraw()
    wd = tkinter.Tk()
    wd.title("CHECK ATTENDANCE STAGE")
    wd.geometry("1000x500")

    facial_feature_path = None
    img_frames_dir = None

    def choose_PPF():
        global facial_feature_path
        facial_feature_path = openfile()
        if facial_feature_path is not None:
            ttk.Label(wd, text="PROCESSED PHOTOSET FILE: {}".format(
            facial_feature_path), width=100, borderwidth=10).pack()

    def choose_EIFF():
        global img_frames_dir
        img_frames_dir = browse_button()
        if img_frames_dir is not None:
            ttk.Label(wd, text="CHOOSE EXTRACTED IMAGE FRAMES FOLDER: {}".format(img_frames_dir), width=100, borderwidth=10).pack()

    def run_main():
        global facial_feature_path, img_frames_dir
        result_path = main(facial_feature_path, img_frames_dir, n_thread=5)
        if result_path is not None:
            ttk.Label(wd, text=" FINISH - CHECK ATTENDANCE", width=100, borderwidth=10).pack()
            ttk.Label(wd, text="RESULT FILE: {}".format(result_path), width=100, borderwidth=10).pack()

    button_datapath = ttk.Button(
        wd, text="CHOOSE PROCESSED PHOTOSET FILE", command=lambda: choose_PPF())
    button_datapath.pack()

    button_frames_dir = ttk.Button(
        wd, text="CHOOSE EXTRACTED IMAGE FRAMES FOLDER", command=lambda: choose_EIFF())
    button_frames_dir.pack()

    button_check = ttk.Button(
        wd, text="CHECK ATTENDANCE", command=lambda: run_main())
    button_check.pack()

    button_finish = ttk.Button(
        wd, text="FINISH", command=lambda: open_root_close_win(root, wd))
    button_finish.pack()

    style_two = ttk.Style(wd)
    style_two.theme_use('classic')
    style_two.configure('TButton', background='grey', foreground='white',
                        width=50, height=50, borderwidth=5, focusthickness=5, focuscolor='Black')
    style_two.map('TButton', background=[('active', 'brown')])


def LOAD_RESULT(root):
    root.withdraw()
    wd = tkinter.Tk()
    wd.title("LOAD FINAL RESULT")
    wd.geometry("800x500")

    button_choose = ttk.Button(
        wd, text="ANALYSIS AUTHENTICATION RESULT FILE", command=lambda: loadresult_tkinter(wd))
    button_choose.pack()

    button_show = ttk.Button(
        wd, text="SHOW FINAL RESULT", command=lambda: show_final_result())
    button_show.pack()

    button_finish = ttk.Button(
        wd, text="FINISH", command=lambda: open_root_close_win(root, wd))
    button_finish.pack()

    style_one = ttk.Style(wd)
    style_one.theme_use('clam')
    style_one.configure('TButton', background='grey', foreground='white',
                        width=50, height=50, borderwidth=5, focusthickness=5, focuscolor='Black')
    style_one.map('TButton', background=[('active', 'brown')])



def loadresult_tkinter(wd):
    result_file = openfile()
    loadresult(result_file)
    ttk.Label(wd, text="AUTHENTICATION RESULT FILE IS ANALYSISED", width=100, borderwidth=10).pack()

def show_final_result():
    headings_list = []

    final_result = openfile()
    df = pd.read_excel(final_result)
    resultWindow = tkinter.Tk()
    resultWindow.title("FINAL AUTHENTICATION RESULT")
    resultWindow.geometry("1000x500")

    headings = df.columns

    # import mipkit;mipkit.set_trace();exit();
    data = list(headings.values.tolist())
    rows = len(df)


    tv = ttk.Treeview(resultWindow, columns=data, show=["headings"], selectmode="browse")

    for heading in headings:
        heading = str(heading)
        tv.column(heading, width=200, anchor='center')
        tv.heading(heading, text= heading)

    for rownumber in range(rows):
        rowvalue = df.values[rownumber]             # Get row data
        rowvalue = np.array2string(rowvalue)        # Convert from an np array to string
        rowvalue = rowvalue.strip("[]")             # Strip the string of square brackets
        rowvalue = rowvalue.replace("'",'')         # Replace all instances of ' with no character
        tv.insert('', 'end', values= rowvalue)

    tv.pack()

    result_close = ttk.Button(resultWindow, text="CLOSE", command=resultWindow.destroy)
    result_close.pack()


button_one = ttk.Button(big_frame, text="PROCESSING DATA",
                        command=lambda: PROCESSING_DATA(root))
button_one.pack()

button_two = ttk.Button(big_frame, text="CHECK STUDENT'S ATTENDANCE",
                        command=lambda: CHECK_ATTENDANCE(root))
button_two.pack()

button_three = ttk.Button(big_frame, text="LOAD RESULT",
                          command=lambda: LOAD_RESULT(root))
button_three.pack()

button_four = ttk.Button(
    big_frame, text="CLOSE APPLICATION", command=root.destroy)
button_four.pack()

style = ttk.Style()
style.theme_use('alt')
style.configure('TButton', background='grey', foreground='white',
                width=50, borderwidth=5, focusthickness=5, focuscolor='Black')
style.map('TButton', background=[('active', 'brown')])


root.title("SMART ATTENDANCE SYSTEM")
root.geometry('800x500')
root.minsize(250, 100)
root.mainloop()
