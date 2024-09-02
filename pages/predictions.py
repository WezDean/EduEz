import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import classification_report, accuracy_score

def predictions():
    tabs = st.tabs(["Enrollment Success", "Academic Success"])

    with tabs[0]:
        # Streamlit app title
        st.title('Student Success Prediction with GaussianNB')

        # File path
        file_path = "C:/Users/waizz/OneDrive/Documents/GitHub/EduEz/Bruneian_Students_Simulated_Dataset.csv"

        # Load the dataset
        student_data = pd.read_csv(file_path)

        # Display the first few rows of the dataset
        st.write("### Data Preview")
        st.write(student_data.head())

        # Label encode the Success_Level to create the target variable 'Enroll'
        label_encoder = LabelEncoder()
        student_data['Enroll'] = label_encoder.fit_transform(student_data['Success_Level'])

        # Define the features and the target variable
        features = [
            'O_Level_Results', 'A_Level_Results', 'O_Level_Credits', 'A_Level_Credits',
            'Gender', 'Age', 'School_Type', 'District', 'Preferred_Program'
        ]
        X = pd.get_dummies(student_data[features], drop_first=True)

        # Handle missing values if any
        X.fillna(X.median(), inplace=True)

        y = student_data['Enroll']

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

        # Initialize and train the GaussianNB model
        model = GaussianNB()
        model.fit(X_train, y_train)

        # Make predictions
        y_pred = model.predict(X_test)

        # Evaluate the model
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred, target_names=label_encoder.classes_)

        # Display the results
        st.write("### Model Evaluation")
        st.write(f"**Accuracy:** {accuracy:.2f}")
        st.write("**Classification Report:**")
        st.text(report)

    with tabs[1]:
        # Streamlit app title
        st.title('Student Success Prediction with Random Forest')

        # File path
        file_path = "C:/Users/waizz/OneDrive/Documents/GitHub/EduEz/Bruneian_Students_Simulated_Dataset.csv"

        # Load the dataset
        student_data = pd.read_csv(file_path)

        # Display the first few rows of the dataset
        st.write("### Data Preview")
        st.write(student_data.head())

        # Label encode the Success_Level to create the target variable 'Enroll'
        label_encoder = LabelEncoder()
        student_data['Enroll'] = label_encoder.fit_transform(student_data['Success_Level'])

        # Define the features and the target variable
        features = [
            'O_Level_Results', 'A_Level_Results', 'O_Level_Credits', 'A_Level_Credits',
            'Gender', 'Age', 'School_Type', 'District', 'Preferred_Program'
        ]
        X = pd.get_dummies(student_data[features], drop_first=True)

        # Handle missing values if any
        X.fillna(X.median(), inplace=True)

        y = student_data['Enroll']

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

        # Initialize and train the RandomForestClassifier
        model = RandomForestClassifier(random_state=42)
        model.fit(X_train, y_train)

        # Make predictions
        y_pred = model.predict(X_test)

        # Evaluate the model
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred, target_names=label_encoder.classes_)

        # Display the results
        st.write("### Model Evaluation")
        st.write(f"**Accuracy:** {accuracy:.2f}")
        st.write("**Classification Report:**")
        st.text(report)

