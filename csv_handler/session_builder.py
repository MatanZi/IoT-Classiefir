import pandas as pd
from Session import Session
from Packet import Packet

def build_sessions(csv_file, mac):
    df = pd.read_csv(csv_file, error_bad_lines=False, warn_bad_lines=False, engine='python')
    filter_by_mac = df.loc[(df['wlan.sa'] == mac) | (df['wlan.da'] == mac)]
    sessions = {}
    for i, row in filter_by_mac.iterrows():
        # create a packet from row
        if pd.notnull(row['tcp.srcport']):
            packet = Packet(row[0], row['_ws.col.AbsTime'], row['wlan.sa'], row['wlan.da'], row['ip.src'], row['ip.dst'],
                            row['tcp.srcport'], row['tcp.dstport'], "TCP")
        elif pd.notnull(row['udp.srcport']):
            packet = Packet(row[0], row['_ws.col.AbsTime'], row['wlan.sa'], row['wlan.da'], row['ip.src'], row['ip.dst'],
                            row['udp.srcport'], row['udp.dstport'], "UDP")
        else:
            packet = Packet(row[0], row['_ws.col.AbsTime'], row['wlan.sa'], row['wlan.da'], row['ip.src'],row['ip.dst'],
                            0, 0, "other")
        # check if the packet belongs to a known session, if it does, add the packet to it's session
        # (filtering by other mac)
        if packet.s_mac == mac:
            if packet.d_mac in sessions.keys():
                sessions[packet.d_mac].add(packet)
            else:
                sess = Session(mac,packet.d_mac)
                sess.add(packet)
                sessions[packet.d_mac] = sess
        elif packet.d_mac == mac:
            if packet.s_mac in sessions.keys():
                sessions[packet.s_mac].add(packet)
            else:
                sess = Session(mac,packet.s_mac)
                sess.add(packet)
                sessions[packet.s_mac] = sess
    return sessions

sessions = {}
build_sessions("filter_MAC.csv", "00:17:88:77:35:80")



#def build_session2(filter_ip_csv, row):
#    csv_file = pd.read_csv(filter_ip_csv, error_bad_lines=False, warn_bad_lines=False, low_memory=False)
#    if pd.notnull(row['tcp.srcport']):
#        detils = row[['ip.src', 'ip.dst', 'tcp.srcport', 'tcp.dstport']]
#        session_csv = csv_file.loc[:, ['ip.src', 'ip.dst', 'tcp.srcport', 'tcp.dstport'].isin(detils)]
#    else:
#        detils = row[['ip.src', 'ip.dst', 'udp.srcport', 'udp.dstport']]
#        session_csv = csv_file.loc[:, ['ip.src', 'ip.dst', 'udp.srcport', 'udp.dstport'].isin(detils)]


#    print(session_csv)



#def sessions_handler():
#    for name, row in session_csv.iterrows():
#        build_session("filter_IP.csv", )