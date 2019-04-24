import numpy as np
import matplotlib.pyplot as plt

hours_spent_driving_x = [10, 9, 2, 15, 10, 16, 11, 16]
risk_score_y = [95, 80, 10, 50, 45, 98, 38, 93]

x = np.array(hours_spent_driving_x)
y = np.array(risk_score_y)
n = np.size(x)

mean_x = np.mean(x)
mean_y = np.mean(y)

cov_xy = np.sum(x * y) - (n * mean_x * mean_y)
cov_xx = np.sum(x * x) - (n * mean_x * mean_x)

slope = cov_xy / cov_xx

intercept = mean_y - (slope * mean_x)

print(slope)
print(intercept)
print(slope * 10 + intercept)

# Plotting Graph
plt.scatter(x, y, color='m', marker='o', s=30)

y_pred = intercept + (slope * x)

plt.plot(x, y_pred, color='g')

plt.xlabel('Hours Spent Driving')
plt.ylabel('Risk Score')
plt.show()

'''
4.58789860997547
12.584627964022893
58.46361406377759
'''