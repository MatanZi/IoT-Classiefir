from csv_handler.csv_builder import *
from features_handler.Feature import Feature
from packet_handler.Packet import build_packets
from session_handler.session_builder import build_sessions
from packet_handler.Packet import Packet


def main():
    ip_list = ["192.168.1.150", "192.168.1.151", "192.168.1.119", "192.168.1.111"]
    mac_list = ["98:fc:11:a1:f7:0f", "00:17:88:77:35:80", "fc:6b:f0:0a:c3:43", "6c:fd:b9:4f:70:0b"]
    feature_id = 0
    N = 10
    print("retrieving dataset...")
    dataset = pd.DataFrame()
    for chunk in pd.read_csv(r"C:\Users\Matan\Documents\GitHub\IoT Classiefir\out\packets_dataset.csv", error_bad_lines=False, warn_bad_lines=False, chunksize=20000):
        dataset = pd.concat([dataset, chunk], ignore_index=True)

    # create CSV with olny IoT device ip address
    filtered_IP = build_filtered_IP_csv(dataset, ip_list)

    # create CSV with olny IoT device mac address
    #filtered_MAC = build_filtered_MAC_csv(dataset, mac_list)

    # create CSV with olny IoT device ip address (44000 packets)
    #compressed_filtered_IP = build_compressed_filtered_IP_csv(dataset, ip_list)

    # create features
    print("Creating features...")
    filtered_ip_packets = build_packets(filtered_IP)
    for address in mac_list:
        feature_list = []
        session_list = build_sessions(filtered_ip_packets, address)
        print("session_list length:")
        print(len(session_list))
        for mac_address in session_list:
            print("session_list[mac_address].packets Length:")
            print(len(session_list[mac_address].packets))
            if len(session_list[mac_address].packets) > 1:
                sent_time, rec_time = session_list[mac_address].calc_delta_time_send_receive()
                packet = session_list[mac_address].packets[0]
                feature_list.append(Feature(feature_id, packet.s_mac, packet.d_mac, packet.s_ip, packet.d_ip, packet.s_port, packet.d_port, N, N,sent_time[:N], rec_time[:N], session_list[mac_address].label))

    print(len(feature_list))



if __name__ == '__main__':
    main()
