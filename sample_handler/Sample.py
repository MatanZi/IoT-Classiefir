class Sample(object):
    def __init__(self, id, s_mac, d_mac, s_ip, d_ip, s_port, d_port, n_packet_sent, n_packet_received, sent_time , rec_time, label):
        self.id = id
        self.n_packet_sent = n_packet_sent
        self.n_packet_received = n_packet_received
        self.sent_time = sent_time
        self.rec_time = rec_time
        self.s_mac = s_mac
        self.d_mac = d_mac
        self.s_ip = s_ip
        self.d_ip = d_ip
        self.s_port = s_port
        self.d_port = d_port
        self.label = label


def build_packets(features_csv):
    features_list = []
    time_list = []
    time_headers = features_csv.columns[features_csv.columns.str.contains('Diffrence_time')]
    for col_name, row in features_csv.iterrows():
        for header in time_headers:
            time_list.append(row[header])
        feature = Sample(row['ID'], row["s_mac"], row["d_mac"], row["s_ip"], row["d_ip"], row["s_port"], row["d_port"], row["N-packet_sent"], row["packet_received"], time_list)
        features_list.append(feature)

    return features_list

def toString(self):
    return "id: "+self.id+", Source mac: "+self.s_mac+", Des mac: "+self.d_mac+", Source IP:  "+self.s_ip+", Des IP: "+self.d_ip+", Source port: "+self.s_port+", Des port: "+self.d_port+" N-sent: "+self.n_packet_sent+", N-recieved: "+self.n_packet_received+", sent_time:  "+self.sent_time+", rec_time: "+self.rec_time+", Label: "+self.label


