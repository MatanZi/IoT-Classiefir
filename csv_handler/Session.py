from datetime import datetime

class Session:
    def __init__(self, mac1, mac2):
        self.mac1 = mac1
        self.mac2 = mac2
        self.deltaT = [0]
        self.packets = []
        self.packets_num = 0

    def add(self, packet):
        self.packets.append(packet)
        self.packets_num += 1

    def calcDeltaTime(self):
        packets_time = []
        for packet in self.packets:
            dt = datetime.strptime(packet.time, '%Y-%m-%d %H:%M:%S.%f')
            packets_time.append(dt)
        for i in range (1, len(packets_time) - 1):
            self.deltaT.append((packets_time[i + 1] - packets_time[i]).total_seconds())