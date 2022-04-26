# %% 데이터의 분리 (Splitting Data)

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

X, y = np.arange(10).reshape((5, 2)), range(5)
print("X : ", X)
print("y : ", list(y))

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1234)

print("X_train : ", X_train)
print("X_test : ", X_test)
print("y_train : ", y_train)
print("y_test : ", y_test)