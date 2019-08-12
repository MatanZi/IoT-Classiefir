import pandas as pd
from session_handler import Session
from packet_handler import Packet


def build_sessions(csv_file, mac):
    df = pd.read_csv(csv_file, error_bad_lines=False, warn_bad_lines=False, engine='python')
    filter_by_mac = df.loc[(df['wlan.sa'] == mac) | (df['wlan.da'] == mac)]
    sessions = {}
    for i, row in filter_by_mac.iterrows():
        # create a packet from row
        if pd.notnull(row['tcp.srcport']):
            packet = Packet(row[0], row['_ws.col.AbsTime'], row['wlan.sa'], row['wlan.da'], row['ip.src'],
                            row['ip.dst'],
                            row['tcp.srcport'], row['tcp.dstport'], "TCP")
        elif pd.notnull(row['udp.srcport']):
            packet = Packet(row[0], row['_ws.col.AbsTime'], row['wlan.sa'], row['wlan.da'], row['ip.src'],
                            row['ip.dst'],
                            row['udp.srcport'], row['udp.dstport'], "UDP")
        else:
            packet = Packet(row[0], row['_ws.col.AbsTime'], row['wlan.sa'], row['wlan.da'], row['ip.src'],
                            row['ip.dst'],
                            0, 0, "other")
        # check if the packet belongs to a known session, if it does, add the packet to it's session
        # (filtering by other mac)
        if packet.s_mac == mac:
            if packet.d_mac in sessions.keys():
                sessions[packet.d_mac].add(packet)
            else:
                sess = Session(mac, packet.d_mac)
                sess.add(packet)
                sessions[packet.d_mac] = sess
        elif packet.d_mac == mac:
            if packet.s_mac in sessions.keys():
                sessions[packet.s_mac].add(packet)
            else:
                sess = Session(mac, packet.s_mac)
                sess.add(packet)
                sessions[packet.s_mac] = sess
    return sessions


'''
mac1 = '98:fc:11:a1:f7:0f'
mac2 = '00:1c:10:f7:cd:bc'
df = pd.read_csv("filter_MAC.csv")
print(df[(((df['wlan.sa'] == mac1) & (df['wlan.da'] == mac2)) | ((df['wlan.da'] == mac1) & (df['wlan.sa'] == mac2)))])
'''

sessions_dict = build_sessions("filter_MAC.csv", "98:fc:11:a1:f7:0f") # filter_IP.csv for performance (need to use filter_MAC.csv)
print(sessions_dict.keys())
print("Number of sessions: " , len(sessions_dict))
for session in sessions_dict.values():
    send, rec = session.calc_delta_time_send_receive()
    if len(send) > 1 or len(rec) > 1:
        print()
        print("Session with:", session.mac2)
        if len(send) > 1:
            print("-----------------------send-----------------------")
            print(send)
        if len(rec) > 1:
            print("-----------------------rec------------------------")
            print(rec)
