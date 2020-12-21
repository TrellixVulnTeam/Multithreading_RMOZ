class Queue:  # katlardaki kuyruk yönetimi için oluşturduğumuz class
    def __init__(self):
        self.head = None  # kuyruğun başı
        self.tail = None  # kuyruğun sonu
        self.peopleCount = 0
        self.groupCount = 0
        self.info = ""

    def enque(self, group):  # kuyruğa grup ekle
        if self.head is None:
            self.head = group
            self.tail = self.head
            self.peopleCount += group.people  # kuyruktaki insan sayısını artırır
            self.groupCount += 1  # kuyruktaki grup sayısını artırır
        else:
            self.tail.next = group
            self.tail = self.tail.next
            self.peopleCount += group.people  # kuyruktaki insan sayısını artırır
            self.groupCount += 1  # kuyruktaki grup sayısını artırır

    def deque(self):  # kuyruktan grup sil
        groupSize = 0

        if self.head is None:
            print("Empty queue")
        elif self.head.next is not None:
            self.peopleCount -= self.head.people  # kuyruktaki insan sayısını azaltır
            groupSize = self.head.people  # updated
            self.head = self.head.next
            self.groupCount -= 1  # kuyruktaki grup sayısını azaltır
        else:
            self.peopleCount -= self.head.people  # kuyruktaki insan sayısını azaltır
            groupSize = self.head.people  # updated
            self.head = None
            self.groupCount -= 1  # kuyruktaki grup sayısını azaltır

        return groupSize

    def display(self):  # kuyruktaki grupları yazdırır
        groups = " "
        it = self.head
        while it is not None:
            groups += f"[{it.people},{it.targetFloor}], "
            it = it.next
        return groups

    def getTop(self):
        return self.head

    def isEmpty(self):
        return self.head is None

    def getPeopleCount(self):
        return self.peopleCount

    def getGroupCount(self):
        return self.groupCount
