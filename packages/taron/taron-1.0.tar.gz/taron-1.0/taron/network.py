import numpy as np
import torch
from sklearn.model_selection import train_test_split
from torch import nn
from torch.utils.data import Dataset
from neurons_better import Neurons
from seeds import random_seed
from mydata import MyData
import h5py


def main(group, sr, seed):
    test_size = 0.2
    batch_size = 10
    max_epoch = 300
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    with h5py.File('example_data.h5', 'r') as f:
        X_all = np.array(f[group]['x_train'])
        y_all = np.array(f[group]['y_train'])

    X_all = torch.from_numpy(X_all).to(torch.float32)
    y_all = torch.from_numpy(y_all).to(torch.float32)
    X, X_test, y, y_test = train_test_split(X_all, y_all, test_size=test_size, random_state=10)
    trainset = MyData(X, y)
    trainloader = torch.utils.data.DataLoader(trainset, batch_size=batch_size, shuffle=True)

    random_seed(seed)
    net = nn.Sequential(Neurons(10, 8, sr),
                        nn.Sigmoid(),

                        Neurons(8, 5, sr),
                        nn.Sigmoid(),

                        Neurons(5, 3, sr),
                        nn.Sigmoid(),

                        Neurons(3, 1, sr)
                        ).to(device)

    cost = nn.MSELoss().to(device)
    optimizer = torch.optim.RMSprop(net.parameters(), lr=0.001)

    for k in range(max_epoch):
        for inputs, labels in trainloader:
            inputs = inputs.to(device)
            labels = labels.to(device)
            predict = net(inputs)
            loss = cost(predict, labels)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

    with torch.no_grad():
        train_error_net = cost(net(X.to(device)), y.to(device))

    with torch.no_grad():
        test_error_net = cost(net(X_test.to(device)), y_test.to(device))

    return train_error_net.cpu(), test_error_net.cpu()


if __name__ == '__main__':
    gr = 'no1'
    expr = '6@x**2 + 2@x - 3'

    result = np.empty((1, 4))

    train_mse_net_list = []
    test_mse_net_list = []

    for j in range(10):
        train_net, test_net = main(group=gr, sr=expr, seed=(j + 1) * 10)
        train_mse_net_list.append(train_net)
        test_mse_net_list.append(test_net)

    result[0, 0] = np.mean(train_mse_net_list)
    result[0, 1] = np.mean(test_mse_net_list)
    result[0, 2] = np.std(train_mse_net_list)
    result[0, 3] = np.std(test_mse_net_list)

    np.savetxt(gr + '_result.csv', result, delimiter=',')
