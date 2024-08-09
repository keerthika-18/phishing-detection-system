import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os

# Load the datasets
email_df = pd.read_csv('dataset/phishing_email_dataset.csv')
url_df = pd.read_csv('dataset/phishing_url_dataset.csv')

# Combine both datasets
email_df['Text'] = email_df['Email Text']
url_df['Text'] = url_df['URL']
combined_df = pd.concat([email_df[['Text', 'Email Type']], url_df.rename(columns={'Label': 'Email Type'})])

# Features and Labels
X = combined_df['Text']
y = combined_df['Email Type']

# Create a pipeline with TF-IDF vectorization and Random Forest classifier
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(stop_words='english')),
    ('rf', RandomForestClassifier(n_estimators=100, random_state=42))
])

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model using the pipeline
pipeline.fit(X_train, y_train)

# Model Evaluation
y_pred = pipeline.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, y_pred)}")
print(classification_report(y_test, y_pred))

# Save the model
output_dir = 'backend/models'
os.makedirs(output_dir, exist_ok=True)
model_path = os.path.join(output_dir, 'phishing_model.pkl')
joblib.dump(pipeline, model_path)
print(f"Model saved as '{model_path}'")


# import joblib
# import pandas as pd
# import re
# import os
# from sklearn.impute import SimpleImputer
# from sklearn.pipeline import Pipeline
# from sklearn.preprocessing import StandardScaler
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.metrics import classification_report, accuracy_score
# from sklearn.model_selection import train_test_split, cross_val_score

# # Load datasets
# try:
#     emails_df = pd.read_csv('dataset/Phishing_Email.csv', quoting=3, on_bad_lines='skip', encoding='utf-8')
#     urls_df = pd.read_csv('dataset/phishing_site_urls.csv', quoting=3, on_bad_lines='skip', encoding='utf-8')
# except pd.errors.ParserError as e:
#     print(f"Error reading CSV files: {e}")
#     exit()

# # Clean data
# emails_df = emails_df.dropna(subset=['Email Text'])
# urls_df = urls_df.dropna(subset=['URL'])

# # Add labels
# emails_df['label'] = 1  # Assuming all emails in this dataset are phishing
# urls_df['label'] = 1  # Assuming all URLs in this dataset are phishing

# # Feature extraction functions
# def extract_features_email(df):
#     features = pd.DataFrame()
#     features['length'] = df['Email Text'].apply(len)
#     # Add more features here if needed
#     return features

# def extract_features_url(df):
#     features = pd.DataFrame()
#     features['length'] = df['URL'].apply(len)
#     features['num_dots'] = df['URL'].apply(lambda x: x.count('.'))
#     features['has_ip'] = df['URL'].apply(lambda x: bool(re.search(r'\d+\.\d+\.\d+\.\d+', x)))
#     # Add more features here if needed
#     return features

# # Extract features from email and URL datasets
# email_features = extract_features_email(emails_df)
# url_features = extract_features_url(urls_df)

# # Combine the datasets into one for training
# email_data = pd.concat([email_features, emails_df['label']], axis=1)
# url_data = pd.concat([url_features, urls_df['label']], axis=1)
# final_data = pd.concat([email_data, url_data], ignore_index=True)

# # Prepare data for training
# X = final_data.drop('label', axis=1)
# y = final_data['label']

# # Ensure the data is consistent and properly formatted
# print("X shape:", X.shape)
# print("y shape:", y.shape)
# print("Sample X:", X.head())
# print("Sample y:", y.head())

# # Split the data into training and testing sets
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # Train the model using a pipeline
# pipeline = Pipeline([
#     ('imputer', SimpleImputer(strategy='mean')),
#     ('scaler', StandardScaler()),
#     ('model', RandomForestClassifier(n_estimators=100, random_state=42))
# ])

# # Run cross-validation to check for overfitting and to ensure it works without errors
# try:
#     scores = cross_val_score(pipeline, X, y, cv=5)
#     print(f"Cross-Validation Scores: {scores}")
#     print(f"Mean Accuracy: {scores.mean()}")
# except Exception as e:
#     print(f"Error during cross-validation: {e}")

# # Fit the model
# pipeline.fit(X_train, y_train)

# # Evaluate the model on the test set
# y_pred = pipeline.predict(X_test)
# print(f"Test Accuracy: {accuracy_score(y_test, y_pred)}")
# print(classification_report(y_test, y_pred))

# # Save the trained model
# output_dir = 'backend/models'
# os.makedirs(output_dir, exist_ok=True)
# model_path = os.path.join(output_dir, 'phishing_model.pkl')
# joblib.dump(pipeline, model_path)
# print(f"Model saved as '{model_path}'")


# # # Save the model
# # joblib.dump(pipeline, 'backend/models/phishing_model.pkl')
# # print("Model saved as 'backend/models/phishing_model.pkl'")
