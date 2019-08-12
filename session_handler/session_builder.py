import pandas as pd
from packet_handler.Packet import build_packets
from session_handler.Session import Session


def build_sessions(packet_list, mac):
    sessions = {}
    for packet in packet_list:
        # check if the packet belongs to a known session, if it does, add the packet to it's session
        # (filtering by other mac)
        if packet.s_mac == mac:
            if packet.d_mac in sessions.keys():
                sessions[packet.d_mac].add(packet)
            else:
                new_session = Session(mac, packet.d_mac)
                new_session.add(packet)
                sessions[packet.d_mac] = new_session
        elif packet.d_mac == mac:
            if packet.s_mac in sessions.keys():
                sessions[packet.s_mac].add(packet)
            else:
                new_session = Session(mac, packet.s_mac)
                new_session.add(packet)
                sessions[packet.s_mac] = new_session
    return sessions


'''
mac1 = '98:fc:11:a1:f7:0f'
mac2 = '00:1c:10:f7:cd:bc'
df = pd.read_csv("filter_MAC.csv")
print(df[(((df['wlan.sa'] == mac1) & (df['wlan.da'] == mac2)) | ((df['wlan.da'] == mac1) & (df['wlan.sa'] == mac2)))])
'''


t = pd.read_csv(r"C:\Users\Matan\Documents\GitHub\IoT Classiefir\csv_handler\filter_IP_comp.csv", error_bad_lines=False, warn_bad_lines=False)
packet_list = build_packets(t)
sessions_dict = build_sessions(packet_list, "98:fc:11:a1:f7:0f") # filter_IP.csv for performance (need to use filter_MAC.csv)
print(sessions_dict.keys())
print("Number of sessions: " , len(sessions_dict))
for session in sessions_dict.values():
    send, rec = session.calc_delta_time_send_receive()
    if len(send) > 1 or len(rec) > 1:
        print()
        print("Session with:", session.mac2)
        if len(send) > 1:
            print("-----------------------send-----------------------")
            print(send[:10])
        if len(rec) > 1:
            print("-----------------------rec------------------------")
            print(rec)
