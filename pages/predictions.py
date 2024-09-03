import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix

def predictions():
    # Create tabs for Enrollment Success, Academic Success, and Preferred Program Success
    tabs = st.tabs(["Enrollment Success", "Academic Success", "Preferred Program Success"])

    # Load the dataset only once to avoid redundancy
    file_path = "C:/Users/waizz/OneDrive/Documents/GitHub/EduEz/Bruneian_Students_Simulated_Dataset.csv"
    student_data = pd.read_csv(file_path)

    # Label encode the Success_Level and Preferred_Program to create target variables
    label_encoder_success = LabelEncoder()
    student_data['Enroll'] = label_encoder_success.fit_transform(student_data['Success_Level'])
    
    label_encoder_program = LabelEncoder()
    student_data['Program_Success'] = label_encoder_program.fit_transform(student_data['Preferred_Program'])

    # Define the features for the first two predictions
    features = [
        'O_Level_Results', 'A_Level_Results', 'O_Level_Credits', 'A_Level_Credits',
        'Gender', 'Age', 'School_Type', 'District', 'Preferred_Program'
    ]
    X = pd.get_dummies(student_data[features], drop_first=True)

    # Handle missing values if any
    X.fillna(X.median(), inplace=True)

    # First prediction - Enrollment Success
    y_enroll = student_data['Enroll']
    X_train, X_test, y_train, y_test = train_test_split(X, y_enroll, test_size=0.3, random_state=42)

    with tabs[0]:
        st.title('Enrollment Success Prediction with GaussianNB')
        st.markdown("### Overview")

        # Implement Gaussian Naive Bayes
        model = GaussianNB()
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)

        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred, target_names=label_encoder_success.classes_)

        col1, col2 = st.columns([1, 1])

        with col1:
            st.write("### Model Evaluation")
            st.metric(label="Model Accuracy", value=f"{accuracy:.2f}")
            st.write("**Classification Report:**")
            st.text(report)

        with col2:
            st.write("### Confusion Matrix")
            cm = confusion_matrix(y_test, y_pred)
            fig, ax = plt.subplots()
            sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=label_encoder_success.classes_, yticklabels=label_encoder_success.classes_, ax=ax)
            ax.set_xlabel("Predicted")
            ax.set_ylabel("Actual")
            st.pyplot(fig)

    # Second prediction - Academic Success
    y_academic = student_data['Enroll']
    X_train, X_test, y_train, y_test = train_test_split(X, y_academic, test_size=0.3, random_state=42)

    with tabs[1]:
        st.title('Academic Success Prediction with Random Forest')
        st.markdown("### Overview")
        st.write("This tab predicts the likelihood of academic success using the Random Forest Classifier.")

        model = RandomForestClassifier(random_state=42)
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)

        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred, target_names=label_encoder_success.classes_)

        col3, col4 = st.columns([1, 1])

        with col3:
            st.write("### Model Evaluation")
            st.metric(label="Model Accuracy", value=f"{accuracy:.2f}")
            st.write("**Classification Report:**")
            st.text(report)

        with col4:
            st.write("### Feature Importance")
            feature_importance = model.feature_importances_
            sorted_idx = feature_importance.argsort()
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.barh(X.columns[sorted_idx], feature_importance[sorted_idx], color='teal')
            ax.set_xlabel("Feature Importance")
            ax.set_title("Feature Importance in Random Forest Model")
            st.pyplot(fig)

    # Third prediction - Preferred Program Success
    y_program_success = student_data['Program_Success']
    X_train, X_test, y_train, y_test = train_test_split(X, y_program_success, test_size=0.3, random_state=42)

    with tabs[2]:
        st.title('Preferred Program Success Prediction with Random Forest')
        st.markdown("### Overview")
        st.write("This tab predicts the likelihood of success in the preferred program using the Random Forest Classifier.")

        model = RandomForestClassifier(random_state=42)
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)

        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred, target_names=label_encoder_program.classes_)

        col5, col6 = st.columns([1, 1])

        with col5:
            st.write("### Model Evaluation")
            st.metric(label="Model Accuracy", value=f"{accuracy:.2f}")
            st.write("**Classification Report:**")
            st.text(report)

        with col6:
            st.write("### Feature Importance")
            feature_importance = model.feature_importances_
            sorted_idx = feature_importance.argsort()
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.barh(X.columns[sorted_idx], feature_importance[sorted_idx], color='purple')
            ax.set_xlabel("Feature Importance")
            ax.set_title("Feature Importance in Preferred Program Success Model")
            st.pyplot(fig)

# Run the prediction function
if __name__ == "__main__":
    predictions()
