import numpy as np
import h5py

# 可加随机数种子
np.random.seed(100)
n = 10
# 生成不等间距的采样点
low = -50.0
high = 50.0
size = 6000
x = np.random.uniform(low, high, size).reshape((-1, n))

w1 = np.ones((x.shape[1], 1)) * 1
w2 = np.ones((x.shape[1], 1)) * 2
w3 = np.ones((x.shape[1], 1)) * 3
w4 = np.ones((x.shape[1], 1)) * 4
w5 = np.ones((x.shape[1], 1)) * 5
w6 = np.ones((x.shape[1], 1)) * 6


# 1
y = x ** 2 @ w6
with h5py.File('data.h5', 'w') as f:
    g = f.create_group('no1')
    g['x_train'] = x
    g['y_train'] = y

# 2
y = x ** 3 @ w2
with h5py.File('data.h5', 'a') as f:
    g = f.create_group('no2')
    g['x_train'] = x
    g['y_train'] = y

# 3
y = x ** 4 @ w3
with h5py.File('data.h5', 'a') as f:
    g = f.create_group('no3')
    g['x_train'] = x
    g['y_train'] = y

##############################################
# 4
y = x ** 2 @ w4 + x @ w5
with h5py.File('data.h5', 'a') as f:
    g = f.create_group('no4')
    g['x_train'] = x
    g['y_train'] = y

# 5
y = x ** 3 @ w5 + x @ w6
with h5py.File('data.h5', 'a') as f:
    g = f.create_group('no5')
    g['x_train'] = x
    g['y_train'] = y

# 6
y = x ** 4 @ w2 + x @ w6
with h5py.File('data.h5', 'a') as f:
    g = f.create_group('no6')
    g['x_train'] = x
    g['y_train'] = y

############################################
# 7
y = x ** 3 @ w3 + x ** 2 @ w2 + x @ w6
with h5py.File('data.h5', 'a') as f:
    g = f.create_group('no7')
    g['x_train'] = x
    g['y_train'] = y

# 8
y = x ** 4 @ w2 + x ** 2 @ w3 + x @ w6
with h5py.File('data.h5', 'a') as f:
    g = f.create_group('no8')
    g['x_train'] = x
    g['y_train'] = y

##############################################
# 9
y = x ** 4 @ w3 + x ** 3 @ w4 + x ** 2 @ w2 + x @ w3
with h5py.File('data.h5', 'a') as f:
    g = f.create_group('no9')
    g['x_train'] = x
    g['y_train'] = y

##############################################
# 10
y = x ** 4 @ w4 + x ** 2 @ w2
with h5py.File('data.h5', 'a') as f:
    g = f.create_group('no10')
    g['x_train'] = x
    g['y_train'] = y

# 11
y = x ** 3 @ w2 + x ** 2 @ w6
with h5py.File('data.h5', 'a') as f:
    g = f.create_group('no11')
    g['x_train'] = x
    g['y_train'] = y

# 12
y = x ** 4 @ w2 + x ** 3 @ w3
with h5py.File('data.h5', 'a') as f:
    g = f.create_group('no12')
    g['x_train'] = x
    g['y_train'] = y

# 13
y = x ** 5 @ w2 + x ** 3 @ w4 + x ** 1 @ w3
with h5py.File('data.h5', 'a') as f:
    g = f.create_group('no13')
    g['x_train'] = x
    g['y_train'] = y


# 14
y = x ** 5 @ w3 + x ** 4 @ w4 + x ** 1 @ w5
with h5py.File('data.h5', 'a') as f:
    g = f.create_group('no14')
    g['x_train'] = x
    g['y_train'] = y



