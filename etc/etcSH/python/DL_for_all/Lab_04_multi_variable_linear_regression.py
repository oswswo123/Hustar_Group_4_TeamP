# %% multi variable linear regression

import tensorflow as tf

x1 = [ 73., 93., 89., 96., 73. ]
x2 = [ 80., 88., 91., 98., 66. ] 
x3 = [ 75., 93., 90., 100., 70. ]
Y = [153., 185., 180., 196., 142. ]

w1 = tf.Variable(tf.random.normal([1]))
w2 = tf.Variable(tf.random.normal([1]))
w3 = tf.Variable(tf.random.normal([1]))
b = tf.Variable(tf.random.normal([1]))

learning_rate = 0.000001

for step in range(1000+1):
    # tf.GradientTape() to record the gradient of the cost function
    with tf.GradientTape() as tape:
        hypothesis = w1 * x1 + w2 * x2 + w3 * x3 + b
        cost = tf.reduce_mean(tf.square(hypothesis - Y))
    # calculates the gradients of the cost
    w1_grad, w2_grad, w3_grad, b_grad = tape.gradient(cost, [w1, w2, w3, b])
    
    # update w1, w2, w3 and b
    w1.assign_sub(learning_rate * w1_grad)
    w2.assign_sub(learning_rate * w2_grad)
    w3.assign_sub(learning_rate * w3_grad)
    b.assign_sub(learning_rate * b_grad)
    
    if step % 50 == 0:
        print("{:5} | {:12.4f}".format(step, cost.numpy()))

# %% using matrix

import numpy as np
import tensorflow as tf

# 5 x 3 matrix (x 종류 3가지, 데이터 수 5개)
data = np.array([
    #x1,  x2,  x3,    y
    [73., 80., 75., 152.],
    [93., 88., 93., 185.],
    [89., 91., 90., 180.],
    [96., 98., 100., 196.],
    [73., 66., 70., 142.]
    ], dtype=np.float32)

# slice data
X = data[:, :-1]
Y = data[:, [-1]]

W = tf.Variable(tf.random.normal([3, 1]))
b = tf.Variable(tf.random.normal([1]))

learning_rate = 0.000001

# hypothesis, prediction function
def predict(X):
    return tf.matmul(X, W) + b

n_epochs = 2000
for step in range(n_epochs + 1):
    # record the gradient of the cost function
    with tf.GradientTape() as tape:
        cost = tf.reduce_mean((tf.square(predict(X) - Y)))
    
    # calculates the gradients of the loss
    W_grad, b_grad = tape.gradient(cost, [W, b])
    
    # updates parameters (W and b)
    W.assign_sub(learning_rate * W_grad)
    b.assign_sub(learning_rate * b_grad)
    
    if step % 100 == 0:
        print("{:5} | {:10.4f}".format(step, cost.numpy()))
