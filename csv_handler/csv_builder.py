import pandas as pd


def build_filtered_IP_csv(csv_file, ip_list):
    IP_csv = csv_file.loc[csv_file['ip.src'].isin(ip_list) | csv_file['ip.dst'].isin(ip_list)]
    IP_csv.to_csv("filter_IP.csv")


def build_filtered_MAC_csv(csv_file, mac_list):
    MAC_csv = csv_file.loc[csv_file["wlan.sa"].isin(mac_list) | csv_file['wlan.da'].isin(mac_list)]
    MAC_csv.to_csv("filter_MAC.csv")


def build_csv():
    csv_file = pd.read_csv('WS12-05-2019.csv', error_bad_lines=False, warn_bad_lines=False, low_memory=False)
    ip_list = ["192.168.1.150", "192.168.1.151", "192.168.1.119", "192.168.1.111"]
    mac_list = ["98:FC:A1:F7:0F", "00:17:88:77:35:80", "FC:6B:F0:0A:C3:43", "6C:FD:B9:4F:70:0B"]
    build_filtered_IP_csv(csv_file, ip_list)
    build_filtered_MAC_csv(csv_file, mac_list)
