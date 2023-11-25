import sys
import threading
from PySide6.QtWidgets import QApplication, QPushButton
from pade.acl.aid import AID
from pade.behaviours.protocols import TimedBehaviour
from pade.misc.utility import start_loop 
from botagent import BotAgent
from pade.core.agent import Agent
from cleaning_area import CleaningArea
from globals import Global
from gui import Gui


class MyTimedBehaviour(TimedBehaviour):
    def __init__(self, agent, time):
        super(MyTimedBehaviour, self).__init__(agent, time)
        self.agent = agent

    def on_time(self):
        super(MyTimedBehaviour, self).on_time()
        # display_message(self.agent.aid.localname, 'Updating the cleaning_boties!')
        for cleaning_bot in self.agent.cleaning_bot_list:
            # print("checking",cleaning_bot.x," ",cleaning_bot.y)
            if(self.agent.map.map[cleaning_bot.x][cleaning_bot.y]):
                cleaning_bot.cleaning=1
                # print("cleaning: ",self.agent.map.map[cleaning_bot.x][cleaning_bot.y],"\n")
                cleaned=min(self.agent.map.map[cleaning_bot.x][cleaning_bot.y], cleaning_bot.power)
                self.agent.map.map[cleaning_bot.x][cleaning_bot.y]-=cleaned
                # print("cleaned: ",cleaning_bot.power )
                self.agent.map.dirtiness-=cleaned
            else:
                cleaning_bot.cleaning=0
            cleaning_bot.updateStatus()
            cleaning_bot.move()

        gui.update()

class YourTimedBehaviour(TimedBehaviour):
    def __init__(self, agent, time):
        super(YourTimedBehaviour, self).__init__(agent, time)
        self.agent = agent

    def on_time(self):
        super(YourTimedBehaviour, self).on_time()
        # print("dirtiness: ", self.agent.map.dirtiness)
        prog=round((1-self.agent.map.dirtiness/self.agent.map.initial_dirtiness)*100,2)
        self.agent.map.progress=prog
        print("clean %: ", prog," %")

class HostAgent(Agent):
    gui= None
    num_cleaning_botes = 50
    cleaning_bot_list = []
    map= CleaningArea()
    enabled = False

    def __init__(self, aid):
        super(HostAgent, 
              self).__init__(aid=aid, debug=False)

        Global.x_center = 0

        for _ in range(self.num_cleaning_botes):
            self.cleaning_bot_list.append(BotAgent())
            # TODO name it and launch it as an agent of chaos

        mytimed = MyTimedBehaviour(self, .2)
        yourtimed = YourTimedBehaviour(self, 2)
        self.behaviours.append(mytimed)
        self.behaviours.append(yourtimed)

def agentsexec():
    start_loop(agents)

def exit_program(x):
    global stop_event
    stop_event.set()
    app.quit()
    
if __name__ == '__main__':
    agents = list()
    port = int(sys.argv[1])
    host_agent_name = 'host_agent_{}@localhost:{}'.format(port+1, port+1)
    host_agent = HostAgent(AID(name=host_agent_name))
    agents.append(host_agent)


    stop_event = threading.Event()

    x = threading.Thread(target=agentsexec)
    x.start()
    app = QApplication([])
    gui = Gui(host_agent)
    gui.show()
    app.exec()
    gui.exit_button.clicked.connect(exit_program(x))
    x.join()
   
#run string
#python D:\Documentos\Universidad\2023-2\Topicos\cs_topics-main\week12pade\TA3\hostagent.py 8000