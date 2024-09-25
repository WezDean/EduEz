def predictions():
    import streamlit as st
    import pandas as pd
    from sklearn.model_selection import train_test_split, RandomizedSearchCV
    from sklearn.preprocessing import LabelEncoder
    from sklearn.metrics import accuracy_score
    from xgboost import XGBClassifier
    from xgboost import plot_importance
    from lightgbm import LGBMClassifier
    from sklearn.ensemble import StackingClassifier, RandomForestClassifier
    from imblearn.over_sampling import SMOTE
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns

    # Load the dataset
    file_path = "C:/Users/waizz/OneDrive/Documents/GitHub/EduEz/pages/Updated_Bruneian_Students_Simulated_Dataset.csv"
    df = pd.read_csv(file_path)

    st.title("Comprehensive Model Improvement for Enrollment Success Prediction")

    # Feature Engineering: Break down performance by subject or credits
    features = ['Gender', 'Age', 'School_Type', 'District', 'Parent_Education_Level', 
                'O_Level_Credits', 'A_Level_Credits', 'Preferred_Program', 'Study_Hours']
    target = 'Enrolled'

    # Encode categorical variables
    label_encoders = {}
    for column in ['Gender', 'School_Type', 'District', 'Parent_Education_Level', 'Preferred_Program']:
        le = LabelEncoder()
        df[column] = le.fit_transform(df[column])
        label_encoders[column] = le

    # Split dataset into features (X) and target (y)
    X = df[features]
    y = df[target]

    # Handle class imbalance using SMOTE
    smote = SMOTE(random_state=42)
    X_resampled, y_resampled = smote.fit_resample(X, y)

    # Split data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.2, random_state=42)

    ### Step 1: XGBoost with Hyperparameter Tuning
    param_distributions = {
        'n_estimators': np.arange(100, 1000, 100),
        'learning_rate': np.linspace(0.01, 0.3, 30),
        'max_depth': np.arange(3, 15),
        'min_child_weight': np.arange(1, 10),
        'subsample': np.linspace(0.5, 1, 10),
        'colsample_bytree': np.linspace(0.5, 1, 10)
    }

    xgb = XGBClassifier(random_state=42)
    random_search = RandomizedSearchCV(xgb, param_distributions, n_iter=100, cv=3, random_state=42, n_jobs=-1)
    random_search.fit(X_train, y_train)

    best_xgb_model = random_search.best_estimator_
    y_pred_xgb = best_xgb_model.predict(X_test)
    accuracy_xgb = accuracy_score(y_test, y_pred_xgb)

    ### Step 2: LightGBM Classifier
    lgbm = LGBMClassifier(random_state=42)
    lgbm.fit(X_train, y_train)
    y_pred_lgbm = lgbm.predict(X_test)
    accuracy_lgbm = accuracy_score(y_test, y_pred_lgbm)

    ### Step 3: Stacking Ensemble (XGBoost + Random Forest)
    estimators = [
        ('xgb', best_xgb_model),
        ('rf', RandomForestClassifier(random_state=42))
    ]

    stacking_model = StackingClassifier(estimators=estimators, final_estimator=LGBMClassifier(random_state=42))
    stacking_model.fit(X_train, y_train)

    y_pred_stack = stacking_model.predict(X_test)
    accuracy_stack = accuracy_score(y_test, y_pred_stack)

    # Display model evaluation in a CSS-formatted box with model accuracy leading
    st.markdown(
        f"""
        <style>
        .model-eval-box {{
            background-color: #f9f9f9;
            border-left: 4px solid #3498db;
            padding: 15px;
            margin-top: 10px;
            font-family: Arial, sans-serif;
        }}
        .accuracy-lead {{
            color: #2ecc71;
            font-size: 24px;
            font-weight: bold;
        }}
        .evaluation {{
            font-size: 16px;
            color: #555;
        }}
        </style>

        <div class="model-eval-box">
            <div class="accuracy-lead">XGBoost Accuracy: {accuracy_xgb * 100:.2f}%</div>
            <div class="accuracy-lead">LightGBM Accuracy: {accuracy_lgbm * 100:.2f}%</div>
            <div class="accuracy-lead">Stacking Model Accuracy: {accuracy_stack * 100:.2f}%</div>
            <div class="evaluation">Best Model: Stacking (XGBoost + Random Forest)</div>
            <div class="evaluation">Training set size: {len(X_train)}</div>
            <div class="evaluation">Test set size: {len(X_test)}</div>
        </div>
        """, unsafe_allow_html=True
    )

    # User Inputs for Prediction
    st.subheader("Enter Student Details for Prediction")

    col1, col2, col3 = st.columns(3)

    with col1:
        gender = st.selectbox("Gender", label_encoders['Gender'].classes_)
        preferred_program = st.selectbox("Preferred Program", label_encoders['Preferred_Program'].classes_)

    with col2:
        age = st.number_input("Age", min_value=16, max_value=25)
        school_type = st.selectbox("School Type", label_encoders['School_Type'].classes_)

    with col3:
        district = st.selectbox("District", label_encoders['District'].classes_)
        parent_education = st.selectbox("Parent's Education Level", label_encoders['Parent_Education_Level'].classes_)

    o_level_credits = st.number_input("O Level Credits Obtained", min_value=0, max_value=9)
    a_level_credits = st.number_input("A Level Credits Obtained (if applicable)", min_value=0, max_value=5)
    study_hours = st.slider("Weekly Study Hours", 0, 40, 10)

    # Convert user input into model format
    user_input = pd.DataFrame({
        'Gender': [label_encoders['Gender'].transform([gender])[0]],
        'Age': [age],
        'School_Type': [label_encoders['School_Type'].transform([school_type])[0]],
        'District': [label_encoders['District'].transform([district])[0]],
        'Parent_Education_Level': [label_encoders['Parent_Education_Level'].transform([parent_education])[0]],
        'O_Level_Credits': [o_level_credits],
        'A_Level_Credits': [a_level_credits],
        'Preferred_Program': [label_encoders['Preferred_Program'].transform([preferred_program])[0]],
        'Study_Hours': [study_hours]
    })

    # Prediction Button
    if st.button("Predict Enrollment Success"):
        # Make prediction with the Stacking Model (best model)
        prediction = stacking_model.predict(user_input)
        
        st.markdown(
            f"""
            <style>
            .success {{
                color: green;
                font-size: 24px;
                font-weight: bold;
                border: 2px solid green;
                padding: 10px;
                border-radius: 5px;
                background-color: #eaffea;
            }}
            .failure {{
                color: red;
                font-size: 24px;
                font-weight: bold;
                border: 2px solid red;
                padding: 10px;
                border-radius: 5px;
                background-color: #ffeded;
            }}
            </style>
            """, unsafe_allow_html=True
        )
        
        if prediction[0] == 1:
            st.markdown('<div class="success">This student is likely to successfully enroll.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="failure">This student may not successfully enroll.</div>', unsafe_allow_html=True)
