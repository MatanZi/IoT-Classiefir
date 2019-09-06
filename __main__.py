import pandas as pd
import numpy as np
from csv_handler.csv_builder import *
from sample_handler.Sample import Sample
from packet_handler.Packet import build_packets
from session_handler.session_builder import build_sessions
from machine_learning_algorithms.random_forest import RF
from packet_handler.Packet import Packet
from sklearn import datasets


def main():
    ip_list = ["192.168.1.150", "192.168.1.151", "192.168.1.119", "192.168.1.111"]
    mac_list = ["98:fc:11:a1:f7:0f", "6c:fd:b9:4f:70:0b", "00:17:88:77:35:80", "fc:6b:f0:0a:c3:43"]
    sample_id = 0
    N = 10
    sample_list = []

    dataset_file =  r"C:\Users\Dan\PycharmProjects\IOT_project\BigSample.csv"

    print("retrieving dataset...")
    dataset = pd.DataFrame()
    for chunk in pd.read_csv(dataset_file, error_bad_lines=False, warn_bad_lines=False, chunksize=20000):
        dataset = pd.concat([dataset, chunk], ignore_index=True)


    # create DataFrame with only IoT device ip address
    filtered_IP_df = build_filtered_IP_csv(dataset, ip_list)

    # create CSV with only IoT device mac address
    #filtered_MAC = build_filtered_MAC_csv(dataset, mac_list)

    # create CSV with only IoT device ip address (44000 packets)
    #compressed_filtered_IP = build_compressed_filtered_IP_csv(dataset, ip_list)

    # create features
    print("Creating features...")
    filtered_ip_packets_list = build_packets(filtered_IP_df)
    for address in ip_list:
        session_dict = build_sessions(filtered_ip_packets_list, address)
        for session_ip in session_dict:
            session = session_dict[session_ip]
            if session.packets_num > 1:
                sent_time, rec_time = session.calc_delta_time_send_receive()
                #packet = session.packets[0]

                sample = Sample(np.asarray(sent_time[:N-1]), np.asarray(rec_time[:N-1]), session.label)

                #sample = Sample(np.asarray(session.packets_size_sent[:N]), np.asarray(session.packets_size_rec[:N]), np.asarray(sent_time[:N-1]), np.asarray(rec_time[:N-1]), np.asarray(session.label))

                sample_list.append(sample)
                print(sample_list)
                #sample_list.append(Sample(sample_id, packet.s_mac, packet.d_mac, packet.s_ip, packet.d_ip, packet.s_port, packet.d_port, N, N, sent_time[:N], rec_time[:N], session_dict[ip_address].label))
    #print(sample_list[0].sent_time)

    feature_list = []
    for sample in sample_list:
        if sample.n_packet_rec_time.size != 0:
            n_packets_rec_deltaT_mean = 0
        else:
            n_packets_rec_deltaT_mean = np.mean(sample.n_packet_rec_time)
        if sample.n_packet_sent_time.size == 0:
            n_packets_sent_deltaT_mean = 0
        else:
            n_packets_sent_deltaT_mean = np.mean(sample.n_packet_sent_time)
        #n_packets_rec_size_mean = np.mean(sample.sizeof_n_packet_received)
       # n_packets_sent_size_mean = np.mean(sample.sizeof_n_packet_sent)
        feature_list.append([n_packets_rec_deltaT_mean, n_packets_sent_deltaT_mean, sample.label])

        #feature_list.append([n_packets_rec_size_mean, n_packets_sent_size_mean, n_packets_rec_deltaT_mean, n_packets_sent_deltaT_mean, sample.label])

    n = len(sample_list)
    data = np.asarray(feature_list)
    factor = pd.factorize(data[:, 2])
    data.reshape(n,3)
    X = data[:, :2]
    y = data[:, 2]
    definitions = factor[1]

    RF(X,y, definitions)


   # iris = datasets.load_iris()
  #  iris.head()
    '''data = pd.DataFrame({
        'packets_size_sent':sample_list[:,0],
        'session.packets_size_rec':sample_list[:,1],
        'sent_time':sample_list[:,2],
        'rec_time':sample_list[:,3],
        'label':sample_list[:,4]
    })
    data.head()
       for sample in sample_list:
        X.append(sample[:3])
        y.append(sample[4])
    print("x = ")
    print(X)
    print("y = ")
    print(y)
    #RF(X, y)
    '''


if __name__ == '__main__':
    main()
