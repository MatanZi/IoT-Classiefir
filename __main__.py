from csv_handler.csv_builder import *
from machine_learning_algorithms.random_forest import RF
from machine_learning_algorithms.SVM import SVM



def main():
    ip_list = ["192.168.1.150", "192.168.1.151", "192.168.1.119", "192.168.1.111"]
    mac_list = ["98:fc:11:a1:f7:0f", "6c:fd:b9:4f:70:0b", "00:17:88:77:35:80", "fc:6b:f0:0a:c3:43"]
    N = 5

    dataset_file =  r"C:\Users\user\Desktop\final_project_new\outfile0505.csv"
    features_csv_path = r"C:\Users\user\PycharmProjects\IoT-Classiefir\features1.csv"
    build_features_csv(dataset_file, ip_list, N, features_csv_path)

    features_df = pd.read_csv(features_csv_path)
    X = features_df.drop('label', axis=1)
    y = features_df['label']
    SVM(X,y)
    #factor = pd.factorize(features_df.iloc[:, 4])
    #X = features_df.iloc[:, :4]
    #y = features_df.iloc[:, 4]
    #definitions = factor[1]

    #RF(X, y, definitions)


if __name__ == '__main__':
    main()
