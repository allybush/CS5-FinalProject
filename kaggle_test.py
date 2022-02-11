# from - https://www.kaggle.com/keynyim/music-genre-classification-30-secs-81-accuracy

import warnings
warnings.simplefilter("ignore", UserWarning)

import os
from tqdm import tqdm
import pickle

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

import librosa

from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import RFECV,mutual_info_regression
from sklearn.metrics import confusion_matrix, accuracy_score,classification_report
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.decomposition import PCA

from xgboost import XGBClassifier

#For hyperparameter tuning
from hyperopt import STATUS_OK, Trials, fmin, hp, tpe


df = pd.read_csv('../input/gtzan-dataset-music-genre-classification/Data/features_30_sec.csv')
df.head()

df.label.value_counts()
df.info()
df.describe()

songs_path = '../input/gtzan-dataset-music-genre-classification/Data/genres_original'


def extract_new_features(song_path, num_files=1000, num_new_features=8):
    data_array = np.empty([num_files, num_new_features])

    counter = 0
    for root, dirs, files in os.walk(songs_path):
        dirs.sort()
        for file, i in zip(sorted(files), tqdm(range(num_files))):
            i = i + (counter - 1) * 100
            file_path = os.path.join(root, file)

            try:
                # extract mean and variance of those 4 features
                y, sr = librosa.load(os.fspath(file_path))
                chroma_cens = librosa.feature.chroma_cens(y=y, sr=sr)
                spectral_contrast = librosa.feature.spectral_contrast(y=y, sr=sr)
                spectral_flatness = librosa.feature.spectral_flatness(y=y)
                tonnetz = librosa.feature.tonnetz(y=y, sr=sr)

                data_array[i, 0] = np.mean(chroma_cens)
                data_array[i, 1] = np.var(chroma_cens)
                data_array[i, 2] = np.mean(spectral_contrast)
                data_array[i, 3] = np.var(spectral_contrast)
                data_array[i, 4] = np.mean(spectral_flatness)
                data_array[i, 5] = np.var(spectral_flatness)
                data_array[i, 6] = np.mean(tonnetz)
                data_array[i, 7] = np.var(tonnetz)

            # Set all values to zero for files with problems
            except:
                print(f'Problem file: {file_path}')
                for j in range(num_new_features):
                    data_array[i, j] = 0

        counter += 1

    return data_array


new_features_array = extract_new_features('../input/gtzan-dataset-music-genre-classification/Data/genres_original')

#Add those new features back to the original dataframe

df['chroma_cens_mean'] = new_features_array[:,0]
df['chroma_cens_var'] = new_features_array[:,1]
df['spectral_contrast_mean'] = new_features_array[:,2]
df['spectral_contrast_var'] = new_features_array[:,3]
df['spectral_flatness_mean'] = new_features_array[:,4]
df['spectral_flatness_var'] = new_features_array[:,5]
df['tonnetz_mean'] = new_features_array[:,6]
df['tonnetz_var'] = new_features_array[:,7]

for i in range(-8,0,1):
    # Filter out the jazz genre except jazz.0054
    df.iloc[554,i] = df[ df.label == 'jazz'].iloc[np.r_[np.arange(0,54),np.arange(55,100)],i].mean()

# Save as a new csv
df.to_csv('new_csv', index=False)
#Exclude filename and Length
df = df.iloc[:,2:]

corr = df.corr()

#Create a mask for the heatmap
mask = np.zeros_like(corr)
mask[np.triu_indices_from(mask)] = True

plt.subplots(figsize=(20, 20))
sns.heatmap(corr, mask=mask, cmap="vlag")

sol = (corr.where(np.triu(np.ones(corr.shape), k=1).astype(np.bool))
                  .stack()
                  .sort_values(ascending=False))
for index, value in sol.items():
    if (value > 0.75) or (value < -0.75):
        print(index, value)


y = df.label
X = df

#Use `label` to split data evenly and drop `label` column after split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, stratify=df.label, random_state=77)
X_train.drop('label',axis=1,inplace=True)
X_test.drop('label',axis=1,inplace=True)


sc = StandardScaler()
X_train_scaled = sc.fit_transform(X_train)
X_train = pd.DataFrame(X_train_scaled, index=X_train.index, columns=X_train.columns)
X_test_scaled = sc.transform(X_test)
X_test = pd.DataFrame(X_test_scaled, index=X_test.index, columns=X_test.columns)

estimator = XGBClassifier(eval_metric='merror')
rfecv = RFECV(estimator, step=1, cv=5,scoring='accuracy',verbose=1)
rfecv.fit(X_train, y_train)

# See which features can be eliminated
features_drop_array = list(np.where(rfecv.support_ == False)[0])
X_train.columns[features_drop_array]

X_train.drop(X_train.columns[features_drop_array], axis=1, inplace=True)
X_test.drop(X_test.columns[features_drop_array], axis=1, inplace=True)

model = XGBClassifier(n_estimators=1000)
model.fit(X_train,y_train,eval_metric='merror')

y_pred_train = model.predict(X_train)
y_pred_test = model.predict(X_test)
target_names = sorted(set(y))

print(f'Training accuracy: {accuracy_score(y_train,y_pred_train)}')
print(f'Training:\n {classification_report(y_train, y_pred_train, labels=target_names)}')
print(f'Testing accuracy: {accuracy_score(y_test,y_pred_test)}')
print(f'Testing:\n {classification_report(y_test, y_pred_test, labels=target_names)}')

#Confusion matrix of the test data
cm = confusion_matrix(y_test, y_pred_test)
plt.figure(figsize = (16, 9))
sns.heatmap(cm,cmap="Blues", annot=True, xticklabels = target_names, yticklabels = target_names )

space = {
    'n_estimators': hp.quniform('n_estimators', 0, 3000, 1),
    'reg_lambda': hp.quniform('reg_lambda', 0, 500, 1),
}


def objective(space):
    clf = XGBClassifier(
        n_estimators=int(space['n_estimators']),
        reg_lambda=int(space['reg_lambda']),
    )

    evaluation = [(X_train, y_train), (X_test, y_test)]

    clf.fit(X_train, y_train,
            eval_set=evaluation, eval_metric="auc",
            early_stopping_rounds=10, verbose=False)

    pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test, pred)
    return {'loss': -accuracy, 'status': STATUS_OK}


trials = Trials()
best_hyperparams = fmin(fn=objective,
                        space=space,
                        algo=tpe.suggest,
                        max_evals=100,
                        trials=trials)

print(f"best params: {best_hyperparams}")


model1 = XGBClassifier(n_estimators=304, reg_lambda=25)
model1.fit(X_train,y_train,eval_metric='merror')
y_pred_test1 = model1.predict(X_test)
print(f"accuracy: {accuracy_score(y_test,y_pred_test1)}")
print(f'New tuned model:\n {classification_report(y_test, y_pred_test1, labels=target_names)}')

pickle.dump(sc, open('sc.pkl','wb'))
pickle.dump(model1, open('model.pkl', 'wb'))