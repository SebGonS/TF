from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPaintEvent, QPainter,QImage
from PySide6.QtWidgets import QFrame, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QLabel
# from PIL import Image


class Gui(QFrame):
    def __init__(self, agent) -> None:
        super(Gui, self).__init__()
        self.agent = agent
        
        # self.setMinimumSize(900, 900)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)


        #Botones
        self.exit_button= QPushButton('Exit')
        self.exit_button.clicked.connect(self.exit_program)
        self.exit_button.setMaximumSize(100, 50)  

        #Metricas
        self.progress = QLabel("Total Progress: 0 %")
        self.brandA = QLabel("Marca A")
        self.botsA = QLabel("Bots: ")
        self.progressA = QLabel("Progress: ")
        self.brandB = QLabel("Marca B")
        self.botsB = QLabel("Bots: ")
        self.progressB = QLabel("Progress B: ")
        self.brandC = QLabel("Marca C")
        self.botsC=QLabel("Bots: ")
        self.progressC = QLabel("Progress: ")


        # Layout 
        main=QHBoxLayout()
        sidebar=QVBoxLayout()
        aTags=QVBoxLayout()
        bTags=QVBoxLayout()
        cTags=QVBoxLayout()
        sim_area = QVBoxLayout()
        sidebar.setSpacing(10)
        sidebar.addWidget(self.exit_button, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)  # Center the button
        sidebar.addWidget(self.progress,alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)

        aTags.setSpacing(5)
        aTags.addWidget(self.brandA,alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)
        aTags.addWidget(self.botsA,alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)
        aTags.addWidget(self.progressA,alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)

        bTags.setSpacing(5)
        bTags.addWidget(self.brandB,alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)
        bTags.addWidget(self.botsB,alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)
        bTags.addWidget(self.progressB,alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)
        
        cTags.setSpacing(5)
        cTags.addWidget(self.brandC,alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)
        cTags.addWidget(self.botsC,alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)
        cTags.addWidget(self.progressC,alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)

        
        sidebar.addLayout(aTags)
        sidebar.addLayout(bTags)
        sidebar.addLayout(cTags)
        # sim_area.addSpacing(self.agent.map.width)
        main.addLayout(sim_area)
        main.addLayout(sidebar)

        self.set_bot_counts(agent.count_a,agent.count_b,agent.count_c)

        self.resize(200+agent.map.width*agent.map.cell_size,200 + agent.map.height*agent.map.cell_size)  # (x, y, width, height)
        self.setLayout(main)

    def get_floor_color(self, dirtiness): 
        if dirtiness == 0:
            return QColor(255, 255, 255)  # Blanco para area limpia y distintas escalas de gris hasta negro para los siguientes niveles de suciedad
        elif dirtiness == 1:
            return QColor(200, 200, 200) 
        elif dirtiness == 2:
            return QColor(150, 150, 150) 
        elif dirtiness == 3:
            return QColor(100, 100, 100) 
        elif dirtiness == 4:
            return QColor(50, 50, 50)    
        else:
            return QColor(0, 0, 0)
        
    def update_progress(self,p):
        self.progress.setText(f"Total Progress: {p} %")
    def update_progressA(self,p):
        self.progressA.setText(f"Progress: {p} %")
    def update_progressB(self,p):
        self.progressB.setText(f"Progress: {p} %")
    def update_progressC(self,p):
        self.progressC.setText(f"Progress: {p} %")
    def set_bot_counts(self,a,b,c):
       self.botsA.setText(f"Bots: {a}")
       self.botsB.setText(f"Bots: {b}")
       self.botsC.setText(f"Bots: {c}")

    def paintEvent(self, _: QPaintEvent) -> None:
        painter = QPainter(self)
        for i in range(self.agent.map.height):
            for j in range(self.agent.map.width):
                dirtiness = self.agent.map.map[i][j]
                color = self.get_floor_color(dirtiness)
                painter.fillRect(j * self.agent.map.cell_size, i * self.agent.map.cell_size, self.agent.map.cell_size, self.agent.map.cell_size, color)
                # painter.drawRect(j * self.agent.map.cell_size, i * self.agent.map.cell_size, self.agent.map.cell_size, self.agent.map.cell_size)

        for cleaning_bot in self.agent.cleaning_bot_list:
            #    print(cleaning_bot.x, cleaning_bot.y)
            painter.fillRect(cleaning_bot.x*cleaning_bot.size, cleaning_bot.y*cleaning_bot.size, cleaning_bot.size, cleaning_bot.size, cleaning_bot.color)
            painter.drawRect(cleaning_bot.x*cleaning_bot.size, cleaning_bot.y*cleaning_bot.size, cleaning_bot.size, cleaning_bot.size)
        self.update_progress(self.agent.map.progress)
        self.update_progressA(round(self.agent.a_progress/self.agent.map.initial_dirtiness*100,2))
        self.update_progressB(round(self.agent.b_progress/self.agent.map.initial_dirtiness*100,2))
        self.update_progressC(round(self.agent.c_progress/self.agent.map.initial_dirtiness*100,2))

    # def set_size(self,w,h):
    #     self.main.resize(w,h)
   

        
    def exit_program(self):
        #self.agent
        self.close()
