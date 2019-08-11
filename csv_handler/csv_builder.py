import pandas as pd


def build_filtered_IP_csv(csv_file, ip_list):
    IP_csv = csv_file.loc[csv_file['ip.src'].isin(ip_list) | csv_file['ip.dst'].isin(ip_list)]
    IP_csv.to_csv("filter_IP.csv")


def build_filtered_MAC_csv(csv_file, mac_list):
    MAC_csv = csv_file.loc[csv_file["wlan.sa"].isin(mac_list) | csv_file['wlan.da'].isin(mac_list)]
    MAC_csv.to_csv("filter_MAC.csv")


def build_csv(csv_file):
    df = pd.DataFrame()
    for chunk in pd.read_csv(csv_file, error_bad_lines=False, warn_bad_lines=False, chunksize=20000):
        df = pd.concat([df, chunk], ignore_index=True)
    ip_list = ["192.168.1.150", "192.168.1.151", "192.168.1.119", "192.168.1.111"]
    mac_list = ["98:fc:a1:f7:0f", "00:17:88:77:35:80", "fc:6b:f0:0a:c3:43", "6c:fd:b9:4f:70:0b"]
    build_filtered_IP_csv(df, ip_list)
    build_filtered_MAC_csv(df, mac_list)

build_csv('BigSample.csv') # BigSample.csv = 320mb dataset