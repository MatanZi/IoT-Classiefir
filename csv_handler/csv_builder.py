from datetime import timedelta

import numpy as np
import pandas as pd
from packet_handler.Packet import build_packets
from session_handler.session_builder import build_sessions, build_sessions_df


def build_compressed_filtered_IP_csv(csv_file, ip_list):
    IP_df = pd.DataFrame()
    for chunk in pd.read_csv(csv_file, error_bad_lines=False,
                             warn_bad_lines=False, chunksize=20000):
        IP_df = pd.concat([IP_df, chunk], ignore_index=True)

    IP_df = IP_df.loc[(IP_df['ip.src'].isin(ip_list)) | (IP_df['ip.dst'].isin(ip_list))]
    IP_csv_compressed = IP_df.head(44000)
    IP_csv_compressed.to_csv(r"C:\Users\user\Desktop\Final Project\filtered_ip.csv")
    return IP_csv_compressed


def build_filtered_IP_csv(csv_file, ip_list):
    IP_csv = csv_file.loc[(csv_file['ip.src'].isin(ip_list)) | (csv_file['ip.dst'].isin(ip_list))]
    # IP_csv.to_csv(r"C:\Users\Matan\Documents\GitHub\IoT Classiefir\out\filter_IP.csv")
    return IP_csv


def build_filtered_MAC_csv(csv_file, mac_list):
    MAC_csv = csv_file.loc[(csv_file["wlan.sa"].isin(mac_list)) | (csv_file['wlan.da'].isin(mac_list))]
    # MAC_csv.to_csv(r"C:\Users\Matan\Documents\GitHub\IoT Classiefir\out\filter_MAC.csv")
    return MAC_csv


def build_features_csv_packet_split(dataset_file, w_path, ip_list, n):
    sample_list = []
    print("Retrieving dataset...")
    dataset = pd.DataFrame()
    for chunk in pd.read_csv(dataset_file, error_bad_lines=False, warn_bad_lines=False, chunksize=20000):
        dataset = pd.concat([dataset, chunk], ignore_index=True)

    # create DataFrame with only IoT device ip address
    filtered_ip_df = build_filtered_IP_csv(dataset, ip_list)

    # create CSV with only IoT device mac address
    # filtered_MAC = build_filtered_MAC_csv(dataset, mac_list)

    # create CSV with only IoT device ip address (44000 packets)
    # compressed_filtered_IP = build_compressed_filtered_IP_csv(dataset, ip_list)

    # create features
    print("Extracting packets...")
    filtered_ip_packets_list = build_packets(filtered_ip_df)
    print("Extracting features...")
    for address in ip_list:
        session_dict = build_sessions(filtered_ip_packets_list, address)
        for session_ip in session_dict:
            session = session_dict[session_ip]
            if len(session.packets_size_rec) >= n and len(session.packets_size_sent) >= n:
                sub_sessions_dict = session.split_by_packets(n)
                for i in sub_sessions_dict:
                    sub_session = sub_sessions_dict[i]
                    if len(sub_session.packets_size_rec) >= n and len(sub_session.packets_size_sent) >= n:
                        add_sample(sub_session, sample_list, n)
                        print(str(sub_session.label) + " session with " + str(session_ip) + " : " +
                              str(len(sub_session.packets_size_rec))
                              + " - " + str(len(sub_session.packets_size_sent)))

    print("Number of bidirectional samples with >=N  (s/r) packets = " + str(len(sample_list)))
    df = pd.DataFrame(sample_list,  columns = ['n_packets_rec_size_mean', 'n_packets_sent_size_mean',
                                               'n_packets_rec_deltaT_mean', 'n_packets_sent_deltaT_mean', 'label'])
    print("Writing to csv...")
    df.to_csv(w_path, index=False)
    print("Done!")


def build_features_csv_time_split(dataset_file, w_path, ip_list, max_session_length, n):
    sample_list = []
    print("Retrieving dataset...")
    dataset = pd.DataFrame()
    for chunk in pd.read_csv(dataset_file, error_bad_lines=False, warn_bad_lines=False, chunksize=20000):
        dataset = pd.concat([dataset, chunk], ignore_index=True)

    # create DataFrame with only IoT device ip address
    filtered_ip_df = build_filtered_IP_csv(dataset, ip_list)

    # create CSV with only IoT device mac address
    # filtered_MAC = build_filtered_MAC_csv(dataset, mac_list)

    # create CSV with only IoT device ip address (44000 packets)
    # compressed_filtered_IP = build_compressed_filtered_IP_csv(dataset, ip_list)

    # create features
    print("Extracting packets...")
    filtered_ip_packets_list = build_packets(filtered_ip_df)

    print("Extracting features...")
    for address in ip_list:
        session_dict = build_sessions(filtered_ip_packets_list, address)
        for session_ip in session_dict:
            session = session_dict[session_ip]
            session_length = session.get_session_length()
            if session_length > max_session_length:
                sub_sessions_dict = session.split_by_time(max_session_length)
                for i in sub_sessions_dict:
                    sub_session = sub_sessions_dict[i]
                    if len(sub_session.packets_size_rec) >= n and len(sub_session.packets_size_sent) >= n:
                        add_sample(sub_session, sample_list, n)
                        print(str(sub_session.label) + " session with " + str(session_ip) + " : " +
                              str(len(sub_session.packets_size_rec))
                              + " - " + str(len(sub_session.packets_size_sent)) +
                              " (" + str(sub_session.get_session_length()) + ")")
            elif len(session.packets_size_rec) >= n and len(session.packets_size_sent) >= n:
                add_sample(session, sample_list, n)
                print(str(session.label) + " ***** session with " + str(session_ip) + " : " +
                      str(len(session.packets_size_rec))
                      + " - " + str(len(session.packets_size_sent)) +
                      " (" + str(session.get_session_length()) + ")")

    print("Number of bidirectional samples with >=" + str(n) + "  (s/r) packets = " + str(len(sample_list)))
    df = pd.DataFrame(sample_list, columns=['n_packets_rec_size_mean', 'n_packets_sent_size_mean',
                                            'n_packets_rec_deltaT_mean', 'n_packets_sent_deltaT_mean', 'label'])
    print("Writing to csv...")
    df.to_csv(w_path, index=False)
    print("Done!")


def add_sample(sub_session, sample_list, n):
    sent_time, rec_time = sub_session.calc_delta_time_send_receive()
    n_packets_rec_size_mean = np.mean(sub_session.packets_size_rec[:n])
    n_packets_rec_deltaT_mean = np.mean(rec_time[:n - 1])
    n_packets_sent_size_mean = np.mean(sub_session.packets_size_sent[:n])
    n_packets_sent_deltaT_mean = np.mean(sent_time[:n - 1])
    sample_list.append(
        [n_packets_rec_size_mean, n_packets_sent_size_mean, n_packets_rec_deltaT_mean,
         n_packets_sent_deltaT_mean, sub_session.label])

