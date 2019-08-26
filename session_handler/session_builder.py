from session_handler.Session import Session


def get_label(address):
    if address == "192.168.1.150" or address == "98:fc:11:a1:f7:0f":
        return "Camera 1"
    elif address == "192.168.1.151" or address == "6c:fd:b9:4f:70:0b":
        return "Camera 2"
    elif address == "192.168.1.119" or address == "00:17:88:77:35:80":
        return "Smart blub"
    elif address == "192.168.1.111" or address == "fc:6b:f0:0a:c3:43":
        return "Intercom"
    else:
        print("Label wasn't found !")


def build_sessions(packet_list, mac):
    sessions = {}
    for packet in packet_list:
        # check if the packet belongs to a known session, if it does, add the packet to it's session
        # (filtering by other mac)
        label = get_label(mac)
        if packet.s_mac == mac:
            if packet.d_mac in sessions.keys():
                sessions[packet.d_mac].add(packet)
            else:
                new_session = Session(mac, packet.d_mac , label)
                new_session.add(packet)
                sessions[packet.d_mac] = new_session
        elif packet.d_mac == mac:
            if packet.s_mac in sessions.keys():
                sessions[packet.s_mac].add(packet)
            else:
                new_session = Session(mac, packet.s_mac ,label)
                new_session.add(packet)
                sessions[packet.s_mac] = new_session
    return sessions
