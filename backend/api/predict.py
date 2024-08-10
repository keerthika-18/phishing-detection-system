import pandas as pd
import joblib
import os

model_path = '../models/phishing_model_best.pkl'
if not os.path.exists(model_path):
    print(f"Model file not found: {model_path}")
else:
    model = joblib.load(model_path)
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


# url_test = "http://www.google.com"
# email_test = "This is a phishing email example."
# print("URL Prediction:", "safe" if predict(text=url_test, content_type='url') == 1 else "phishing")
# print("Email Prediction:", "safe" if predict(text=email_test, content_type='email') == 1 else "phishing")

safe_email = "This is a legitimate email."
phishing_email = "Please click this link to update your bank account."
safe_url1 = "http://www.example.com"
phishing_url1 = "www.1up.com/do/gameOverview?cId=3159391"

print("Safe Email Prediction:", model.predict([safe_email]))
print("Phishing Email Prediction:", model.predict([phishing_email]))
print("Safe URL Prediction:", model.predict([safe_url1]))
print("Phishing URL Prediction:", model.predict([phishing_url1]))
# Test a specific phishing URL
phishing_url = "http://wwwdsfsdgsdg-site.m"
prediction = predict(phishing_url, content_type='url')
print(f"Prediction for '{phishing_url}': {'safe' if prediction == 'Legitimate' else 'phishing'}")

