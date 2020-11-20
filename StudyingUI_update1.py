from PyQt5.QtWidgets import (QWidget, QPushButton, QLabel, QComboBox, QDesktopWidget)
from PyQt5.QtGui import (QPainter, QPen, QFont)
from PyQt5.QtCore import Qt



class LearningUI(QWidget):
    def __init__(self):
        super(LearningUI, self).__init__()

        self.__init_ui()

        #设置只有鼠标按下时才跟踪移动，否则不按的时候也在画画
        self.setMouseTracking(False)
        #self.pos_xy保存所有绘画的点（要想将按住鼠标后移动的轨迹保留在窗体上，需要一个列表来保存所有移动过的点）
        self.pos_xy = []
        #设置pos_x、pos_y专门存放x、y轴坐标，方便计算
        self.pos_x = []
        self.pos_y = []

        #设置关联事件（学习、识别、清屏），连接到槽函数
        self.btn_learn.clicked.connect(self.btn_learn_on_clicked)
        self.btn_recognize.clicked.connect(self.btn_recognize_on_clicked)
        self.btn_clear.clicked.connect(self.btn_clear_on_clicked)

        #连接到自定义槽函数btn_add_on_clicked
        self.btn_add.clicked.connect(self.btn_add_on_clicked)
        self.btn_minus.clicked.connect(self.btn_minus_on_clicked)
        self.btn_mulitiplication.clicked.connect(self.btn_mulitiplication_on_clicked)
        self.btn_division.clicked.connect(self.btn_division_on_clicked)
        self.btn_equal.clicked.connect(self.btn_equal_on_clicked)
        self.btn_delete.clicked.connect(self.btn_delete_on_clicked)
        self.btn_c.clicked.connect(self.btn_c_on_clicked)

    def __init_ui(self):
        '''
        定义UI界面：
        三个按钮：学习、识别、清屏
        btn_learn、btn_recognize、btn_clear
        一个组合框：选择0-9
        combo_table
        两条标签：请在屏幕空白处用鼠标输入0-9中的某一个数字进行识别！
        2017/10/10 by PyLearn
        一条输出识别结果的标签
        label_output
        '''

        #添加三个按钮，分别是学习、识别、清屏
        self.btn_learn = QPushButton("学习", self)
        '''
        setGeometry()方法做两个事。它定位了窗口在屏幕的位置并且设定窗口大小。前两个参数是窗口的x,y坐标。第三个参数是窗口宽度，第四个是窗口高度。
        '''
        self.btn_learn.setGeometry(50, 400, 70, 40)
        self.btn_recognize = QPushButton("识别", self)
        self.btn_recognize.setGeometry(320, 400, 70, 40)
        self.btn_clear = QPushButton("清屏", self)
        self.btn_clear.setGeometry(420, 400, 70, 40)

        '''
        添加+、-、*、/、=、Delete、C按钮
        '''
        self.btn_add= QPushButton("+", self)
        self.btn_add.setGeometry(0, 100, 70, 40)

        self.btn_minus = QPushButton("-", self)
        self.btn_minus.setGeometry(0, 180, 70, 40)

        self.btn_mulitiplication = QPushButton("x", self)
        self.btn_mulitiplication.setGeometry(0, 260, 70, 40)

        self.btn_division = QPushButton("÷", self)
        self.btn_division.setGeometry(0, 340, 70, 40)

        self.btn_equal = QPushButton("=", self)
        self.btn_equal.setGeometry(80, 100, 70, 40)

        self.btn_delete = QPushButton("Delete", self)
        self.btn_delete.setGeometry(450, 100, 70, 40)

        self.btn_c=QPushButton("C",self)
        self.btn_c.setGeometry(370,100,70,40)

        #添加一个组合框，选择0-9
        self.combo_table = QComboBox(self)
        for i in range(10):
            self.combo_table.addItem("%d" % i)
        self.combo_table.setGeometry(150, 400, 70, 40)

        #添加一条标签
        #self.label_head = QLabel('请在屏幕空白处用鼠标输入0-9中的某一个数字进行识别！', self)
        #self.label_head.move(75, 50)
        self.label_end = QLabel('by 憨憨小分队', self)
        self.label_end.move(375, 470)

        #添加一条输出识别结果的标签
        self.label_output = QLabel('', self)
        #设定窗口大小（x坐标，y坐标，宽度，高度）
        self.label_output.setGeometry(0, 50,550 , 50)
        #设置边框大小、颜色
        self.label_output.setStyleSheet("QLabel{border:5px solid black;}")
        #设置字体类型、大小、加粗
        self.label_output.setFont(QFont("Roman times", 10, QFont.Bold))
        #设置文本居中
        self.label_output.setAlignment(Qt.AlignCenter)


        '''
        setFixedSize()固定了窗体的宽度与高度
        self.center()将窗体居中显示
        setWindowTitle()设置窗体的标题
        '''
        self.setFixedSize(550, 500)
        self.center()
        self.setWindowTitle('0-9手写体识别(机器学习中的"HelloWorld!")')


    def center(self):
        '''
        窗口居中显示
        '''

        #在主窗口内得到一个指定的长方形几何体
        qt_center = self.frameGeometry()
        '''
        QDesktopWidget类提供了关于用户桌面的信息，包括屏幕尺寸
        '''
        #获取显示器的中心点
        desktop_center = QDesktopWidget().availableGeometry().center()
        #我们的长方形窗口已经有了宽度和高度，现在我们设定它的中心在屏幕中心。它的大小不变。
        qt_center.moveCenter(desktop_center)
        #我们移动应用窗口的左上点到长方形的左上角，至此我们就将窗口移动到了中央。
        self.move(qt_center.topLeft())

    def paintEvent(self, event):
        '''
        首先判断pos_xy列表中是不是至少有两个点了
        然后将pos_xy中第一个点赋值给point_start
        利用中间变量pos_tmp遍历整个pos_xy列表
        point_end = pos_tmp

        判断point_end是否是断点，如果是
        point_start赋值为断点
        continue
        判断point_start是否是断点，如果是
        point_start赋值为point_end
        continue

        画point_start到point_end之间的线
        point_start = point_end
        这样，不断地将相邻两个点之间画线，就能留下鼠标移动轨迹了
        '''

        painter = QPainter()
        painter.begin(self)
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        painter.setPen(pen)

        #至少两个点
        if len(self.pos_xy) > 1:
            #起点
            point_start = self.pos_xy[0]
            #遍历鼠标经过的点，找到终点
            for pos_tmp in self.pos_xy:
                point_end = pos_tmp

                #判断断点
                if point_end == (-1, -1):
                    point_start = point_end
                    continue

                if point_start == (-1, -1):
                    point_start = point_end
                    continue

                #绘制一条制定了断点坐标的线，绘制从(start[0],start[1])到(end[0],end[1])的直线并且设置当前画笔的位置为end那里
                painter.drawLine(point_start[0], point_start[1], point_end[0], point_end[1])
                point_start = point_end
        painter.end()

    def mouseReleaseEvent(self, event):
        '''
        重写鼠标按住后松开的事件
        在每次松开后向pos_xy列表中添加一个断点(-1, -1)
        然后在绘画时判断一下是不是断点就行了
        是断点的话就跳过去，不与之前的连续
        '''

        pos_test = (-1, -1)
        self.pos_xy.append(pos_test)

        self.update()

    #获得鼠标移动过的点的坐标，并存入数组
    def mouseMoveEvent(self, event):

        self.pos_x.append(event.pos().x())
        self.pos_y.append(event.pos().y())

        #中间变量pos_tmp提取当前点
        pos_tmp = (event.pos().x(), event.pos().y())
        #pos_tmp添加到self.pos_xy中
        self.pos_xy.append(pos_tmp)

        self.update()

    def btn_learn_on_clicked(self):
        '''
        需要用到数据库，因此在在子类中实现
        '''

        '''
        pass 是空语句，是为了保持程序结构的完整性。
        pass 不做任何事情，一般用做占位语句。
        '''
    pass

    def btn_recognize_on_clicked(self):
        '''
        需要用到数据库，因此在在子类中实现
        '''

    pass

    #清屏函数
    def btn_clear_on_clicked(self):
        '''
        按下清屏按钮：
        将列表赋值为空
        将输出识别结果的标签赋值为空
        然后刷新界面，重新绘画即可清屏
        '''

        self.pos_xy = []
        self.pos_x = []
        self.pos_y = []
        #self.label_output.setText('')
        self.update()

    #自定义槽函数
    def btn_add_on_clicked(self):
        content=self.label_output.text()
        self.label_output.setText("%s+"%content)

    def btn_minus_on_clicked(self):
        content=self.label_output.text()
        self.label_output.setText("%s-"%content)

    def btn_mulitiplication_on_clicked(self):
        content=self.label_output.text()
        self.label_output.setText("%s×"%content)

    def btn_division_on_clicked(self):
        content=self.label_output.text()
        self.label_output.setText("%s÷"%content)

    def btn_equal_on_clicked(self):
        content = self.label_output.text()
        str=''
        for e in content:
            if e =='×':
                str=str+'*'
            elif e == '÷':
                str=str+'/'
            else:
                str=str+e
        result=eval(str)
        self.label_output.setText("%s=%d" % (content,result))

    def btn_delete_on_clicked(self):
        content = self.label_output.text()
        content_str=content
        if '=' in content:
            content=''
            for e in content_str:
                if e !='=':
                    content = content+e
                else:
                    break
        else:
            content=content[0:len(content)-1]
        self.label_output.setText("%s" % content)

    def btn_c_on_clicked(self):
        self.label_output.setText('')

    def get_pos_xy(self):
        '''
        将手写体在平面上分为9个格子
        计算每个格子里点的数量
        然后点的数量转化为占总点数的百分比
        接着返回一个数组dim[9]
        横轴依次是min_x、min2_x、max2_x、max_x
        纵轴依次是min_y、min2_y、max2_y、max_y
        '''

        if not self.pos_xy:
            return None

        pos_count = len(self.pos_x)
        max_x = max(self.pos_x)
        max_y = max(self.pos_y)
        min_x = min(self.pos_x)
        min_y = min(self.pos_y)
        dim = [0, 0, 0, 0, 0, 0, 0, 0, 0]

        dis_x = (max_x - min_x) // 3
        dis_y = (max_y - min_y) // 3

        min2_x = min_x + dis_x
        min2_y = min_y + dis_y
        max2_x = max_x - dis_x
        max2_y = max_y - dis_y

        for i in range(len(self.pos_x)):
            if self.pos_y[i] >= min_y and self.pos_y[i] < min2_y:
                if self.pos_x[i] >= min_x and self.pos_x[i] < min2_x:
                    dim[0] += 1
                    continue
            if self.pos_x[i] >= min2_x and self.pos_x[i] < max2_x:
                dim[1] += 1
                continue
            if self.pos_x[i] >= max2_x and self.pos_x[i] <= max_x:
                dim[2] += 1
                continue
            elif self.pos_y[i] >= min2_y and self.pos_y[i] < max2_y:
                if self.pos_x[i] >= min_x and self.pos_x[i] < min2_x:
                    dim[3] += 1
                    continue
            if self.pos_x[i] >= min2_x and self.pos_x[i] < max2_x:
                dim[4] += 1
                continue
            if self.pos_x[i] >= max2_x and self.pos_x[i] <= max_x:
                dim[5] += 1
                continue
            elif self.pos_y[i] >= max2_y and self.pos_y[i] <= max_y:
                if self.pos_x[i] >= min_x and self.pos_x[i] < min2_x:
                    dim[6] += 1
                    continue
            if self.pos_x[i] >= min2_x and self.pos_x[i] < max2_x:
                dim[7] += 1
                continue
            if self.pos_x[i] >= max2_x and self.pos_x[i] <= max_x:
                dim[8] += 1
                continue
            else:
                pos_count -= 1
            continue
        #将数量转化为所占百分比
        for num in dim:
            num = num * 100 // pos_count

        return dim

