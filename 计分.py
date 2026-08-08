import csv
import pandas as pd
from decorator import append


##############################################
def score():
        name = input('姓名：')
        while 1:
            try:
                num1 = float(input('1.请输入晚上睡觉时间(12小时制的时间,晚上超过12点，写13点)：'))
                break
            except:
                print('输入有误，请重新输入')
        while 1:
            try:
                num2 = float(input('2.请输入上床到入睡所需时间(超过60分钟即为最大值)：'))
                if num2 < 15:
                    B1 = 0
                elif num2 >= 15 and num2 < 30:
                    B1 = 1
                elif num2 >= 30 and num2 < 60:
                    B1 = 2
                else:
                    B1 = 3
                break
            except:
                print('输入有误，请重新输入')
        ###################################################
        while 1:
            try:
                num3 = float(input('3.请输早上起床时间(12小时制的时间)：')) + 12
                break
            except:
                print('输入有误，请重新输入')
        while 1:
            try:
                num4 = float(input('4.请输入实际睡眠时间：'))
                if num4 > 7:
                    C = 0
                elif num4 > 6 and num4 <= 7:
                    C = 1
                elif num4 > 5 and num4 <= 6:
                    C = 2
                else:
                    C = 3
                break
            except:
                print('输入有误，请重新输入')
        ##################################################
        while 1:
                num5 = input('5.请输入第5题的选项：')
                match num5.upper():
                    case 'A':
                        B2 = 0
                        break
                    case 'B':
                        B2 = 1
                        break
                    case 'C':
                        B2 = 2
                        break
                    case 'D':
                        B2 = 3
                        break
                    case _:
                        print('输入有误，请重新输入')
                        continue

        ##############################################
        num_lst = []
        lst = []
        for i in range(6,15):
            while 1:
                num = input(f'{i}.请输入第{i}题的选项：')
                match num.upper():
                    case 'A':
                        E_score = 0
                        break
                    case 'B':
                        E_score = 1
                        break
                    case 'C':
                        E_score = 2
                        break
                    case 'D':
                        E_score = 3
                        break
                    case _:
                        print('输入有误，请重新输入')
                        continue
            lst.append(E_score)
            num_lst.append(num)
        ###################################################
        E_final = sum(lst)
        if E_final >= 0 and E_final <= 9:
            E = 1
        elif E_final >= 10 and E_final <= 18:
            E = 2
        elif E_final >= 19 and E_final <= 27:
            E = 3
        else:
            E = 0
        #########################################
        while 1:
            num15 = input("15.请输入第15题的选项:")
            match num15.upper():
                case 'A':
                    A = 0
                    break
                case 'B':
                    A = 1
                    break
                case 'C':
                    A = 2
                    break
                case 'D':
                    A = 3
                    break
                case _:
                    print('输入错误,请重新输入')
                    continue
        ###################################################
        #计算F部分分数
        while 1:
            num16 = input('16.请输入第16题的选项：')
            match num16.upper():
                case 'A':
                    F = 0
                    break
                case 'B':
                    F = 1
                    break
                case 'C':
                    F = 2
                    break
                case 'D':
                    F = 3
                    break
                case _:
                    print('输入错误,请重新输入')
                    continue
        #计算G部分分数
        while 1:
            num17 = input('17.请输入第17题的选项：')
            match num17.upper():
                case 'A':
                    G1 = 0
                    break
                case 'B':
                    G1 = 1
                    break
                case 'C':
                    G1 = 2
                    break
                case 'D':
                    G1 = 3
                    break
                case _:
                    print('输入错误,请重新输入')
                    continue
        while 1:
            num18 = input('18.请输入第18题的选项：')
            match num18.upper():
                case 'A':
                    G2 = 0
                    break
                case 'B':
                    G2 = 1
                    break
                case 'C':
                    G2 = 2
                    break
                case 'D':
                    G2 = 3
                    break
                case _:
                    print('输入错误,请重新输入')
                    continue

        ###########################################
        D1 = num4 / (num3 - num1)
        if D1 >= 0.85:
            D = 0
        elif D1 >= 0.75 and D1 < 0.85:
            D = 1
        elif D1 >= 0.65 and D1 <0.75:
            D = 2
        else:
            D = 3
        ################################
        B3 = B1 + B2
        if B3 > 1 and B3 <=2:
            B = 1
        elif B3 > 2 and B3 <=3:
            B = 2
        elif B3 > 5 and B3 <=6:
            B = 3
        else:
            B =0
        ###############################
        G3 = G1 + G2
        if G3 > 1 and G3 <=2:
            G = 1
        elif G3 > 2 and G3 <=3:
            G = 2
        elif G3 > 5 and G3 <=6:
            G = 3
        else:
            G =0
        ###########################
        total = A + B + C + D + E + F + G
        while 1:
            try:
                SAS = int(input('请输入SAS分数'))
                break
            except:
                print('请输入整数')
        while 1:
            try:
                SDS = int(input('请输入SDS分数'))
                break
            except:
                print('请输入整数')



        print(f'A部分:{A}\n B部分:{B}\n,C部分:{C}\n,D部分:{D}\n,E部分:{E}\n,F部分:{F}\n,G部分:{G}\n,总分:{total}\n')
        df = pd.DataFrame([{
            '姓名' : name,
            '第一题' : num1,
            '第二题' : num2,
            '第三题' : num3,
            '第四题' : num4,
            '第五题' : num5,
            '第六题' : num_lst[0],
            '第七题' : num_lst[1],
            '第八题' : num_lst[2],
            '第九题' : num_lst[3],
            '第十题' : num_lst[4],
            '第十一题' : num_lst[5],
            '第十二题' : num_lst[6],
            '第十三题' : num_lst[7],
            '第十四题' : num_lst[8],
            '第十五题' : num15,
            '第十六题' : num16,
            '第十七题' : num17,
            '第十八题' : num18,
            'A部分' : A,
            'B部分' : B,
            'C部分' : C,
            'D部分' : D,
            'E部分' : E,
            'F部分' : F,
            'G部分' : G,
            '总分': total,
            'SAS' : SAS,
            'SDS' : SDS
        }])
        return df
if __name__ == '__main__':
    score()