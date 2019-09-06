from session_handler.Session import Session
import numpy as np


def get_label(address):
    if address == "192.168.1.150" or address == "98:fc:11:a1:f7:0f":
        return "Camera 1" # Camera 1
    elif address == "192.168.1.151" or address == "6c:fd:b9:4f:70:0b":
        return "Camera 2" # Camera 2
    elif address == "192.168.1.119" or address == "00:17:88:77:35:80":
        return "Smart bulb" # Smart bulb
    elif address == "192.168.1.111" or address == "fc:6b:f0:0a:c3:43":
        return "Smart doorbell" # Smart doorbell


def build_sessions(packet_list, ip):
    sessions = {}
    for packet in packet_list:
        # check if the packet belongs to a known session, if it does, add the packet to it's session
        # (filtering by other ip)
        label = get_label(ip)
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
