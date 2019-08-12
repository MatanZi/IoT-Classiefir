import pandas as pd

from csv_handler.csv_builder import *


def main():
    csv_file = "csv_handler/WS12-05-2019.csv"
    ip_list = ["192.168.1.150", "192.168.1.151", "192.168.1.119", "192.168.1.111"]
    mac_list = ["98:fc:11:a1:f7:0f", "00:17:88:77:35:80", "fc:6b:f0:0a:c3:43", "6c:fd:b9:4f:70:0b"]

    df = pd.DataFrame()
    for chunk in pd.read_csv(csv_file, error_bad_lines=False, warn_bad_lines=False, chunksize=20000):
        df = pd.concat([df, chunk], ignore_index=True)
    #create CSV with olny IoT device ip address
    build_filtered_IP_csv(df, ip_list)
    # create CSV with olny IoT device mac address
    build_filtered_MAC_csv(df, mac_list)
    # create CSV with olny IoT device ip address (44000 packets)
    build_compressed_filtered_IP_csv(df, ip_list)


    filtered_ip_packets = build_packet()







if __name__ == '__main__':
    main()