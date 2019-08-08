import pandas as pd


def build_session(filter_ip_csv, row):
    csv_file = pd.read_csv(filter_ip_csv, error_bad_lines=False, warn_bad_lines=False, low_memory=False)
    if pd.notnull(row['tcp.srcport']):
        detils = row[['ip.src', 'ip.dst', 'tcp.srcport', 'tcp.dstport']]
        session_csv = csv_file.loc[:, ['ip.src', 'ip.dst', 'tcp.srcport', 'tcp.dstport'].isin(detils)]
    else:
        detils = row[['ip.src', 'ip.dst', 'udp.srcport', 'udp.dstport']]
        session_csv = csv_file.loc[:, ['ip.src', 'ip.dst', 'udp.srcport', 'udp.dstport'].isin(detils)]


    print(session_csv)



def sessions_handler():
    for name, row in session_csv.iterrows():
        build_session("filter_IP.csv", )