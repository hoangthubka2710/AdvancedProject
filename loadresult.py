import pandas as pd
import os
import glob
from os.path import join

def loadresult(result_path):
    result_data = pd.read_excel(result_path, None)
    frames_list = list(result_data.keys())
    frame_rate = len(frames_list)
    student_name_list = list(result_data[frames_list[0]]['STUDENT_NAME'].values)
    attendance_rate = {}
    for s in student_name_list:
        attendance_rate.update({
            f'{s}': 0
        })

    for f in frames_list:
        result_frame = result_data[f]
        for s in student_name_list:
            attendance = result_frame['AUTHENTICATION_RESULT'][result_frame['STUDENT_NAME']==s].values[0]
            if attendance == 'SUCCESS':
                attendance_rate[f'{s}'] += 1
    FINAL_ATTENDANCE_LIST = []

    id = 1
    for a in list(attendance_rate.keys()):
        FINAL_ATTENDANCE = {}
        rate_value = attendance_rate[a]
        concentration_level = float("{:.2f}".format(rate_value/frame_rate*100))
        if concentration_level >= 30:
            final_authentication = 'SUCCESS'
        else:
            final_authentication = 'FAIL'
            
        FINAL_ATTENDANCE.update({
            'ID': id,
            'STUDENT_NAME': a,
            'CONCENTRATION_LEVEL': concentration_level,
            'FINAL_RESULT': final_authentication
        })
        FINAL_ATTENDANCE_LIST.append(FINAL_ATTENDANCE)
        id = id + 1

    df = pd.DataFrame(columns=['ID', 'STUDENT_NAME', 'CONCENTRATION_LEVEL', 'FINAL_RESULT'])

    for l in range(len(FINAL_ATTENDANCE_LIST)):
        one_student = FINAL_ATTENDANCE_LIST[l]
        df = df.append(one_student, ignore_index=True)
    
    df.sort_values(by='CONCENTRATION_LEVEL')
    df.index.name = 'ID'
    df.to_excel("/workspace/AdvanceProjectforAIConvergence/coding/python/RESULT/Final_Authentication_Result.xlsx", 'wb', index=False)

if __name__ == '__main__' :
    result_path = '/workspace/AdvanceProjectforAIConvergence/coding/python/RESULT/Authentication_Result.xlsx'
    loadresult(result_path)