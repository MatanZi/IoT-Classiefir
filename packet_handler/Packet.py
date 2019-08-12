from datetime import datetime

import pandas as pd


class Packet(object):
    def __init__(self, id, time, s_mac, d_mac, s_ip , d_ip, s_port, d_port, protocol):
        self.id = id
        self.time = datetime.strptime(time, '%d/%m/%Y %H:%M:%S.%f')
        self.s_mac = s_mac
        self.d_mac = d_mac
        self.s_ip = s_ip
        self.d_ip = d_ip
        self.s_port = int(s_port)
        self.d_port = int(d_port)
        self.protocol = protocol


def build_packets(csv_file):
    id = 1
    packets_list = []
    for name, row in csv_file.iterrows():
        print(row['_ws.col.AbsTime'])
        if pd.notnull(row['tcp.srcport']):
            packet = Packet(id, row['_ws.col.AbsTime'], row['wlan.sa'], row['wlan.da'], row['ip.src'], row['ip.dst'],
                            row['tcp.srcport'], row['tcp.dstport'], "TCP")
        else:
            packet = Packet(id, row['_ws.col.AbsTime'], row['wlan.sa'], row['wlan.da'], row['ip.src'], row['ip.dst'],
                            row['udp.srcport'], row['udp.dstport'], "UDP")
        packets_list.append(packet)

    return packets_list


i = pd.read_csv("filter_IP.csv", error_bad_lines=False, warn_bad_lines=False)
d = build_packets(i)

print(d[0].time)
