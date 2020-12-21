import _thread
import random
import sys
import threading
import time

from PyQt5 import QtWidgets

import ui.mainDialog as mainDialog
from Queue import Queue

groundFloorQueue = Queue()  # katlardaki asansör kuyrukları
firstFloorQueue = Queue()
secondFloorQueue = Queue()
thirdFloorQueue = Queue()
fourthFloorQueue = Queue()
exitCount = 0  # AVM den çıkan insan sayısı

ui = mainDialog.Ui_MainWindow()


class Group:  # insan sayısını ve hedef katı tuttuğumuz class
    def __init__(self, people, targetFloor):
        self.people = people
        self.targetFloor = targetFloor
        self.next = None


def LoginThread(delay):  # İstenen aralıklarla 1-10 kişi arasındaki bir grup AVM'ye grişi yapacak
    while True:
        people = random.randint(1, 10)  # gidecek insan sayısı
        targetFloor = random.randint(1, 4)  # gidilecek kat
        newGroup = Group(people, targetFloor)  # bu iki bilgiyi bir grup altında toplar
        groundFloorQueue.enque(newGroup)  # ve zemin katın sırasına ekler
        time.sleep(delay)


def ExitThread(delay):  # İstenen aralıklarla 1-5 kişi arasındaki bir grup AVM'den çıkış kuyruğuna girecek

    targetFloor = 0
    while True:
        time.sleep(delay)
        people = random.randint(1, 5)  # gidecek insan sayısı
        floor = random.randint(1, 4)  # kuyruğa eklenecek katı belirler

        if floor == 1:  # gelen random değerlere göre katlardaki çıkış kuyruğuna insan ekler
            firstFloorQueue.enque(Group(people, targetFloor))
        elif floor == 2:
            secondFloorQueue.enque(Group(people, targetFloor))
        elif floor == 3:
            thirdFloorQueue.enque(Group(people, targetFloor))
        elif floor == 4:
            fourthFloorQueue.enque(Group(people, targetFloor))


class ElevatorThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.elevatorCapacity = 10
        self.currentFloor = 0
        self.elevatorQueue = Queue()
        self.active = True
        self.goesUp = True

    def run(self):
        print("1st elevator is running")
        while True:
            getPassenger(self)
            dropPassenger(self)
            time.sleep(0.4)
            move(self)


class ExtraElevatorThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.elevatorCapacity = 10
        self.currentFloor = 0
        self.elevatorQueue = Queue()
        self.active = False
        self.goesUp = True

    def run(self):
        self.active = True
        print("Extra elevator is running")
        while self.active:
            getPassenger(self)
            dropPassenger(self)
            time.sleep(0.4)
            move(self)


def getPassenger(self):  # yolcu alma fonksiyonu

    while True:
        if self.currentFloor == 0 and groundFloorQueue.isEmpty() is False \
                and self.elevatorCapacity - groundFloorQueue.getTop().people >= 0:

            self.elevatorQueue.enque(groundFloorQueue.getTop())
            self.elevatorCapacity -= groundFloorQueue.getTop().people
            groundFloorQueue.deque()

        elif self.currentFloor == 1 and firstFloorQueue.isEmpty() is False \
                and self.elevatorCapacity - firstFloorQueue.getTop().people >= 0:

            self.elevatorQueue.enque(firstFloorQueue.getTop())
            self.elevatorCapacity -= firstFloorQueue.getTop().people
            firstFloorQueue.deque()

        elif self.currentFloor == 2 and secondFloorQueue.isEmpty() is False \
                and self.elevatorCapacity - secondFloorQueue.getTop().people >= 0:

            self.elevatorQueue.enque(secondFloorQueue.getTop())
            self.elevatorCapacity -= secondFloorQueue.getTop().people
            secondFloorQueue.deque()

        elif self.currentFloor == 3 and thirdFloorQueue.isEmpty() is False \
                and self.elevatorCapacity - thirdFloorQueue.getTop().people >= 0:

            self.elevatorQueue.enque(thirdFloorQueue.getTop())
            self.elevatorCapacity -= thirdFloorQueue.getTop().people
            thirdFloorQueue.deque()

        elif self.currentFloor == 4 and fourthFloorQueue.isEmpty() is False \
                and self.elevatorCapacity - fourthFloorQueue.getTop().people >= 0:

            self.elevatorQueue.enque(fourthFloorQueue.getTop())
            self.elevatorCapacity -= fourthFloorQueue.getTop().people
            fourthFloorQueue.deque()
        else:
            break


def dropPassenger(self):  # yolcu bırakma fonskiyonu
    global exitCount

    while self.elevatorQueue.isEmpty() is False and self.elevatorQueue.getTop().targetFloor is self.currentFloor:
        if self.currentFloor == 0:
            exitCount += self.elevatorQueue.getTop().people
            self.elevatorCapacity += self.elevatorQueue.getTop().people
            self.elevatorQueue.deque()
        else:
            self.elevatorCapacity += self.elevatorQueue.getTop().people
            self.elevatorQueue.deque()


def move(self):  # asansör hareketi
    if self.goesUp:
        self.currentFloor += 1
    else:
        self.currentFloor -= 1

    if self.currentFloor == 4:
        self.goesUp = False

    if self.currentFloor == 0:
        self.goesUp = True


elevator1 = ElevatorThread()
elevator2 = ExtraElevatorThread()
elevator3 = ExtraElevatorThread()
elevator4 = ExtraElevatorThread()
elevator5 = ExtraElevatorThread()


def ControlThread(num):
    global elevator2, elevator3, elevator4, elevator5
    while True:
        totalQueue = groundFloorQueue.getPeopleCount() + firstFloorQueue.getPeopleCount() \
                     + secondFloorQueue.getPeopleCount() + thirdFloorQueue.getPeopleCount() \
                     + fourthFloorQueue.getPeopleCount()

        if totalQueue > 20 and elevator2.active is False:
            elevator2.start()
        elif totalQueue < 10:
            elevator2.active = False
            elevator2 = ExtraElevatorThread()

        if totalQueue > 40 and elevator3.active is False:
            elevator3.start()
        elif totalQueue < 20:
            elevator3.active = False
            elevator3 = ExtraElevatorThread()

        if totalQueue > 60 and elevator4.active is False:
            elevator4.start()
        elif totalQueue < 40:
            elevator4.active = False
            elevator4 = ExtraElevatorThread()

        if totalQueue > 80 and elevator5.active is False:
            elevator5.start()
        elif totalQueue < 60:
            elevator5.active = False
            elevator5 = ExtraElevatorThread()


def terminal():
    print(
        f"0.floor: {groundFloorQueue.getPeopleCount()} people in {groundFloorQueue.getGroupCount()} groups  => {groundFloorQueue.display()}\n "
        f"1.floor: {firstFloorQueue.getPeopleCount()} people in {firstFloorQueue.getGroupCount()} groups  => {firstFloorQueue.display()}\n"
        f"2.floor: {secondFloorQueue.getPeopleCount()} people in {secondFloorQueue.getGroupCount()} groups  => {secondFloorQueue.display()}\n"
        f"3.floor: {thirdFloorQueue.getPeopleCount()} people in {thirdFloorQueue.getGroupCount()} groups  => {thirdFloorQueue.display()}\n"
        f"4.floor: {fourthFloorQueue.getPeopleCount()} people in {fourthFloorQueue.getGroupCount()} groups  => {fourthFloorQueue.display()}\n"
        f"Exit Count: {exitCount}\n"
        "Elevator 1\n"
        f"active: {str(elevator1.active)} , capacity: {elevator1.elevatorCapacity}, floor: {elevator1.currentFloor}\n"
        f"inside: {elevator1.elevatorQueue.display()}\n"
        "Elevator 2\n"
        f"active: {str(elevator2.active)} , capacity: {elevator2.elevatorCapacity}, floor: {elevator2.currentFloor}\n"
        f"inside: {elevator2.elevatorQueue.display()}\n"
        "Elevator 3\n"
        f"active: {str(elevator3.active)} , capacity: {elevator3.elevatorCapacity}, floor: {elevator3.currentFloor}\n"
        f"inside: {elevator3.elevatorQueue.display()}\n"
        "Elevator 4\n"
        f"active: {str(elevator4.active)} , capacity: {elevator4.elevatorCapacity}, floor: {elevator4.currentFloor}\n"
        f"inside: {elevator4.elevatorQueue.display()}\n"
        "Elevator 5\n"
        f"active: {str(elevator5.active)} , capacity: {elevator5.elevatorCapacity}, floor: {elevator5.currentFloor}\n"
        f"inside: {elevator5.elevatorQueue.display()}\n"
        f"-------------------------------------------------------------------------------------------------------\n")


def gui():
    ui.f01.setText(str(groundFloorQueue.getPeopleCount()))
    ui.f03.setText(str(groundFloorQueue.getGroupCount()))
    ui.f0g.setText(groundFloorQueue.display())

    ui.f11.setText(str(firstFloorQueue.getPeopleCount()))
    ui.f13.setText(str(firstFloorQueue.getGroupCount()))
    ui.f1g.setText(firstFloorQueue.display())

    ui.f21.setText(str(secondFloorQueue.getPeopleCount()))
    ui.f23.setText(str(secondFloorQueue.getGroupCount()))
    ui.f2g.setText(secondFloorQueue.display())

    ui.f31.setText(str(thirdFloorQueue.getPeopleCount()))
    ui.f33.setText(str(thirdFloorQueue.getGroupCount()))
    ui.f3g.setText(thirdFloorQueue.display())

    ui.f41.setText(str(fourthFloorQueue.getPeopleCount()))
    ui.f43.setText(str(fourthFloorQueue.getGroupCount()))
    ui.f4g.setText(fourthFloorQueue.display())

    ui.active1.setText(str(elevator1.active))
    ui.capaticy1.setText(str(elevator1.elevatorCapacity))
    ui.floor1.setText(str(elevator1.currentFloor))
    ui.inside1.setText(elevator1.elevatorQueue.display())

    ui.active2.setText(str(elevator2.active))
    ui.capaticy2.setText(str(elevator2.elevatorCapacity))
    ui.floor2.setText(str(elevator2.currentFloor))
    ui.inside2.setText(elevator2.elevatorQueue.display())

    ui.active3.setText(str(elevator3.active))
    ui.capaticy3.setText(str(elevator3.elevatorCapacity))
    ui.floor3.setText(str(elevator3.currentFloor))
    ui.inside3.setText(elevator3.elevatorQueue.display())

    ui.active4.setText(str(elevator4.active))
    ui.capaticy4.setText(str(elevator4.elevatorCapacity))
    ui.floor4.setText(str(elevator4.currentFloor))
    ui.inside4.setText(elevator4.elevatorQueue.display())

    ui.active5.setText(str(elevator5.active))
    ui.capaticy5.setText(str(elevator5.elevatorCapacity))
    ui.floor5.setText(str(elevator5.currentFloor))
    ui.inside5.setText(elevator5.elevatorQueue.display())

    ui.exitCount.setText(str(exitCount))


def display(delay):

    while True:
        gui()
        # terminal()
        time.sleep(delay)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()

    _thread.start_new_thread(display, (0.4,))          #verileri arayüz ya da terminal üzerinden yazdıran thread
    _thread.start_new_thread(LoginThread, (1,))
    elevator1.start()
    _thread.start_new_thread(ControlThread, (0.01,))
    _thread.start_new_thread(ExitThread, (2,))

    while 1:
        sys.exit(app.exec_())
        pass
