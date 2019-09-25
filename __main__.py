from datetime import datetime
import matplotlib.pyplot as plt
from csv_handler.csv_builder import *
from machine_learning_algorithms.random_forest import RF


def main():
    ip_list = ["192.168.1.150", "192.168.1.151", "192.168.1.111"]
    #ip_list = ["192.168.0.104", "192.168.0.5", "192.168.0.179"]
    mac_list = ["98:fc:11:a1:f7:0f", "6c:fd:b9:4f:70:0b", "00:17:88:77:35:80", "fc:6b:f0:0a:c3:43"]
    dataset_file = r"C:\Users\Dan\PycharmProjects\IoT-Classiefir\outfile0505.csv"
    acc_dict = {}

    # TODO move to function

    

    for i in range(5, 21):
        i_acc = []
        for j in range(1, 4):
            print("i: " + str(i) + " j: " + str(j))
            features_csv_path = r"C:\Users\Dan\PycharmProjects\IoT-Classiefir\features\features_2409_" + str(i) + "_" + str(
                j) + ".csv "
            #build_features_csv_packet_split(dataset_file, features_csv_path, ip_list, i, j)
            features_df = pd.read_csv(features_csv_path)
            if j == 1:
                i_acc.append(RF(features_df, 4))
            elif j == 2:
                i_acc.append(RF(features_df, 6))
            elif j == 3:
                i_acc.append(RF(features_df, 10))
                print(str(i_acc))
                # avg_acc = sum(i_acc) / len(i_acc)
                # print(str(avg_acc))
                acc_dict[i] = i_acc

    l = list(acc_dict.values())
    np.savetxt(r"C:\Users\Dan\PycharmProjects\IoT-Classiefir\2409_plotList.csv", l, delimiter=",", fmt='%s', header='a,b,c', comments='')
    df = pd.read_csv(r"C:\Users\Dan\PycharmProjects\IoT-Classiefir\2409_plotList.csv")
    x = df['a'].values.tolist()
    y = df['b'].values.tolist()
    z = df['c'].values.tolist()
    #z = [row[2] for row in l]

    index = np.arange(16)
    bar_width = 0.3
    opacity = 0.8

    ax = plt.subplot()

    rect1 = ax.bar(index - bar_width, x, width=bar_width, color='b', align='center', label='Article features')
    rect2 = ax.bar(index, y, width=bar_width, color='g', align='center', label='Our features')
    rect3 = ax.bar(index + bar_width, z, width=bar_width, color='y', align='center', label='Combined features')

    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{0:.2f}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

    autolabel(rect1)
    autolabel(rect2)
    autolabel(rect3)

    plt.xticks(index, list(range(5, 21)))
    plt.legend()

    plt.tight_layout()
    #ax.autoscale(tight=True)

    plt.title('3 IoT Devices Classification Accuracy')
    plt.ylabel('Accuracy')
    plt.xlabel('N')
    plt.savefig(r"C:\Users\Dan\PycharmProjects\IoT-Classiefir\plotGraph.png")
    plt.show()

    start_time = datetime.now()


if __name__ == '__main__':
    main()
