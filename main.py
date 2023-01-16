'''该文件将用于界面的生成，以及用excl表格保存输入数据
用一个excl表格存储数据，以达到记忆功能
这个excl表格将会由程序创建，用户将有权决定他的储存数据
在用户调用历史数据时，这个程序会读取并将其表示出来'''
# 打包用我（pyinstaller -F -w main.py --hidden-import=['openpyxl']）
import os
import time
# ----------------------------------------------------------------------------------------------------------------------
from tkinter import *
from tkinter import ttk
import tkinter as TK
# ----------------------------------------------------------------------------------------------------------------------
import openpyxl
# ----------------------------------------------------------------------------------------------------------------------
import math
import numpy as np
import pandas as pd
from sympy import *
from sympy import S, symbols, nonlinsolve, Rational, I
# ----------------------------------------------------------------------------------------------------------------------
import matplotlib
from matplotlib.figure import Figure
from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt
from matplotlib.pylab import mpl
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.pyplot import MultipleLocator


# ----------------------------------------------------------------------------------------------------------------------


class analpressmecaism(Frame):  # 定义显示窗口界面的类

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.welcome()

    def window_destroy(self):  # 该方法用与摧毁之前留下的窗口界面残留
        for widget in self.winfo_children():
            widget.destroy()

    def wait(self):
        self.label_wait = Label(self, text="请稍等······")
        self.label_wait.pack()

    def welcome(self):  # 欢迎界面
        self.label_welcome = Label(self, text="欢迎使用本机构解析发软件（*^-^*），如有使用问题请联系2564977456@qq.com")
        self.label_welcome.pack()
        self.button_start = Button(self, text="开始", command=self.first_use_judge)
        self.button_start.pack()
        self.button_quit = Button(self, text="结束", command=self.quit)
        self.button_quit.pack()

    def first_use_judge(self):  # 该方法用于多选判断之前是否存储过界面的页面
        self.window_destroy()
        self.label_use_judge = Label(self, text="是否创建过存储表格")
        self.label_use_judge.pack()
        self.use_yes = IntVar();
        self.use_no = IntVar()
        print(self.use_yes.get())
        self.c_use_y = Checkbutton(self, text='是', variable=self.use_yes, onvalue=1, offvalue=0)
        self.c_use_n = Checkbutton(self, text='否', variable=self.use_no, onvalue=1, offvalue=0)
        self.c_use_y.pack(side='left')
        self.c_use_n.pack(side='left')

        Button(self, text='确定', command=self.use_judge_confirm).pack(side='left')

    def use_judge_confirm(self):  # 该方法是对于上方self.first_use_judge()的延续，用于对其结果进行判断处理
        if self.use_yes.get() == 1:  # 如果说存储过的话，询问存储路径并查找判断
            self.window_destroy()
            self.label_use_judge = Label(self, text="请输入上次存储路径，默认工作目录")
            self.label_use_judge.pack()
            v_store_place = StringVar()
            self.entry_store_place = Entry(self, textvariable=v_store_place)
            self.entry_store_place.pack()
            workplace = os.getcwd()
            v_store_place.set(workplace)
            print(v_store_place.get())
            print(self.entry_store_place.get())
            self.store_place_judgeb = Button(self, text="检查", command=self.store_place_judge)
            self.store_place_judgeb.pack()
            # 检查会转到下面self.store_place_judge进行判断
            self.store_place_back = Button(self, text="回退上一级", command=self.first_use_judge)
            self.store_place_back.pack()
        if self.use_no.get() == 1:  # 如果说没有存储过的话，直接跳转到新建储存文件函数
            self.store_place()

    def store_place(self):  # 该方法用与进行进行新建存储文件操作
        self.window_destroy()
        self.label_store_place = Label(self, text="请选择你要存储数据的位置,默认在程序文件夹,推荐默认，其他位置可能存在后续不兼容")
        self.label_store_place.pack()
        v_store_place = StringVar()
        self.entry_store_place = Entry(self, textvariable=v_store_place)
        self.entry_store_place.pack()
        workplace = os.getcwd()
        v_store_place.set(workplace)
        print(v_store_place.get())
        print(self.entry_store_place.get())
        self.store_place_judgeb = Button(self, text="创建", command=self.store_place_judge)
        self.store_place_judgeb.pack()

    def store_place_judge(self):  # 该方法是对于存储位置是否有该文件的判断
        path = self.entry_store_place.get()
        self.window_destroy()
        # 先得到数据，再对之前的窗口界面进行清除
        excl_path = os.path.join(path, '解析法机构分析用表.xlsx')
        if not os.path.exists(excl_path):  # 如果判断没有存储文件
            new_wb = openpyxl.Workbook()  # 创建工作簿
            sheet = new_wb.active  # 创建工作表
            sheet.title = '数据记录表格'  # 设置工作表标题
            # 设置工作表各单元标题
            sheet["A1"].value = "时间"
            sheet["B1"].value = "备注"
            sheet["C1"].value = "l1长度（m）"
            sheet["D1"].value = "l2长度（m）"
            sheet["E1"].value = "l3长度（m）"
            sheet["F1"].value = "lcd长度（m）"
            sheet["G1"].value = "l4长度（m）"
            sheet["H1"].value = "AD水平距离x1（m）"
            sheet["I1"].value = "DF水平距离x2（m）"
            sheet["J1"].value = "AD竖直距离y（m）"
            sheet["K1"].value = "原动件转速n1（r/min）"
            sheet["L1"].value = "步进取点角度"
            new_wb.save('解析法机构分析用表.xlsx')  # 保存工作簿
            self.label_store_place_judge = Label(self, text="创建成功")  # 反馈创建成功
            self.label_store_place_judge.pack()
        else:
            self.label_store_place_judge = Label(self, text="已有对应文件")  # 如果已有文件，反馈已有对应文件
            self.label_store_place_judge.pack()
        self.button_store_data = Button(self, text="开始记录数据", command=self.to_store_data)  # 直接用现有数据计算
        self.button_store_data.pack()
        self.button_to_memory_data = Button(self, text="为我展示历史数据，我要计算历史数据", command=self.show_memory_data)  # 可以调用历史数据
        self.button_to_memory_data.pack()

    def to_store_data(self):  # 对于新数据的录入
        self.window_destroy()
        self.label_store_datal1 = Label(self, text="请输入l1长度（m）")
        self.label_store_datal1.pack()
        v_store_datal1 = StringVar()
        self.entry_store_datal1 = Entry(self, textvariable=v_store_datal1)
        self.entry_store_datal1.pack()
        v_store_datal1.set('0.0628192')
        print(v_store_datal1.get())
        print(self.entry_store_datal1.get())
        self.label_store_datal2 = Label(self, text="请输入l2长度（m）")
        self.label_store_datal2.pack()
        v_store_datal2 = StringVar()
        self.entry_store_datal2 = Entry(self, textvariable=v_store_datal2)
        self.entry_store_datal2.pack()
        v_store_datal2.set('0.2419643')
        print(v_store_datal2.get())
        print(self.entry_store_datal2.get())
        self.label_store_datal3 = Label(self, text="请输入l3长度（m）")
        self.label_store_datal3.pack()
        v_store_datal3 = StringVar()
        self.entry_store_datal3 = Entry(self, textvariable=v_store_datal3)
        self.entry_store_datal3.pack()
        v_store_datal3.set('0.19')
        print(v_store_datal3.get())
        print(self.entry_store_datal3.get())
        self.label_store_datalcd = Label(self, text="请输入lcd长度（m）")
        self.label_store_datalcd.pack()
        v_store_datalcd = StringVar()
        self.entry_store_datalcd = Entry(self, textvariable=v_store_datalcd)
        self.entry_store_datalcd.pack()
        v_store_datalcd.set('0.1266667')
        print(v_store_datalcd.get())
        print(self.entry_store_datalcd.get())
        self.label_store_datal4 = Label(self, text="请输入l4长度（m）")
        self.label_store_datal4.pack()
        v_store_datal4 = StringVar()
        self.entry_store_datal4 = Entry(self, textvariable=v_store_datal4)
        self.entry_store_datal4.pack()
        v_store_datal4.set('0.057')
        print(v_store_datal4.get())
        print(self.entry_store_datal4.get())
        self.label_store_datax1 = Label(self, text="请输入AD水平距离x1（m）")
        self.label_store_datax1.pack()
        v_store_datax1 = StringVar()
        self.entry_store_datax1 = Entry(self, textvariable=v_store_datax1)
        self.entry_store_datax1.pack()
        v_store_datax1.set('0.08')
        print(v_store_datax1.get())
        print(self.entry_store_datax1.get())
        self.label_store_datax2 = Label(self, text="请输入DF水平距离x2（m）")
        self.label_store_datax2.pack()
        v_store_datax2 = StringVar()
        self.entry_store_datax2 = Entry(self, textvariable=v_store_datax2)
        self.entry_store_datax2.pack()
        v_store_datax2.set('0.150')
        print(v_store_datax2.get())
        print(self.entry_store_datax2.get())
        self.label_store_datay = Label(self, text="请输入AD竖直距离y（m）")
        self.label_store_datay.pack()
        v_store_datay = StringVar()
        self.entry_store_datay = Entry(self, textvariable=v_store_datay)
        self.entry_store_datay.pack()
        v_store_datay.set('0.240')
        print(v_store_datay.get())
        print(self.entry_store_datay.get())
        self.label_store_datan1 = Label(self, text="请输入原动件转速n1（r/min）")
        self.label_store_datan1.pack()
        v_store_datan1 = StringVar()
        self.entry_store_datan1 = Entry(self, textvariable=v_store_datan1)
        self.entry_store_datan1.pack()
        v_store_datan1.set('110')
        print(v_store_datan1.get())
        print(self.entry_store_datan1.get())
        self.label_store_dataps = Label(self, text="您可以为这组数据添加一个备注")
        self.label_store_dataps.pack()
        v_store_dataps = StringVar()
        self.entry_store_dataps = Entry(self, textvariable=v_store_dataps)
        self.entry_store_dataps.pack()
        v_store_dataps.set('无')
        print(v_store_dataps.get())
        print(self.entry_store_dataps.get())
        self.label_angel = Label(self, text="请输入您希望所隔多少角度取一个数据点")
        self.label_angel.pack()
        v_angel = StringVar()
        self.entry_angel = Entry(self, textvariable=v_angel)
        self.entry_angel.pack()
        v_angel.set('1')
        print(v_angel.get())
        print(self.entry_angel.get())
        self.button_to_store_data = Button(self, text="导入", command=self.store_data)
        self.button_to_store_data.pack()

    def store_data(self):  # 该方法用于把上文的内容存入excel表
        l1 = self.entry_store_datal1.get()
        l2 = self.entry_store_datal2.get()
        l3 = self.entry_store_datal3.get()
        lcd = self.entry_store_datalcd.get()
        l4 = self.entry_store_datal4.get()
        x1 = self.entry_store_datax1.get()
        x2 = self.entry_store_datax2.get()
        y = self.entry_store_datay.get()
        n1 = self.entry_store_datan1.get()
        ps = self.entry_store_dataps.get()
        angel = self.entry_angel.get()
        store_time = time.strftime('%Y%m%d%H%M%S')
        wb = openpyxl.load_workbook('解析法机构分析用表.xlsx')
        sheet = wb['数据记录表格']
        sheet.append([store_time, ps, l1, l2, l3, lcd, l4, x1, x2, y, n1, angel])
        wb.save('解析法机构分析用表.xlsx')
        self.window_destroy()
        self.label_store_datan1 = Label(self, text="导入成功")
        self.label_store_datan1.pack()
        self.button_to_calculate_data = Button(self, text="开始计算", command=self.new_calculate)
        self.button_to_calculate_data.pack()
        self.button_to_memory_data = Button(self, text="为我展示历史数据，我要计算历史数据", command=self.show_memory_data)
        self.button_to_memory_data.pack()

    def show_memory_data(self):  # 因为tkinter不支持显示DataFrame表格数据，这里创建了一个支持的新表用于显示，DataFrame不显示用与调取数据计算，类似于一种镜像
        self.window_destroy()
        data_memory = pd.read_excel('解析法机构分析用表.xlsx', sheet_name='数据记录表格')
        print(data_memory)
        tree = ttk.Treeview(self)
        tree['columns'] = (
            '时间', '备注', 'l1长度（m)', 'l2长度（m)', 'l3长度（m)', 'lcd长度（m)', 'l4长度（m)', 'AD水平距离x1（m)', 'DF水平距离x2（m)',
            'AD竖直距离y（m)', '原动件转速n1（r/min)', '步进取点角度')
        tree.column('时间', width=150)
        tree.column('备注', width=100)
        tree.column('l1长度（m)', width=100)
        tree.column('l2长度（m)', width=100)
        tree.column('l3长度（m)', width=100)
        tree.column('lcd长度（m)', width=100)
        tree.column('l4长度（m)', width=100)
        tree.column('AD水平距离x1（m)', width=100)
        tree.column('DF水平距离x2（m)', width=100)
        tree.column('AD竖直距离y（m)', width=100)
        tree.column('原动件转速n1（r/min)', width=100)
        tree.column('步进取点角度', width=100)
        tree.heading('时间', text='时间')
        tree.heading('备注', text='备注')
        tree.heading('l1长度（m)', text='l1长度（m)')
        tree.heading('l2长度（m)', text='l2长度（m)')
        tree.heading('l3长度（m)', text='l3长度（m)')
        tree.heading('lcd长度（m)', text='lcd长度（m)')
        tree.heading('l4长度（m)', text='l4长度（m)')
        tree.heading('AD水平距离x1（m)', text='AD水平距离x1（m)')
        tree.heading('DF水平距离x2（m)', text='DF水平距离x2（m)')
        tree.heading('AD竖直距离y（m)', text='AD竖直距离y（m)')
        tree.heading('原动件转速n1（r/min)', text='原动件转速n1（r/min)')
        tree.heading('步进取点角度', text='步进取点角度')
        for row_number in range(data_memory.shape[0]):
            tree.insert('', row_number, text=str(row_number), values=data_memory.loc[row_number].values)
        tree.pack()
        self.button_store_data = Button(self, text="我要创建新数据计算", command=self.to_store_data)
        self.button_store_data.pack()
        self.button_use_memory_data = Button(self, text="我要使用旧有数据", command=self.use_memory_data)
        self.button_use_memory_data.pack()

    def use_memory_data(self):  # 旧数据直接输入序号去dataframe找 ，本方法用于输入组序号
        self.button_store_data.destroy()
        self.label_memory_data_number = Label(self, text="请输入使用组序号")
        self.label_memory_data_number.pack()
        v_memory_data_number = StringVar()
        self.entry_memory_data_number = Entry(self, textvariable=v_memory_data_number)
        self.entry_memory_data_number.pack()
        v_memory_data_number.set('0')
        print(v_memory_data_number.get())
        print(self.entry_memory_data_number.get())
        self.button_to_calculate_data = Button(self, text="开始计算", command=self.memory_calculate)
        self.button_to_calculate_data.pack()

    def memory_calculate(self):  # 旧数据直接输入序号去dataframe找 ，本方法用于通过组序号赋予变量值
        row_number = self.entry_memory_data_number.get()
        data_memory = pd.read_excel('解析法机构分析用表.xlsx', sheet_name='数据记录表格')
        values = data_memory.loc[int(row_number)].values
        print(values)
        l1 = float(values[2])
        l2 = float(values[3])
        l3 = float(values[4])
        lcd = float(values[5])
        l4 = float(values[6])
        x1 = float(values[7])
        x2 = float(values[8])
        y = float(values[9])
        n1 = float(values[10])
        angel = int(values[11])
        self.calculate_x(l1, l2, l3, lcd, l4, x1, x2, y, n1, angel)

    def new_calculate(self):  # 新数据直接输入序号去dataframe找 最后一行数据
        data_memory = pd.read_excel('解析法机构分析用表.xlsx', sheet_name='数据记录表格')
        data_length = len(data_memory)
        values = data_memory.loc[data_length - 1].values
        l1 = float(values[2])
        l2 = float(values[3])
        l3 = float(values[4])
        lcd = float(values[5])
        l4 = float(values[6])
        x1 = float(values[7])
        x2 = float(values[8])
        y = float(values[9])
        n1 = float(values[10])
        angel = int(values[11])
        self.calculate_x(l1, l2, l3, lcd, l4, x1, x2, y, n1, angel)

    '''def destory_wait(self, l1, l2, l3, lcd, l4, x1, x2, y, n1, angel):
        for widget in self.winfo_children():
            widget.destroy()
        self.label_wait = Label(self, text="请稍等······")
        self.label_wait.pack()
        self.calculate(l1, l2, l3, lcd, l4, x1, x2, y, n1, angel)'''

    def calculate_x(self, l1, l2, l3, lcd, l4, x1, x2, y, n1, angel):  # 计算位置
        self.window_destroy()
        self.label_rade_x = Label(self, text="正在努力计算位置呀QAQ")
        self.label_rade_x.pack()
        self.wait()
        print(l1)
        print(l2)
        print(l3)
        print(lcd)
        print(l4)
        print(x1)
        print(x2)
        print(y)
        print(n1)
        print(angel)
        th2, th3, th4, s5 = symbols('th2 th3 th4 th5', real=True)
        s5store = []
        th2store = []
        th3store = []
        th4store = []
        th1store = []
        progressbarOne = ttk.Progressbar(self)
        progressbarOne.pack(pady=20)
        # 进度值最大值
        progressbarOne['maximum'] = (360 / angel)
        # 进度值初始值
        progressbarOne['value'] = 0
        for th1r in range(0, 360, angel):
            th1 = th1r * 2 * np.pi / 360
            th1store.append(th1)
            # 每次更新加1
            progressbarOne['value'] += 1
            # 更新画面
            self.update()
            time.sleep(0.05)
            f1 = l1 * cos(th1) - l2 * cos(th2) + lcd * cos(th3) - x1
            f2 = l1 * sin(th1) + l2 * sin(th2) - lcd * sin(th3) - y
            f3 = -l3 * cos(th3) + l4 * cos(th4) + x2
            f4 = -l3 * sin(th3) + l4 * sin(th4) - s5
            system = [f1, f2, f3, f4]
            solve_value = solve(system, [th2, th3, th4, s5])
            print(solve_value)
            # 要通过th4角度进行限制<pi/2
            for ith in range(2):
                if solve_value[ith][2] < np.pi / 2:
                    s5store.append(float(solve_value[ith][3]))
                    th2store.append(float(solve_value[ith][0]))
                    th3store.append(float(solve_value[ith][1]))
                    th4store.append(float(solve_value[ith][2]))

        print(s5store)
        print(type(s5store))
        print(th1store)
        print(type(th1store))
        self.calculate_v(th1store, th2store, th3store, th4store, s5store, l1, l2, l3, lcd, l4, n1, angel)

    def calculate_v(self, th1store, th2store, th3store, th4store, s5store, l1, l2, l3, lcd, l4, n1, angel):#计算速度
        self.window_destroy()
        self.label_rade_v = Label(self, text="正在努力计算速度呀QAQ")
        self.label_rade_v.pack()
        self.wait()
        print(f'th1store{th1store}')
        print(f'th2store{th2store}')
        print(f'th3store{th3store}')
        print(f'th4store{th4store}')
        w2store = []
        w3store = []
        w4store = []
        v5store = []
        w1 = n1 * 2 * np.pi / 60
        w2, w3, w4, v5 = symbols('w2 w3 w4 v5', real=True)
        progressbarOne = ttk.Progressbar(self)
        progressbarOne.pack(pady=20)
        # 进度值最大值
        progressbarOne['maximum'] = (360 / angel)
        # 进度值初始值
        progressbarOne['value'] = 0
        for iv in range(len(th1store)):
            # 每次更新加1
            progressbarOne['value'] += 1
            # 更新画面
            self.update()
            time.sleep(0.05)
            f1 = - l1 * sin(th1store[iv]) * w1 + l2 * sin(th2store[iv]) * w2 - lcd * sin(th3store[iv]) * w3
            f2 = l1 * cos(th1store[iv]) * w1 + l2 * cos(th2store[iv]) * w2 - lcd * cos(th3store[iv]) * w3
            f3 = l3 * sin(th3store[iv]) * w3 - l4 * sin(th4store[iv]) * w4
            f4 = - l3 * cos(th3store[iv]) * w3 + l4 * cos(th4store[iv]) * w4 - v5
            system = [f1, f2, f3, f4]
            solve_value = solve(system, [w2, w3, w4, v5])
            print(solve_value)
            v5store.append(float(solve_value[v5]))
            w2store.append(float(solve_value[w2]))
            w3store.append(float(solve_value[w3]))
            w4store.append(float(solve_value[w4]))

        self.calculate_a(w1, w2store, w3store, w4store, v5store, th1store, th2store, th3store, th4store, s5store, l1,
                         l2, l3,
                         lcd, l4, angel)

    def calculate_a(self, w1, w2store, w3store, w4store, v5store, th1store, th2store, th3store, th4store, s5store, l1,
                    l2, l3,
                    lcd, l4, angel):#计算加速度，传参数为了保证画图
        self.window_destroy()
        self.label_rade_a = Label(self, text="正在努力计算加速度呀QAQ")
        self.label_rade_a.pack()
        self.wait()
        a2store = []
        a3store = []
        a4store = []
        a5store = []
        a2, a3, a4, a5 = symbols('a2 a3 a4 a5', real=True)
        progressbarOne = ttk.Progressbar(self)
        progressbarOne.pack(pady=20)
        # 进度值最大值
        progressbarOne['maximum'] = (360 / angel)
        # 进度值初始值
        progressbarOne['value'] = 0
        for ia in range(len(th1store)):
            # 每次更新加1
            progressbarOne['value'] += 1
            # 更新画面
            self.update()
            time.sleep(0.05)
            f1 = - l1 * (w1 ** 2) * cos(th1store[ia]) + l2 * (
                    (w2store[ia] ** 2) * cos(th2store[ia]) + a2 * sin(w2store[ia])) - lcd * (
                         (w3store[ia] ** 2) * cos(th3store[ia]) + a3 * sin(th3store[ia]))
            f2 = - l1 * (w1 ** 2) * sin(th1store[ia]) + l2 * (
                    (w2store[ia] ** 2) * -sin(th2store[ia]) + a2 * cos(w2store[ia])) - lcd * (
                         (w3store[ia] ** 2) * -sin(th3store[ia]) + a3 * cos(th3store[ia]))
            f3 = l3 * ((w3store[ia] ** 2) * cos(th3store[ia]) + a3 * sin(th3store[ia])) - l4 * (
                    (w4store[ia] ** 2) * cos(th4store[ia]) + a4 * sin(th4store[ia]))
            f4 = -l3 * ((w3store[ia] ** 2) * -sin(th3store[ia]) + a3 * cos(th3store[ia])) - l4 * (
                    (w4store[ia] ** 2) * -sin(th4store[ia]) + a4 * cos(th4store[ia])) - a5
            system = [f1, f2, f3, f4]
            solve_value = solve(system, [a2, a3, a4, a5])
            print(solve_value)
            a5store.append(float(solve_value[a5]))
            a2store.append(float(solve_value[a2]))
            a3store.append(float(solve_value[a3]))
            a4store.append(float(solve_value[a4]))
        self.pic(th1store, v5store, s5store, a5store, angel)

    def pic(self, th1store, v5store, s5store, a5store, angel):
        self.window_destroy()
        self.label_success = Label(self, text="生成图像如下")
        self.label_success.pack()
        plt.rcParams['font.sans-serif'] = ['SimSun']  # 全局字体，显示中文，宋体，可替换为其他字体
        plt.rcParams['font.size'] = 14  # 全局字号
        plt.rcParams['mathtext.fontset'] = 'stix'  # 用tex公式的形式输入英文和公式，以显示Times New Roman字体
        fonten = FontProperties(fname='C:\Windows\Fonts\Times.ttf',
                                size=12)  # 在其他需要个性化设置字体类型时，使用FontProperties进行设置，此处也可以使用dict,然后在需要时赋值给fontdict
        fx = plt.figure()
        figx1 = plt.subplot(2, 2, 1)
        figv1 = plt.subplot(2, 2, 2)
        figa1 = plt.subplot(2, 2, 3)
        store_time = time.strftime('%Y%m%d%H%M%S')
        th1xstore = []
        for th1x in range(0, 360, int(360 / len(th1store))):
            th1xstore.append(th1x)
        x = th1xstore
        y1 = s5store
        y2 = v5store
        y3 = a5store
        figx1.plot(x, y1)
        figv1.plot(x, y2)
        figa1.plot(x, y3)
        figx1.set_title('滑块的位置分析折线图')
        figx1.set_xlabel('构建1角度(°)')
        figx1.set_ylabel('滑块位置s5(m)')
        figv1.set_title('滑块的速度分析折线图')
        figv1.set_xlabel('构建1角度(°)')
        figv1.set_ylabel('滑块速度v5(m/s)')
        figa1.set_title('滑块的加速度分析折线图')
        figa1.set_xlabel('构建1角度(°)')
        figa1.set_ylabel('滑块加速度a5(m/s**2)')

        fx.tight_layout()
        # 把绘制的图形显示到tkinter窗口上
        self.canvas = FigureCanvasTkAgg(fx, self)
        self.canvas.draw()  # 以前的版本使用show()方法，matplotlib 2.2之后不再推荐show（）用draw代替，但是用show不会报错，会显示警告
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

        # 把matplotlib绘制图形的导航工具栏显示到tkinter窗口上
        toolbar = NavigationToolbar2Tk(self.canvas,
                                       self)  # matplotlib 2.2版本之后推荐使用NavigationToolbar2Tk，若使用NavigationToolbar2TkAgg会警告
        toolbar.update()
        self.canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)
        plt.savefig(f'./{store_time}滑块位置，速度与加速度分析折线图,隔{angel}°取一个点.png')
        self.label_memory_pictures = Label(self, text="图像已自动保存")
        self.label_memory_pictures.pack()
        self.button_rstore_data = Button(self, text="重新开始记录数据", command=self.to_store_data)  # 直接用现有数据计算
        self.button_rstore_data.pack()
        self.button_rto_memory_data = Button(self, text="再次为我展示历史数据，我要计算历史数据", command=self.show_memory_data)  # 可以调用历史数据
        self.button_rto_memory_data.pack()
        self.button_quit = Button(self, text="结束", command=self.quit)
        self.button_quit.pack()


if __name__ == "__main__":
    root = Tk()
    root.title('解析法机构分析程序')
    root.minsize(600, 600)
    main = analpressmecaism(root)
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    ww = 610
    wh = 400
    x = (sw - ww) / 2
    y = (sh - wh) / 2
    root.geometry('%dx%d+%d+%d' % (ww, wh, x, y))
    root.mainloop()
