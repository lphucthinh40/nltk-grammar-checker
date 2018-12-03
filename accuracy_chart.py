# from pylab import *
#
# t = arange(0.0, 20.0, 1)
# s = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
# s2 = [4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
# plot(t, s)
# plot(t, s2)
#
# xlabel('Item (s)')
# ylabel('Value')
# title('Python Line Chart: Plotting numbers')
# grid(True)
# show()
import matplotlib.pyplot as plt

n = [2500, 5000, 7500, 8800]
# accuracy collected from training three ML models over 2500, 5000, 7500, 8800 sentences
accuracy = { 'crf':             [95.836, 96.859, 97.313, 97.428],
             'decision-tree':   [61.745, 71.35, 75.09, 89.95],
             'decision-tree-modified':   [85.8, 88.4, 90.76, 91.45],
             'naive-bayes':     [77.38, 82.885, 85.09, 93.396]
             }
# accuracy collected from training three ML models over 2500, 5000, 7500, 8800 sentences
training_time = { 'crf':             [57.789, 119.542, 219.018, 258.306],
                  'decision-tree':   [149.32, 392.146, 716.784, 921.008],
                  'decision-tree-modified':   [47.3126, 116.3389, 198.4007, 234.0613],
                  'naive-bayes':     [2.2011, 4.3094, 6.7429, 7.5954]
                }

plt.subplot(1, 2, 1)
plt.plot(n, accuracy['crf'], label='crf', linewidth=2, color='red')
plt.plot(n, accuracy['decision-tree'], label='decision-tree', linewidth=2, color='blue')
plt.plot(n, accuracy['decision-tree-modified'], label='decision-tree-modified',
                      linewidth=1, color='blue', linestyle='--')
plt.plot(n, accuracy['naive-bayes'], label='naive-bayes', linewidth=2, color='green')

plt.xlabel('Size of training data (sentence)')
plt.ylabel('Accuracy (%)')
plt.title('Accuracy vs Training Set Size')
plt.legend()
plt.grid(True)

plt.subplot(1, 2, 2)
plt.plot(n, training_time['crf'], label='crf', linewidth=2, color='red')
plt.plot(n, training_time['decision-tree'], label='decision-tree', linewidth=2, color='blue')
plt.plot(n, training_time['decision-tree-modified'], label='decision-tree-modified',
         linewidth=1, color='blue', linestyle='--')
plt.plot(n, training_time['naive-bayes'], label='naive-bayes', linewidth=2, color='green')

plt.xlabel('Size of training data (sentence)')
plt.ylabel('Training Time (s)')
plt.title('Training Time vs Training Set Size')
plt.legend()
plt.grid(True)

plt.show()