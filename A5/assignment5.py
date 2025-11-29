from sklearn import datasets
from sklearn.svm import SVR
from sklearn.model_selection import cross_validate, cross_val_score
import pickle

# part 1 : load dataset
data = datasets.load_diabetes()

# X is uppercase for matrix (2D), y is lowercase for vector (1D)
X = data['data']
y = data['target']

# part 2 Support Vector Machine (SVM) with 10 fold cross-validation
svr_model = SVR() #creates a new svr model
# MSE = Mean Squared Error - squares the error before averaging
mse_scores = cross_val_score(svr_model, X, y, cv=10, scoring ='neg_mean_squared_error')\
     #cv is number of folds, 
mean_mse = mse_scores.mean()

# MAE = Mean Absolute Error - takes abs value of error before averaging
mae_scores = cross_val_score(svr_model, X, y, cv=10, scoring ='neg_mean_absolute_error')
mean_mae = mae_scores.mean()

print('MSE = ', mean_mse)
print('MAE = ', mean_mae)

# part 3 Create new SVR and train it on ALL X and y Data
svr_new_model = SVR()
svr_new_model.fit(X,y) #trains the model, takes features (X) and targets (y) to make prediction


# part 4 Save trained SVM to pickle
with open('assignment5.pkl', 'wb') as file:
    pickle.dump(svr_new_model, file)
print(data['DESCR'])