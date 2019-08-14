
def build_compressed_filtered_IP_csv(csv_file, ip_list):
    IP_csv = csv_file.loc[(csv_file['ip.src'].isin(ip_list)) | (csv_file['ip.dst'].isin(ip_list))]
    IP_csv_compressed = IP_csv.head(44000)
    #IP_csv_compressed.to_csv(r"C:\Users\Matan\Documents\GitHub\IoT Classiefir\out\filter_IP.csv")
    return IP_csv_compressed

def build_filtered_IP_csv(csv_file, ip_list):
    IP_csv = csv_file.loc[(csv_file['ip.src'].isin(ip_list)) | (csv_file['ip.dst'].isin(ip_list))]
    #IP_csv.to_csv(r"C:\Users\Matan\Documents\GitHub\IoT Classiefir\out\filter_IP.csv")
    return IP_csv

def build_filtered_MAC_csv(csv_file, mac_list):
    MAC_csv = csv_file.loc[(csv_file["wlan.sa"].isin(mac_list)) | (csv_file['wlan.da'].isin(mac_list))]
    #MAC_csv.to_csv(r"C:\Users\Matan\Documents\GitHub\IoT Classiefir\out\filter_MAC.csv")
    return MAC_csv
