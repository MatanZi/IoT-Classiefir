from datetime import datetime

from csv_handler.csv_builder import *
from machine_learning_algorithms.random_forest import RF


def main():
    ip_list = ["192.168.1.150", "192.168.1.151", "192.168.1.111", "192.168.1.119"]
    mac_list = ["98:fc:11:a1:f7:0f", "6c:fd:b9:4f:70:0b", "00:17:88:77:35:80", "fc:6b:f0:0a:c3:43"]
    N = 10

    start_time = datetime.now()
    dataset_file = r"C:\Users\Dan\PycharmProjects\IoT-Classiefir\outfile0505.csv"
    features_csv_path = r"C:\Users\Dan\PycharmProjects\IoT-Classiefir\features1.csv"
    build_features_csv_time_split(dataset_file, features_csv_path, ip_list, 300, N)

    build_features_csv_packet_split(dataset_file, features_csv_path, ip_list, N)


    end_time = datetime.now()

    print("Time = " + str((end_time - start_time).total_seconds()))
    features_df = pd.read_csv(features_csv_path)
    factor = pd.factorize(features_df.iloc[:, 4])
    X = features_df.iloc[:, :4]
    y = features_df.iloc[:, 4]
    definitions = factor[1]

    RF(X, y, definitions)

    '''
    features_df = pd.read_csv(features_csv_path)
    X = features_df.drop('label', axis=1)
    y = features_df['label']
    SVM(X,y)
    '''


if __name__ == '__main__':
    main()
