import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc
  
y_test = np.array([0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1,  0, 1, 0, 0, 0, 1, 1, 1])  
  
y_score = np.array([ 0.17267435,  0.65502116, -0.54222913,  0.3548153 ,  0.0043917 ,  
       -0.20117165,  0.05791453,  0.00383045, -0.15164967,  0.25616448,  
        0.39700001,  0.04521194,  0.33390031, -0.12555765,  0.23799148,  
       -0.36378854, -0.08697789, -0.11682054, -0.25244267, -0.23321231,  
       -0.18097178, -0.10763756, -0.32069159,  0.72074967, -0.29360569,  
       -0.2213709 , -0.32328807, -0.19504498, -0.24365451,  0.37595292])  
  
fpr,tpr,threshold = roc_curve(y_test, y_score)   
roc_auc = auc(fpr,tpr)   
   
fig = plt.figure()  
lw = 2  
ax = fig.add_subplot(111)  
  
ax.plot(fpr, tpr, color='darkorange',  
         lw=lw, label='ROC curve (area = %0.2f)' % roc_auc)   
ax.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')  
ax.set_xlim([0.0, 1.0])  
ax.set_ylim([0.0, 1.05])  
ax.set_xlabel('False Positive Rate')  
ax.set_ylabel('True Positive Rate')  
ax.set_title('Receiver operating characteristic example')  
ax.legend(loc="lower right")  
plt.show()
