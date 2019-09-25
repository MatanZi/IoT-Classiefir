import csv
from datetime import datetime

import numpy as np
import pandas as pd

from session_handler.session_builder import build_sessions


def get_n_packets(csv_file, address):
    try:
        n_sent = 0
        n_received = 0
        for val in csv_file['ip.src']:
            if val == address:
                n_sent = n_sent + 1

        for val in csv_file['ip.dst']:
            if val == address:
                n_received = n_received + 1

        return n_sent, n_received

    except Exception as e:
        print(e)


def get_max_packets(filter_IP, ip_list):
    try:
        max = 0
        counter = 0
        with open('WS12-05-2019.csv') as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            for i in range(len(ip_list)):
                for row in readCSV:
                    if row[3] == ip_list[i]:
                        counter = counter + 1
                    else:
                        if row[4] == ip_list[i]:
                            counter = counter + 1

            if counter > max:
                max = counter

        return max
    except Exception as e:
        print(e)


def build_header(max_packets):
    try:
        headers = ["ID", "s_mac", "d_mac", "s_ip", "d_ip", "s_port", "d_port", "Protocol", "N-packet_sent",
                   "packet_received"]
        for i in range(max_packets):
            headers.append("Diffrence_time (" + str(i + 1) + "-" + str(i + 2) + ")")
        headers.append("Avrage_time")
        headers.append("Label")
        return headers
    except Exception as e:
        print(e)


def get_difference_time(address, n_packets):
    s_ip = address
    flag = False
    result = []
    with open('filter_IP_1.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        # while n_packets > 0 :
        for row in readCSV:
            if row[4] == address and not flag:
                # print("s_ip: " + row[4] + " d_ip: " + row[5])
                s_ip = row[5]
                d_ip = row[4]
                flag = True
                before = datetime.strptime(row[1], '%M:%S.%f')
                n_packets = n_packets - 1

            elif flag and row[4] == s_ip and row[5] == d_ip:
                # print("s_ip: " + row[4] + "d_ip: " + row[5])
                after = datetime.strptime(row[1], '%M:%S.%f')
                result.append(after - before)
                s_ip = address
                flag = False
                n_packets = n_packets - 1

    return result


def build_difference_time(session_csv, n_packets):
    before = 0
    result = []
    for i in range(n_packets):
        for name, row in session_csv.iterrows():
            if before == 0:
                before = datetime.strptime(row['_ws.col.AbsTime'], '%M:%S.%f')
            else:
                after = datetime.strptime(row['_ws.col.AbsTime'], '%M:%S.%f')
                result.append(after - before)
                before = after

    return result


def get_label(ip_list, index):
    if ip_list[index] == "192.168.1.150":
        return "Camera 1"
    elif ip_list[index] == "192.168.1.151":
        return "Camera 2"
    elif ip_list[index] == "192.168.1.119":
        return "Smart blub"
    else:
        return "Intercom"


'''
def build_feature_row(session_csv, ip_list, index, n_packets):
    row = [str(index + 1)]
    row.append(session_csv['wlan.sa'])
    row.append(session_csv['wlan.da'])
    row.append(session_csv['ip.src'])
    row.append(session_csv['ip.dst'])
    if pd.notnull(row['tcp.srcport']):
        row.append(session_csv['tcp.srcport'])
        row.append(session_csv['tcp.dstport'])
        row.append("TCP")
    else:
        row.append(session_csv['udp.srcport'])
        row.append(session_csv['udp.dstport'])
        row.append("UDP")

    row.append(str(n_packets))
    row.append(str(n_packets))
    diff_time = build_difference_time(session_csv, n_packets - 1)
    sum_diff_time = diff_time[0]
    for time in diff_time:
        sum_diff_time = sum_diff_time + time
        row.append(time)

    row.append(str(sum_diff_time / len(diff_time)))
    row.append(get_label(ip_list, index))
    return row
'''


# TODO
def extract_features_df_to_list(df, ip_list, n, machine_num, classby=''):
    features_list = []
    for address in ip_list:
        session_dict = build_sessions(df, address, classby)
        for session in session_dict.values():
            if len(session.packets_size_rec) >= n and len(session.packets_size_sent) >= n:
                sub_sessions_dict = session.split_by_packets(n)
                for sub_session in sub_sessions_dict.values():
                    if len(sub_session.packets_size_rec) >= n and len(sub_session.packets_size_sent) >= n:
                        if machine_num == 1:
                            add_sample_features1(sub_session, features_list, n)
                        elif machine_num == 2:
                            add_sample_features2(sub_session, features_list, n)
                        else:
                            add_sample_features3(sub_session, features_list, n)

                        print(str(sub_session.label) + " session with " + str(sub_session.ip2) + " : " +
                              str(len(sub_session.packets_size_rec))
                              + " - " + str(len(sub_session.packets_size_sent)) +
                              " (" + str(session.get_session_length()) + ")")


    print("Number of bidirectional samples with >=N  (s/r) packets = " + str(len(features_list)))
    if machine_num == 1:
        df = pd.DataFrame(features_list, columns=['n_packets_rec_size_sum', 'n_packets_sent_size_sum',
                                                  'n_packets_rec_deltaT_mean', 'n_packets_sent_deltaT_mean', 'label'])
    elif machine_num == 2:
        df = pd.DataFrame(features_list, columns=['n_packets_rec_size_mean', 'n_packets_sent_size_mean',
                                                  'sent_std', 'rec_std', 'sent_var', 'rec_var', 'label'])
    else:
        df = pd.DataFrame(features_list,
                          columns=['n_packets_rec_size_sum', 'n_packets_sent_size_sum', 'n_packets_rec_size_mean',
                                   'n_packets_sent_size_mean', 'n_packets_rec_deltaT_mean',
                                   'n_packets_sent_deltaT_mean', 'sent_std', 'rec_std', 'sent_var', 'rec_var', 'label'])
    return df


# Article's features
def add_sample_features1(session, sample_list, n):
    sent_time, rec_time = session.calc_delta_time_send_receive()
    n_packets_rec_size_sum = np.sum(session.packets_size_rec[:n])
    n_packets_sent_size_sum = np.sum(session.packets_size_sent[:n])
    n_packets_rec_deltaT_mean = np.mean(rec_time[:n - 1])
    n_packets_sent_deltaT_mean = np.mean(sent_time[:n - 1])
    sample_list.append(
        [n_packets_rec_size_sum, n_packets_sent_size_sum, n_packets_rec_deltaT_mean,
         n_packets_sent_deltaT_mean, session.label])


# Our features
def add_sample_features2(session, sample_list, n):
    sent_time, rec_time = session.calc_delta_time_send_receive()
    n_packets_rec_size_mean = np.mean(session.packets_size_rec[:n])
    n_packets_sent_size_mean = np.mean(session.packets_size_sent[:n])
    sent_std = np.std(sent_time[:n])
    rec_std = np.std(rec_time[:n])
    sent_var = np.var(sent_time[:n])
    rec_var = np.var(rec_time[:n])

    # first_sent_packet_time = sent_time[0]
    # nth_sent_packet_time = sent_time[n]
    # first_rec_packet_time = rec_time[0]
    # nth_rec_packet_time = rec_time[n]

    sample_list.append(
        [n_packets_rec_size_mean, n_packets_sent_size_mean, sent_std,
         rec_std, sent_var, rec_var, session.label])


# Combined features
def add_sample_features3(session, sample_list, n):
    sent_time, rec_time = session.calc_delta_time_send_receive()
    n_packets_rec_size_sum = np.sum(session.packets_size_rec[:n])
    n_packets_sent_size_sum = np.sum(session.packets_size_sent[:n])

    n_packets_rec_size_mean = np.mean(session.packets_size_rec[:n])
    n_packets_rec_deltaT_mean = np.mean(rec_time[:n - 1])
    n_packets_sent_size_mean = np.mean(session.packets_size_sent[:n])
    n_packets_sent_deltaT_mean = np.mean(sent_time[:n - 1])
    sent_std = np.std(sent_time[:n])
    rec_std = np.std(rec_time[:n])
    sent_var = np.var(sent_time[:n])
    rec_var = np.var(rec_time[:n])
    sample_list.append(
        [n_packets_rec_size_sum, n_packets_sent_size_sum, n_packets_rec_size_mean, n_packets_sent_size_mean,
         n_packets_rec_deltaT_mean,
         n_packets_sent_deltaT_mean, sent_std, rec_std, sent_var, rec_var, session.label])
