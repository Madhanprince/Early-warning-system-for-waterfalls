import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder, label_binarize
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, roc_curve, auc
from sklearn.multiclass import OneVsRestClassifier

# Load Data
data = pd.read_csv('waterfall_risk_simulation.csv')

# Strip extra spaces in column names
data.columns = data.columns.str.strip()

# Drop NaN values
data.dropna(inplace=True)

# Prepare features and target
X = data.drop('Risk Level', axis=1)
y = data['Risk Level']

# Label encode the target variable
le = LabelEncoder()
y = le.fit_transform(y)

# Train-test split (Stratify for imbalanced data if necessary)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Standardize features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Use OneVsRestClassifier for proper multiclass ROC AUC
base_estimator = RandomForestClassifier(n_estimators=100, random_state=42)
ovr_classifier = OneVsRestClassifier(base_estimator)
ovr_classifier.fit(X_train, label_binarize(y_train, classes=np.unique(y)))

# Predictions
y_pred = ovr_classifier.predict(X_test)

# Evaluate
accuracy = accuracy_score(y_test, y_pred.argmax(axis=1))
print(f"Accuracy: {accuracy * 100:.2f}%")

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred.argmax(axis=1))
plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=le.classes_, yticklabels=le.classes_)
plt.xlabel('Predicted')
plt.ylabel('True')
plt.title('Confusion Matrix')
plt.show()


# Classification Report
print(classification_report(y_test, y_pred.argmax(axis=1), target_names=le.classes_))



# ROC Curve - Using OneVsRestClassifier's predict_proba
fpr = dict()
tpr = dict()
roc_auc = dict()
y_test_bin = label_binarize(y_test, classes=np.unique(y))  # Binarize y_test

for i in range(len(le.classes_)):
    fpr[i], tpr[i], _ = roc_curve(y_test_bin[:, i], ovr_classifier.predict_proba(X_test)[:, i])
    roc_auc[i] = auc(fpr[i], tpr[i])

# Plot ROC Curve
plt.figure(figsize=(6, 5))
colors = ['blue', 'green', 'red']  # Adjust colors if more than 3 classes
for i in range(len(le.classes_)):
    plt.plot(fpr[i], tpr[i], color=colors[i % len(colors)], lw=2,
             label=f'ROC curve of class {le.classes_[i]} (area = {roc_auc[i]:.2f})')

plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic example')
plt.legend(loc="lower right")
plt.show()



# Feature Importance
importances = ovr_classifier.estimators_[0].feature_importances_
indices = np.argsort(importances)[::-1]
plt.figure(figsize=(8, 6))
plt.title('Feature Importances')
plt.barh(range(len(indices)), importances[indices], align="center")
plt.yticks(range(len(indices)), X.columns[indices])
plt.xlabel('Relative Importance')
plt.show()