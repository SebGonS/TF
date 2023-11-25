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
        self.progress = QLabel("Progress: 0 %")
        self.brandA = QLabel("Marca A")
        self.brandB = QLabel("Marca B")
        self.brandC = QLabel("Marca C")

        # Layout 
        main=QHBoxLayout()
        sidebar=QVBoxLayout()
        sim_area = QVBoxLayout()
        sidebar.addWidget(self.exit_button, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)  # Center the button
        sidebar.addWidget(self.progress,alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)
        sidebar.addWidget(self.brandA,alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)
        sidebar.addWidget(self.brandB,alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)
        sidebar.addWidget(self.brandC,alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)


        # sim_area.addSpacing(self.agent.map.width)
        main.addLayout(sim_area)
        main.addLayout(sidebar)


        self.resize(agent.map.width,agent.map.height)  # (x, y, width, height)
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
        self.progress.setText(f"Progress: {p} %")
    def update_BrandA(self,p):
        self.brandA.setText(f"Marca A: {p} %")
    def update_BrandB(self,p):
        self.brandB.setText(f"Marca B: {p} %")
    def update_BrandC(self,p):
        self.brandC.setText(f"Marca C: {p} %")

    def paintEvent(self, _: QPaintEvent) -> None:
        painter = QPainter(self)
        for i in range(self.agent.map.height):
            for j in range(self.agent.map.width):
                dirtiness = self.agent.map.map[i][j]
                color = self.get_floor_color(dirtiness)
                painter.fillRect(j * self.agent.map.cell_size, i * self.agent.map.cell_size, self.agent.map.cell_size, self.agent.map.cell_size, color)

        for cleaning_bot in self.agent.cleaning_bot_list:
            #    print(cleaning_bot.x, cleaning_bot.y)
            painter.fillRect(cleaning_bot.x*cleaning_bot.size, cleaning_bot.y*cleaning_bot.size, cleaning_bot.size, cleaning_bot.size, cleaning_bot.color)
        self.update_progress(self.agent.map.progress)

    # def set_size(self,w,h):
    #     self.main.resize(w,h)
   

        
    def exit_program(self):
        #self.agent
        self.close()
