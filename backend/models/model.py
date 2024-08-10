import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score
import joblib

# Load the datasets
email_df = pd.read_csv('dataset/phishing_email_dataset.csv')
url_df = pd.read_csv('dataset/phishing_url_dataset.csv')

# Combine both datasets
email_df['Text'] = email_df['Email Text']
url_df['Text'] = url_df['URL']
combined_df = pd.concat([email_df[['Text', 'Email Type']], url_df.rename(columns={'Label': 'Email Type'})])

# Standardize label names by converting them to lowercase
combined_df['Email Type'] = combined_df['Email Type'].str.lower()

# Optionally combine minor classes into 'phishing'
combined_df['Email Type'] = combined_df['Email Type'].replace({'defacement': 'phishing', 'malware': 'phishing'})

# Filter out very rare classes if necessary
combined_df = combined_df[combined_df['Email Type'].isin(['legitimate', 'phishing'])]

# Features and Labels
X = combined_df['Text']
y = combined_df['Email Type']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Define the pipeline with class weight and adjusted n_estimators
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(stop_words='english')),  # Vectorize text data
    ('rf', RandomForestClassifier(random_state=42, class_weight='balanced'))  # Classify with Random Forest
])

# Hyperparameter tuning using GridSearchCV
param_grid = {
    'rf__n_estimators': [50, 100, 200],
    'rf__max_depth': [None, 10, 20],
    'rf__min_samples_split': [2, 5, 10],
    'rf__min_samples_leaf': [1, 2, 4]
}

grid_search = GridSearchCV(pipeline, param_grid, cv=5, scoring='accuracy')
grid_search.fit(X_train, y_train)

# Best parameters and model evaluation
print("Best parameters found: ", grid_search.best_params_)
print("Best cross-validation accuracy: ", grid_search.best_score_)

# Evaluate the best model on the test set
best_model = grid_search.best_estimator_
y_pred = best_model.predict(X_test)
print(f"Test Accuracy: {accuracy_score(y_test, y_pred)}")
print(classification_report(y_test, y_pred, zero_division=0))  # Use zero_division to handle undefined metrics

# Save the best model
model_filename = 'phishing_model_best.pkl'
joblib.dump(best_model, model_filename)
print(f"Model saved as '{model_filename}' in the current directory.")

# Load the saved model for prediction
model = joblib.load(model_filename)

# Example usage
example_text = ["http://secure-1121-banking.com"]
prediction = model.predict(example_text)
print(f"Predicted class for '{example_text[0]}': {prediction[0]}")

def predict(text, content_type='email'):
    # Assuming content_type can be 'email' or 'url'
    if content_type == 'email':
        features = pd.DataFrame({'Text': [text]})
    elif content_type == 'url':
        features = pd.DataFrame({'Text': [text]})
    else:
        raise ValueError("Unsupported content type")
    
    prediction = model.predict(features['Text'])
    return prediction[0]

# Test with known phishing and safe examples
safe_email = "This is a legitimate email."
phishing_email = "Please click this link to update your bank account."
safe_url1 = "http://www.example.com"
phishing_url1 = "http://www.phishing-site.com"
uu="xbox360.gamespy.com/xbox-360/condemned-2-bloodshot/"
print("Safe Email Prediction:", model.predict([safe_email]))
print("Phishing Email Prediction:", model.predict([phishing_email]))
print("Safe URL Prediction:", model.predict([safe_url1]))
print("Phishing URL Prediction:", model.predict([phishing_url1]))
print("Safe URL Prediction:", model.predict([uu]))

# # Additional predictions
# url_test = "http://www.google.com"
# email_test = "This is a phishing email example."
# print("URL Prediction:", "phishing" if predict(text=url_test, content_type='url') == 1 else "safe")
# print("Email Prediction:", "phishing" if predict(text=email_test, content_type='email') == 1 else "safe")


