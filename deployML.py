import pandas as pd
import streamlit as st
import pickle
import boto3

# Function to load the model from AWS S3
aws_access_key_id = 'AKIAQDWKCAWVJRO7VVUG'
aws_secret_access_key = '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'
s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

def load_model_from_s3(bucket_name, model_key):
    response = s3.get_object(Bucket=bucket_name, Key=model_key)
    model = pickle.loads(response['Body'].read())
    return model

# AWS S3 configuration
aws_bucket_name = 'mlalgodeploy'
model_key = 'voting_classifier_model.pkl'

# Load the model from AWS S3
loaded_model = load_model_from_s3(aws_bucket_name, model_key)

# Function to perform intrusion prediction
def intrusion_prediction(X_test):
    pred = loaded_model.predict(X_test)
    malicious_count = (pred == 0).sum()
    non_malicious_count = (pred == 1).sum()
    return malicious_count, non_malicious_count

# Streamlit app
def main():
    # Set page title and icon
    st.set_page_config(page_title="DDoS Prediction App", page_icon="🛡️")

    # Header
    st.title('DDoS Prediction App')
    st.subheader('Upload a CSV file to predict network intrusion')

    # File Upload
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

    if uploaded_file is not None:
        # Read the uploaded file into a Pandas DataFrame
        X_test = pd.read_csv(uploaded_file)

        # Display the DataFrame
        st.write("Uploaded DataFrame:")
        st.dataframe(X_test)

        # Perform prediction or other processing based on the uploaded file
        # ...

        # Prediction Button
        if st.button('Predict Network Intrusion'):
            malicious_count, non_malicious_count = intrusion_prediction(X_test)

            # Display Results
            st.success("Prediction Results:")
            st.info(f"Count of Malicious DDoS: {malicious_count} times")
            st.info(f"Count of Non-Malicious DDoS: {non_malicious_count} times")

if __name__ == '__main__':
    main()
