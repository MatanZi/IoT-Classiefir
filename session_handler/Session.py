from datetime import datetime


class Session:
    def __init__(self, mac1, mac2):
        self.mac1 = mac1
        self.mac2 = mac2
        self.deltaT = [0]
        self.deltaT_mac1 = [0]
        self.deltaT_mac2 = [0]
        self.packets = []
        self.packets_num = 0

    def add(self, packet):
        self.packets.append(packet)
        self.packets_num += 1

    def calc_delta_time(self):
        packets_time = []
        for packet in self.packets:
            packets_time.append(packet.time)
        for i in range (1, len(packets_time) - 1):
            self.deltaT.append((packets_time[i + 1] - packets_time[i]).total_seconds())
            packets_time.append(packet.time)
        for i in range (1, len(packets_time)):
            self.deltaT.append((packets_time[i] - packets_time[i - 1]).total_seconds())
        return self.deltaT

    def calc_delta_time_send_receive(self):
        packets_time_send = []
        packets_time_rec = []
        for packet in self.packets:
            if packet.s_mac == self.mac1:
                packets_time_send.append(packet.time)
            elif packet.d_mac == self.mac1:
                packets_time_rec.append(packet.time)

        for i in range(1, len(packets_time_send)):
            self.deltaT_mac1.append((packets_time_send[i] - packets_time_send[i - 1]).total_seconds())
        for i in range(1, len(packets_time_rec)):
            self.deltaT_mac2.append((packets_time_rec[i] - packets_time_rec[i - 1]).total_seconds())
        return self.deltaT_mac1, self.deltaT_mac2
