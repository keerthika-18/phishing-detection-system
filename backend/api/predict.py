import joblib
import pandas as pd

# Load the model
model = joblib.load('../models/phishing_model.pkl')  # Ensure the path is correct

def predict(email_text=None, url=None):
    if email_text:
        text_to_predict = email_text
    elif url:
        text_to_predict = url
    else:
        raise ValueError("Either email_text or url must be provided.")

    # Convert the input into a pandas DataFrame (required for the model's predict method)
    df = pd.DataFrame([{'Text': text_to_predict}])

    # Make a prediction using the loaded model
    prediction = model.predict(df['Text'])

    # Return the prediction (1 for phishing, 0 for safe)
    return prediction[0]

# Test the prediction function
email_test = "This is a phishing email example."
url_test = "https://www.google.com/"

print("Email Prediction:", "Phishing" if predict(email_text=email_test) == 1 else "Safe")
print("URL Prediction:", "Phishing" if predict(url=url_test) == 1 else "Safe")

# Test additional URLs
urls_to_test = [
    "http://phishing-url.com",
    "http://example-phishing-site.com",
    "super1000.info/docs",
    "jbsdbfsdfb.com",
    "google.com",
    "kk"  # This is not a valid URL format
]

for url in urls_to_test:
    result = predict(url=url)
    print(f"URL: {url} - Prediction: {'Phishing' if result == 1 else 'Safe'}")
