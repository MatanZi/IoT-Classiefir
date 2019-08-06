import pandas as pd

import numpy as np
from pandas import DataFrame


def get_filtered_IP_csv(csv_file, ip_list):
    sIP_csv = csv_file.loc[csv_file['ip.src'].isin(ip_list)]
    dIP_csv = csv_file.loc[csv_file['ip.dst'].isin(ip_list)]
    frames_ip = [sIP_csv, dIP_csv]
    filter_IP = pd.concat(frames_ip)
    filter_IP.to_csv("filter_IP.csv")


def get_filtered_MAC_csv(csv_file, mac_list):
    sMAC_csv = csv_file.loc[csv_file["wlan.sa"].isin(mac_list)]
    dMAC_csv = csv_file.loc[csv_file['wlan.da'].isin(mac_list)]
    frames_mac = [sMAC_csv, dMAC_csv]
    filter_MAC = pd.concat(frames_mac)
    filter_MAC.to_csv("filter_MAC.csv")

def create_sample():
    csv_file = pd.read_csv('WS12-05-2019.csv', error_bad_lines=False, warn_bad_lines=False)
    ip_list = ["192.168.1.150", "192.168.1.151", "192.168.1.119", "192.168.1.111"]
    mac_list = ["98:FC:A1:F7:0F", "00:17:88:77:35:80", "FC:6B:F0:0A:C3:43", "6C:FD:B9:4F:70:0B"]
    get_filtered_IP_csv(csv_file, ip_list)
    get_filtered_MAC_csv(csv_file, mac_list)


create_sample()
