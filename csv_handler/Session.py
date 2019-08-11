import numpy as np

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
            packets_time.append(packet.time)
        for i in range (1, len(packets_time)):
            self.deltaT[i] = packets_time[i + 1] - packets_time[i]