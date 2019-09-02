import pandas as pd
import numpy as np
from csv_handler.csv_builder import *
from sample_handler.Sample import Sample
from packet_handler.Packet import build_packets
from session_handler.session_builder import build_sessions
from machine_learning_algorithms.random_forest import RF
from packet_handler.Packet import Packet


def main():
    ip_list = ["192.168.1.150", "192.168.1.151", "192.168.1.119", "192.168.1.111"]
    mac_list = ["98:fc:11:a1:f7:0f", "6c:fd:b9:4f:70:0b", "00:17:88:77:35:80", "fc:6b:f0:0a:c3:43"]
    sample_id = 0
    N = 10
    sample_list = []


    print("retrieving dataset...")
    dataset = pd.DataFrame()
    for chunk in pd.read_csv(r"C:\Users\user\Desktop\final project new\filter_IP.csv", error_bad_lines=False, warn_bad_lines=False, chunksize=20000):
        dataset = pd.concat([dataset, chunk], ignore_index=True)


    # create CSV with olny IoT device ip address
    filtered_IP = build_filtered_IP_csv(dataset, ip_list)

    # create CSV with olny IoT device mac address
    #filtered_MAC = build_filtered_MAC_csv(dataset, mac_list)

    # create CSV with olny IoT device ip address (44000 packets)
    #compressed_filtered_IP = build_compressed_filtered_IP_csv(dataset, ip_list)

    # create features
    print("Creating features...")
    filtered_ip_packets = build_packets(filtered_IP)
    for address in ip_list:
        session_dict = build_sessions(filtered_ip_packets, address)
        for session in session_dict:
            if len(session_dict[session].packets) > 1:
                sent_time, rec_time = session_dict[session].calc_delta_time_send_receive()
                #packet = session_dict[session].packets[0]

                sample_list.append([np.asarray(sent_time[:N-1]), np.asarray(rec_time[:N-1]), session_dict[session].label])
                #print(sample_list)
                #sample_list.append(Sample(sample_id, packet.s_mac, packet.d_mac, packet.s_ip, packet.d_ip, packet.s_port, packet.d_port, N, N, sent_time[:N-1], rec_time[:N-1], session_dict[session].label))
    n = len(sample_list)
    newData = np.asarray(sample_list)
    newData.reshape(n,3)
    print(newData)
    X = newData[:,:2]
    y = newData[:,2]
    #print(sample_list[0].sent_time)

    #X = np.ndarray((n,))
    #y = np.ndarray((n,))
    #for sample in sample_list:
     #   X = np.concatenate(X, sample[0:2])
      #  y = np.concatenate(y, sample[2])
    print("x = ")
    print(X)
    print("y = ")
    print(y)

    RF(X, y)



if __name__ == '__main__':
    main()
