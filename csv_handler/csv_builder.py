import pandas as pd

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
    #IP_csv.to_csv(r"C:\Users\Matan\Documents\GitHub\IoT Classiefir\out\filter_IP.csv")
    return IP_csv

def build_filtered_MAC_csv(csv_file, mac_list):
    MAC_csv = csv_file.loc[(csv_file["wlan.sa"].isin(mac_list)) | (csv_file['wlan.da'].isin(mac_list))]
    #MAC_csv.to_csv(r"C:\Users\Matan\Documents\GitHub\IoT Classiefir\out\filter_MAC.csv")
    return MAC_csv


#build_compressed_filtered_IP_csv(r"C:\Users\user\Desktop\final_project_new\WS13-05-2019_2.csv", ["192.168.1.150", "192.168.1.151", "192.168.1.119", "192.168.1.111"])