import time
from queue import Queue
import pickle as pkl
import threading
import csv
from tqdm import tqdm
from os.path import join
import os
import glob
from PIL import Image
import matplotlib.pyplot as plt
from insightface.data import get_image as ins_get_image
from insightface.app import FaceAnalysis
import insightface
import numpy as np
import sys
import cv2
import argparse
import warnings
warnings.filterwarnings('ignore')

assert insightface.__version__ >= '0.3'


def processing_onedir(student_path, q, app):

    student_feature = []
    student_img_list = glob.glob(join(student_path, '*jpg'))
    student_name = student_path.split('/')[-1]
    print("Student name: ", student_name)

    for img in range(len(student_img_list)):
        image = plt.imread(student_img_list[img])
        face_photo = app.get(image)  # len face photo set image = 1
        feature_photo = face_photo[0].normed_embedding

        student_feature.append({
            'student_name': student_name,
            'image_index': student_img_list[img],
            'facial_feature': feature_photo,
        })

    q.put(student_feature)


def main_processing_photoset(photoset_path, n_thread):

    threads = []
    feature_dirs = []

    q = Queue()

    parser = argparse.ArgumentParser(description='insightface app test')
    # general
    parser.add_argument('--ctx', default=1, type=int,
                        help='ctx id, <0 means using cpu')
    parser.add_argument('--det-size', default=640,
                        type=int, help='detection size')
    args, _ = parser.parse_known_args()

    app = FaceAnalysis()
    app.prepare(ctx_id=args.ctx, det_size=(args.det_size, args.det_size))

    directory_contents = os.listdir(photoset_path)

    print("directory_contents", directory_contents)

    for i in tqdm(range(len(directory_contents))):
        student_path = '{}/{}'.format(photoset_path, directory_contents[i])
        print(student_path)
        threads.append(threadFun(processing_onedir, (student_path, q, app)))

    run_threads(threads, n_thread)

    while q.qsize() < len(directory_contents):
        time.sleep(0.1)  # 100ms

    print('all threads is finished')
    
    for i in range(q.qsize()):
        feature_dirs.append(q.get())

    print('Len of feature dir', len(feature_dirs))

    with open('/{}.pkl'.format(photoset_path), 'wb') as f:
        pkl.dump(feature_dirs, f)

    pikle_datafile = '/{}.pkl'.format(photoset_path)

    print(pikle_datafile)
    return pikle_datafile


def run_threads(threads, n_thread):
    used_thread = []
    for num, new_thread in enumerate(threads):
        print('thread index: {:}'.format(num), end=' \t')
        new_thread.start()
        used_thread.append(new_thread)


class threadFun(threading.Thread):
    def __init__(self, func, args):
        super(threadFun, self).__init__()
        self.fun = func
        self.args = args

    def run(self):
        self.fun(*self.args)


# if __name__ == '__main__':

#     photoset_path = '/workspace/AdvanceProjectforAIConvergence/coding/python/DATASET/PHOTOSET_10PICS'
#     main_processing_photoset(photoset_path, n_thread=2)
