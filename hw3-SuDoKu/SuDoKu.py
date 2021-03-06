## This code is for SuDoKu Agent.
# Authors: Liqiang He, Eugene Seo
from fixed_baseline import *
from MCV import *
from Inference import *
from utility import *
import time
import re


def forward_checking(cells_status):
    for i in range(81):
        if cells_status[i][0] != 0:         # if the cell number is fixed(given), then forward check it
            clean_row(i, cells_status)
            clean_col(i, cells_status)
            clean_box(i, cells_status)

def sudoku(initialState, rule_list):
    # input:     initialState,a str of 81 initial values
    # print(initialState)
    # get data structures
    cells_status = get_initialDict(initialState)
    #inference_recursive(cells_status,50)
    #print(check_goal_3rule(cells_status))

    # apply fixed baseline approach
    t1 = float(time.clock())
    success1, result_cells1, used_steps_fb = fixed_baseline(cells_status, 0, 0, rule_list)
    t2 = float(time.clock())
    # print(check_goal_3rule(result_cells))
    # print(used_steps_fb)
    #
    # print("Begin MCV:")
    t3 = float(time.clock())
    success2, result_cells2, used_steps_mcv = MCV(cells_status, 0 , rule_list)
    t4 = float(time.clock())
    # if success:
    #     print(check_goal_3rule(result_cells))
    # print(used_steps_mcv)
    # print(success1, used_steps_fb)
    # result_print(result_cells1)
    # result_print(result_cells2)
    return used_steps_fb, used_steps_mcv, t2-t1, t4-t3,  success1, success2

def series_sudoku(samples):
    res_fb = []
    res_mcv = []
    rule_lists = []
    rule_lists.append([])
    rule_lists.append([11, 12])
    rule_lists.append([11, 12, 21, 22])
    rule_lists.append([11, 12, 21, 22, 31, 32]) # add rule list 1

    m = len(rule_lists)         # number of rule lists
    n = len(samples)            # 71 samples


    res = [[0 for x in range(n)] for y in range(m)]
    for jdx, rule_list in enumerate(rule_lists):
        for i in range(77):
            test = samples[i+1][0]
            fb, mcv, time1, time2, s1, s2 = sudoku(test, rule_list)
            res_fb.append(fb)
            res_mcv.append(mcv)
            res[jdx][i] = (i, fb, mcv, time1, time2)
            print(i, fb, mcv, time1, time2,  mcv < fb, s1, s2)
    print(res)
    with open("data/result.txt", "w") as f:
        for i in range(len(res)):
            for j in range(77):
                f.write("%s %s %s %s %s \n" %
                        (str(res[i][j][0]), str(res[i][j][1]), str(res[i][j][2]), str(res[i][j][3]), str(res[i][j][4])))
            f.write("********\n")
if __name__ == '__main__':
    # load data
    filePath = 'data/sudoku-problems.txt'
    samples = getData(filePath)

    # test = samples[1][0]
    # test_rule_list = [11, 12, 21, 22, 31, 32]
    # test_rule_list = []
    # print(sudoku(test, test_rule_list))
    series_sudoku(samples)
    # print(sudoku(samples[13][0], []))

    # for i in range(1, 78):
    #     print(samples[i])
    '''
    diff = []
    for i in range(77):
        data = samples[i+1][1]
        tt = re.split('(\d+)', data)
        diff.append(tt[2])
    #
    # print(diff)
    # with open("data/result_diff.txt", "w") as f:
    #     for i in range(77):
    #         f.write("%s\n"%diff[i])
    easy = 0
    med = 0
    hard = 0
    evil = 0
    print(filled_in_num(samples[1][0]))
    for i in range(77):
        tt = filled_in_num(samples[i+1][0])
        if diff[i] == "Easy":
            easy += tt
        if diff[i] == "Medium":
            med += tt
        if diff[i] == "Hard":
            hard += tt
        if diff[i] == "Evil":
            evil += tt
    print(easy, med, hard, evil)
    print(easy/23, med/21, hard/18, evil/15)
    '''