import csv
from datetime import datetime

import numpy as np
import pandas as pd
import switch as switch


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
        headers =["ID", "Address", "N-packet_sent", "packet_received"]
        for i in range(max_packets):
            headers.append("Diffrence_time (" + str(i + 1) + "-" + str(i + 2) + ")")
        headers.append("Avrage_time")
        headers.append("Label")
        return headers
    except Exception as e:
        print(e)


#TODO
def get_difference_time(address, n_packets):
    s_ip = address
    flag = False
    result = []
    with open('filter_IP_1.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        #while n_packets > 0 :
        for row in readCSV:
            if row[4] == address and not flag:
                #print("s_ip: " + row[4] + " d_ip: " + row[5])
                s_ip = row[5]
                d_ip = row[4]
                flag = True
                before = datetime.strptime(row[1], '%M:%S.%f')
                n_packets = n_packets - 1

            elif flag and row[4] == s_ip and row[5] == d_ip:
                #print("s_ip: " + row[4] + "d_ip: " + row[5])
                after = datetime.strptime(row[1], '%M:%S.%f')
                result.append(after - before)
                s_ip = address
                flag = False
                n_packets = n_packets-1

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


def build_feature_row(ip_list, index, n_packets):
    row = [str(index+1), str(ip_list[index])]
    row.append(str(n_packets/2))
    row.append(str(n_packets/2))
    diff_time = get_difference_time(ip_list[index], n_packets)
    sum_diff_time = diff_time[0]
    for time in diff_time:
        sum_diff_time = sum_diff_time + time
        row.append(time)

    row.append(str(sum_diff_time/len(diff_time)))
    row.append(get_label(ip_list, index))
    return row


#TODO
def extract_feature():
        ip_list = ["192.168.1.150", "192.168.1.151", "192.168.1.119", "192.168.1.111"]
        n_packets = 10

        with open('features.csv', mode='w') as features_csv:
            headers = build_header(n_packets)
            writer = csv.writer(features_csv, delimiter=',',
                                quotechar=',', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(headers)
            for i in range(len(ip_list)):
                row = np.array(build_feature_row(ip_list, i, n_packets))
                writer.writerow(row)






extract_feature()
