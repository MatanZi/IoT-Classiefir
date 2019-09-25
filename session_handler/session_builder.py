from session_handler.Session import Session
from packet_handler import Packet
import numpy as np
import pandas as pd


def get_iot_label(address):
    if address == "192.168.1.150" or address == "98:fc:11:a1:f7:0f":
        return "Camera 1"
    elif address == "192.168.1.151" or address == "6c:fd:b9:4f:70:0b": #"192.168.0.5"
        return "Camera 2"
    elif address == "192.168.0.104" or address == "00:17:88:77:35:80": #"192.168.0.104"
        return "Smart bulb"
    elif address == "192.168.1.111" or address == "fc:6b:f0:0a:c3:43": #"192.168.0.179"
        return "Smart doorbell"


def get_non_iot_label(address):
    if address == "192.168.1.150" or address == "98:fc:11:a1:f7:0f":
        return "IoT"
    elif address == "192.168.1.151" or address == "6c:fd:b9:4f:70:0b":
        return "IoT"
    elif address == "192.168.1.119" or address == "00:17:88:77:35:80":
        return "IoT"
    elif address == "192.168.1.111" or address == "fc:6b:f0:0a:c3:43":
        return "IoT"
    else:
        return "Non-IoT"


def build_sessions_df(df, ip):
    sessions = {}
    label = get_iot_label(ip)
    session_packets = df.loc[(df['ip.src'] == ip) | (df['ip.dst'] == ip), :]
    for i, row in session_packets.iterrows():
        # check if the packet belongs to a known session, if it does, add the packet to it's session
        # (filtering by other ip)
        if row['ip.src'] == ip:
            if row['ip.dst'] in sessions.keys():
                packet = Packet.create_packet(row)
                sessions[packet.d_ip].add(packet)
            else:
                new_session = Session(ip, row['ip.dst'], label)
                packet = Packet.create_packet(row)
                new_session.add(packet)
                sessions[packet.d_ip] = new_session
        elif row['ip.dst'] == ip:
            if row['ip.src'] in sessions.keys():
                packet = Packet.create_packet(row)
                sessions[packet.s_ip].add(packet)
            else:
                new_session = Session(ip, row['ip.src'], label)
                packet = Packet.create_packet(row)
                new_session.add(packet)
                sessions[packet.s_ip] = new_session
    return sessions


'''
    packets_sent = session_packets.loc[session_packets['ip.src'] == ip]
    packets_rec = session_packets.loc[session_packets['ip.dst'] == ip]
    sent_ip_list = packets_sent['ip.dst'].values.tolist()
    rec_ip_list = packets_rec['ip.src'].values.tolist()

    merged_ip_list = list(sent_ip_list)
    merged_ip_list.extend(x for x in rec_ip_list if x not in merged_ip_list)

    for ip in merged_ip_list:
        packets_list = session_packets.loc[(session_packets['ip.src'] == ip) | (session_packets['ip.dst'] == ip), :].values.tolist()
        print(packets_list[0])


'''


def build_sessions(packet_list, ip, classby=''):
    sessions = {}
    if classby == 'noniot':
        label = get_non_iot_label(ip)
    else:
        label = get_iot_label(ip)
    for packet in packet_list:
        # check if the packet belongs to a known session, if it does, add the packet to it's session
        # (filtering by other ip)
        if packet.s_ip == ip:
            if packet.d_ip in sessions.keys():
                sessions[packet.d_ip].add(packet)
            else:
                new_session = Session(ip, packet.d_ip, label)
                new_session.add(packet)
                sessions[packet.d_ip] = new_session
        elif packet.d_ip == ip:
            if packet.s_ip in sessions.keys():
                sessions[packet.s_ip].add(packet)
            else:
                new_session = Session(ip, packet.s_ip, label)
                new_session.add(packet)
                sessions[packet.s_ip] = new_session
    return sessions
