import warnings
warnings.filterwarnings('ignore')
import argparse
import cv2
import sys
import numpy as np
import insightface
from insightface.app import FaceAnalysis
from insightface.data import get_image as ins_get_image

assert insightface.__version__>='0.3'
import matplotlib.pyplot as plt
from PIL import Image
import glob
import os
from os.path import join
from tqdm import tqdm
import pandas as pd
import sys
import pickle as pkl
import threading
import xlsxwriter
from pandas import ExcelWriter
import time
from queue import Queue


def compare_sim(frame, facial_feature_path, q, app):

    with open(facial_feature_path, 'rb') as f:
        facial_feature_data = pkl.load(f)
    
    data = {'FRAME' :[],
            'STUDENT_NAME': [], 
            'FACE': [], 
            'AUTHENTICATION_RESULT': [], 
            'SIMILARITY_INFORMATION': []}

    student_success_list = []
    student_name_list = []

    df_frame = pd.DataFrame(data)

    img_frame = plt.imread(frame)
    face_frame = app.get(img_frame)

    frame_name = (frame.split('/')[-1]).split('.')[0]
  

    if len(face_frame) != 0:
        for f in range(len(face_frame)):
            feature_frame = face_frame[f].normed_embedding

            for i in range(len(facial_feature_data)): #Each Student
                student_name = facial_feature_data[i][0]['student_name']
                student_name_list.append(student_name)

                sim_list = [] #List sim of face i in frame with all photo of one student

                for n in range(len(facial_feature_data[i])):    #Each Photo
                    
                    
                    facial_feature_photo = facial_feature_data[i][n]['facial_feature'] 
                    sim = np.dot(facial_feature_photo, feature_frame)
                    sim_list.append(sim) #similarity of each face in frame and photo

                max_sim = np.max(sim_list)
                avg_sim = np.mean(sim_list)


                if max_sim >= 0.45 and avg_sim >= 0.40:
                    result = 'SUCCESS'
                    student_success_list.append(student_name)

                    result_frame = {'FRAME' : frame_name,
                                    'STUDENT_NAME': student_name, 
                                    'FACE': f, 
                                    'AUTHENTICATION_RESULT': result, 
                                    'SIMILARITY_INFORMATION': [max_sim, avg_sim]}

                    df_frame = df_frame.append(result_frame, ignore_index=True)

                else:
                    pass

    else: 
        pass

    student_fail_list = list(set(student_name_list) - set(student_success_list))

    for fail in student_fail_list:
        result_frame = {'FRAME' : frame_name,
                'STUDENT_NAME': fail,
                'FACE': 'CAN NOT IDENTIFY', 
                'AUTHENTICATION_RESULT': 'FAIL',
                'SIMILARITY_INFORMATION': 'NO INFORMATION'}

        df_frame = df_frame.append(result_frame, ignore_index=True)
        
    q.put(df_frame)



def main(facial_feature_path, frame_dir, n_thread):

    print('Starting: Compare Facial_frame and Facial_photo')
    threads = []
    df_list = []
    q = Queue()

    parser = argparse.ArgumentParser(description='insightface app test')
    # general
    parser.add_argument('--ctx', default=1, type=int, help='ctx id, <0 means using cpu')
    parser.add_argument('--det-size', default=640, type=int, help='detection size')
    args, _ = parser.parse_known_args()

    app = FaceAnalysis()
    app.prepare(ctx_id=args.ctx, det_size=(args.det_size,args.det_size))

    frames_list = glob.glob(join(frame_dir, "*.jpg"))

    data = {'FRAME' :[],
        'STUDENT_NAME': [], 
        'FACE': [], 
        'AUTHENTICATION_RESULT': [], 
        'SIMILARITY_INFORMATION': []}

    df_frame = pd.DataFrame(data)
    df_frame.index = df_frame.index + 1
    df_frame.to_excel("/workspace/AdvanceProjectforAIConvergence/coding/python/RESULT/Authentication_Result.xlsx", engine='xlsxwriter')
    df_path = '/workspace/AdvanceProjectforAIConvergence/coding/python/RESULT/Authentication_Result.xlsx'
    
    for f in range(len(frames_list)):
        threads.append(threadFun(compare_sim, (frames_list[f], facial_feature_path, q, app)))
                
    run_threads(threads, n_thread)

    while q.qsize() < len(frames_list):
        time.sleep(0.1)  # 100ms

    print('all threads is finished') 

    for _ in range(q.qsize()):
        df_list.append(q.get())


    save_xls(df_list, df_path)

    return df_path
    

def save_xls(list_dfs, xls_path):
    with ExcelWriter(xls_path) as writer:
        for n, df in enumerate(list_dfs):
            df.to_excel(writer,'{}'.format(list_dfs[n]['FRAME'][0]))
        writer.save()
  

def run_threads(threads, n_thread):
    used_thread = []
    for num, new_thread in enumerate(threads):
        print('thread index: {:}'.format(num), end=' \t')
        new_thread.start()
        used_thread.append(new_thread)
        
        # if num % n_thread == 0:
        #     for old_thread in used_thread:
        #         old_thread.join()
        #     used_thread = []    


class threadFun(threading.Thread):
    def __init__(self, func, args):
        super(threadFun, self).__init__()
        self.fun = func
        self.args = args
    def run(self):
        self.fun(*self.args)



if __name__ == '__main__' :

    facial_feature_path = '/workspace/AdvanceProjectforAIConvergence/coding/python/DATASET/PHOTOSET_10PICS.pkl'
    frame_dir = '/workspace/AdvanceProjectforAIConvergence/coding/python/IMAGE_FRAMES/recorded_video1'

    main(facial_feature_path, frame_dir, n_thread=10)