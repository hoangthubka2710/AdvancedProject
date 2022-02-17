import cv2
import os
from os.path import join
import glob
import sys


def extractimageframe(recorded_path):
    print('STEP 1: EXTRACTING IMAGE FRAMES')
    print('Please fill in recorded video path')

    # recorded_path = str(input())

    print('Check recorded_path again...')
    print(recorded_path)

    video = cv2.VideoCapture(recorded_path)

    # Find OpenCV version
    (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

    if int(major_ver)  < 3 :
        fps = video.get(cv2.cv.CV_CAP_PROP_FPS)
        print ("Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {0}".format(fps))
    else :
        fps = video.get(cv2.CAP_PROP_FPS)
        print ("Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps))

    save_dir_name = recorded_path.split('/')[-1].split('.')[0]
    save_dir_path = f'/workspace/AdvanceProjectforAIConvergence/coding/python/IMAGE_FRAMES/{save_dir_name}'

    if os.path.exists(save_dir_path) == False:
        os.mkdir(save_dir_path)

    if os.path.exists(save_dir_path) == True:
        print('Image Frames are extracted. Please check it again')

    

    print("Directory to save image frames is created with the name: ")
    print(save_dir_path)
    print('')
    print('Image Frames is extracting ...')

    i=0
    while(video.isOpened()):
        ret, frame = video.read()
        if ret == False:
            break
        if i% (20) == 0:
            cv2.imwrite(f'{save_dir_path}/frame'+str(i)+'.jpg',frame)
        i+=1


    img_list = glob.glob(join(save_dir_path, '*.jpg'))

    num_img = len(img_list)
    print('Number of image frames is ', num_img)
    print('STEP 1 - FINISHED - Extracting Image Frames')

    video.release()
    cv2.destroyAllWindows()

    return save_dir_path, num_img


if __name__ == '__main__' :
    extractimageframe()