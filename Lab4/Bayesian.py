import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from pgmpy.models import BayesianModel
from pgmpy.estimators import ParameterEstimator, BayesianEstimator
from pgmpy.inference import VariableElimination

# Load the dataset
data = pd.read_csv('2020_bn_nb_data.txt')

# Display the first few rows of the dataset
print(data.head())

# Convert grades into numerical values for easier processing
grade_mapping = {
    'AA': 4, 'AB': 3.5, 'BB': 3, 'BC': 2.5,
    'CC': 2, 'CD': 1.5, 'DD': 1, 'F': 0
}
data['EC100'] = data['EC100'].map(grade_mapping)
data['IT101'] = data['IT101'].map(grade_mapping)
data['MA101'] = data['MA101'].map(grade_mapping)
data['PH100'] = data['PH100'].map(grade_mapping)

# Prepare data for Naive Bayes Classifier
X = data[['EC100', 'IT101', 'MA101']]
y = data['InternshipQualification']  # Assuming this column has 'Yes'/'No'
y = y.map({'Yes': 1, 'No': 0})  # Convert to binary values

# Split the data into training and testing sets (70-30 split)
accuracy_list = []
for i in range(20):  # Repeat for 20 random splits
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=i)

    # Train Naive Bayes Classifier
    model_nb = GaussianNB()
    model_nb.fit(X_train, y_train)

    # Test the classifier
    accuracy = model_nb.score(X_test, y_test)
    accuracy_list.append(accuracy)
    print(f'Iteration {i + 1} - Naive Bayes Classifier Accuracy: {accuracy * 100:.2f}%')

# Average accuracy for Naive Bayes
average_accuracy_nb = np.mean(accuracy_list)
print(f'Average Naive Bayes Classifier Accuracy: {average_accuracy_nb * 100:.2f}%')

# Prepare data for Bayesian Network
# Define the structure of the Bayesian network
model_bn = BayesianModel([('EC100', 'PH100'), ('IT101', 'PH100'), ('MA101', 'PH100')])

# Fit the model using Bayesian Estimator
model_bn.fit(data, estimator=BayesianEstimator)

# Perform inference
inference = VariableElimination(model_bn)

# Example prediction for PH100 grade based on specific grades
query_result = inference.query(variables=['PH100'], evidence={'EC100': 1, 'IT101': 2, 'MA101': 1.5})
print("Predicted Probability Distribution for PH100 given grades:")
print(query_result)
Week