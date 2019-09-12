import pandas as pd
import numpy as np
from csv_handler.csv_builder import *
from sample_handler.Sample import Sample
from packet_handler.Packet import build_packets
from session_handler.session_builder import build_sessions
from machine_learning_algorithms.random_forest import RF
from machine_learning_algorithms.SVM import SVM
from packet_handler.Packet import Packet
from sklearn import datasets


def main():
    ip_list = ["192.168.1.150", "192.168.1.151", "192.168.1.119", "192.168.1.111"]
    mac_list = ["98:fc:11:a1:f7:0f", "6c:fd:b9:4f:70:0b", "00:17:88:77:35:80", "fc:6b:f0:0a:c3:43"]
    sample_id = 0
    N = 10
    sample_list = []
    feature_list = []

    dataset_file =  r"C:\Users\Dan\PycharmProjects\IoT-Classiefir\outfile.csv"

    print("Retrieving dataset...")
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
            if len(session.packets_size_rec) >= N and len(session.packets_size_sent) >= N:
                sent_time, rec_time = session.calc_delta_time_send_receive()
                print(str(session.label) + " session with " + str(session_ip) + " : " + str(len(session.packets_size_rec))
                      + " - " + str(len(session.packets_size_sent)))
                n_packets_rec_size_mean = np.mean(session.packets_size_rec[:N])
                n_packets_rec_deltaT_mean = np.mean(rec_time[:N - 1])
                n_packets_sent_size_mean = np.mean(session.packets_size_sent[:N])
                n_packets_sent_deltaT_mean = np.mean(sent_time[:N - 1])
                sample_list.append([n_packets_rec_size_mean, n_packets_sent_size_mean, n_packets_rec_deltaT_mean,
                                     n_packets_sent_deltaT_mean, session.label])

    n = len(sample_list)
    print("Number of bidirectional samples with >=N  (s/r) packets = " + str(n))

    data = np.asarray(sample_list)
    factor = pd.factorize(data[:, 4])
    data.reshape(n, 5)
    X = data[:, :4]
    y = data[:, 4]
    definitions = factor[1]

    RF(X, y, definitions)


if __name__ == '__main__':
    main()
