def predictions():
    import streamlit as st
    import pandas as pd
    from sklearn.model_selection import train_test_split, RandomizedSearchCV, cross_val_score
    from sklearn.preprocessing import LabelEncoder
    from sklearn.metrics import accuracy_score
    from xgboost import XGBClassifier, plot_importance
    from imblearn.over_sampling import SMOTE
    from sklearn.metrics import mean_absolute_error
    from xgboost import XGBRegressor
    import numpy as np
    import matplotlib.pyplot as plt

    # Load the dataset
    file_path = "C:/Users/waizz/OneDrive/Documents/GitHub/EduEz/pages/modified_bruneian_students_dataset.csv"
    df = pd.read_csv(file_path)

    # Create tabs for different predictions
    tab1, tab2 = st.tabs(["Enrollment Success Prediction", "O-Level Credits Prediction"])

    with tab1:
        # Split the page into two columns
        col1, col2 = st.columns(2)

        with col1:
            st.title("Enrollment Success Prediction")

        # Add vertical divider (CSS trick)
        st.markdown(
            """
            <style>
            div[data-testid="column"] {
                border-right: 1px solid #d3d3d3;
                padding-right: 10px;
            }
            </style>
            """, unsafe_allow_html=True
        )

        # Feature Engineering
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

        # XGBoost Classifier with Hyperparameter Tuning
        param_distributions = {
            'n_estimators': np.arange(100, 500, 50),
            'learning_rate': np.linspace(0.01, 0.3, 10),
            'max_depth': np.arange(3, 10),
        }

        xgb = XGBClassifier(random_state=42)
        random_search = RandomizedSearchCV(xgb, param_distributions, n_iter=50, cv=3, random_state=42, n_jobs=-1)
        random_search.fit(X_train, y_train)

        best_xgb_model = random_search.best_estimator_
        y_pred_xgb = best_xgb_model.predict(X_test)
        accuracy_xgb = accuracy_score(y_test, y_pred_xgb)

        # Display model evaluation in col1
        with col1:
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
                    <div class="evaluation">Training set size: {len(X_train)}</div>
                    <div class="evaluation">Test set size: {len(X_test)}</div>
                </div>
                """, unsafe_allow_html=True
            )

        # Simple Feature Importance in col2
        with col2:
            st.subheader("Feature Importance")

            # Simple feature importance chart
            fig, ax = plt.subplots(figsize=(6, 3))
            plot_importance(best_xgb_model, ax=ax, height=0.5, max_num_features=5)
            plt.tight_layout()
            plt.grid(False)
            st.pyplot(fig)

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
            prediction = best_xgb_model.predict(user_input)
            
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

    with tab2:
        st.title("O Level Credits Prediction")

        # Feature Engineering for O Level Credits Prediction
        features_credits = ['Gender', 'Age', 'School_Type', 'District', 'Parent_Education_Level', 
                            'Study_Hours', 'Extracurricular_Activities']

        # Assuming 'Extra_Curricular' exists in the dataset, and we need to encode it as binary
        df['Extracurricular_Activities'] = df['Extra_Curricular'].apply(lambda x: 1 if x == 'Yes' else 0)

        target_credits = 'O_Level_Credits'  # The target is the number of O Level credits

        # Split dataset into features (X) and target (y)
        X_credits = df[features_credits]
        y_credits = df[target_credits]

        # Split data into training and test sets
        X_train_credits, X_test_credits, y_train_credits, y_test_credits = train_test_split(
            X_credits, y_credits, test_size=0.2, random_state=42
        )

        # XGBoost Regressor with Refined Hyperparameter Tuning
        param_distributions = {
            'n_estimators': np.arange(200, 1000, 100),  # Increasing n_estimators range
            'learning_rate': np.linspace(0.01, 0.2, 10),  # Narrowing the learning rate range
            'max_depth': np.arange(3, 12),  # Testing more depth values
            'min_child_weight': np.arange(1, 10),  # Adding min_child_weight
            'gamma': [0, 0.1, 0.2],  # Adding gamma regularization
            'subsample': np.linspace(0.7, 1.0, 5),  # Testing different subsample sizes
            'colsample_bytree': np.linspace(0.7, 1.0, 5)  # Testing different column subsample sizes
        }

        xgb_regressor = XGBRegressor(random_state=42)
        random_search_credits = RandomizedSearchCV(xgb_regressor, param_distributions, n_iter=200, cv=5, random_state=42, n_jobs=-1)
        random_search_credits.fit(X_train_credits, y_train_credits)

        best_xgb_model_credits = random_search_credits.best_estimator_
        
        # Evaluate using cross-validation for more reliable results
        cv_scores = cross_val_score(best_xgb_model_credits, X_train_credits, y_train_credits, scoring='neg_mean_absolute_error', cv=5)
        cv_mae = -np.mean(cv_scores)

        y_pred_credits = best_xgb_model_credits.predict(X_test_credits)
        mae_credits = mean_absolute_error(y_test_credits, y_pred_credits)

        # Display model evaluation
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
                <div class="accuracy-lead">Cross-Validated MAE for O Level Credits: {cv_mae:.2f}</div>
                <div class="evaluation">MAE on Test Set: {mae_credits:.2f}</div>
                <div class="evaluation">Training set size: {len(X_train_credits)}</div>
                <div class="evaluation">Test set size: {len(X_test_credits)}</div>
            </div>
            """, unsafe_allow_html=True
        )

        # User Inputs for O Level Credits Prediction
        st.subheader("Enter Student Details for O Level Credits Prediction")

        col1, col2, col3 = st.columns(3)

        # Manually map categorical inputs to encoded values
        gender_map = {'Male': 0, 'Female': 1}
        school_type_map = {'Public': 0, 'Private': 1, 'International': 2}
        district_map = {'Brunei-Muara': 0, 'Tutong': 1, 'Belait': 2, 'Temburong': 3}
        parent_education_map = {'Masters Degree': 0, 'Diploma': 1, 'Degree': 2, 'Postgraduate': 3}

        # Collect categorical user inputs with labels
        with col1:
            gender = st.selectbox("Gender", list(gender_map.keys()), key='gender_credits')
            parent_education = st.selectbox("Parent's Education Level", list(parent_education_map.keys()), key='parent_education_credits')

        with col2:
            age = st.number_input("Age", min_value=16, max_value=25, key='age_credits')  # Numerical input
            school_type = st.selectbox("School Type", list(school_type_map.keys()), key='school_type_credits')

        with col3:
            district = st.selectbox("District", list(district_map.keys()), key='district_credits')
            extracurricular_activities = st.selectbox("Extracurricular Activities", ['Yes', 'No'], key='extracurricular_credits')

        study_hours = st.slider("Weekly Study Hours", 0, 40, 10, key='study_hours_credits')  # Numerical input

        # Convert user input into model format by mapping categorical labels to numeric values
        user_input_credits = pd.DataFrame({
            'Gender': [gender_map[gender]],  # Map 'Male'/'Female' to 0/1
            'Age': [age],
            'School_Type': [school_type_map[school_type]],  # Map school type to numerical values
            'District': [district_map[district]],  # Map district to numerical values
            'Parent_Education_Level': [parent_education_map[parent_education]],  # Map parent education
            'Study_Hours': [study_hours],
            'Extracurricular_Activities': [1 if extracurricular_activities == 'Yes' else 0]  # Binary for extracurricular activities
        }, columns=features_credits)  # Ensure column order matches model training

        # Prediction Button
        if st.button("Predict O Level Credits"):
            prediction_credits = best_xgb_model_credits.predict(user_input_credits)

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
                </style>
                """, unsafe_allow_html=True
            )

            st.markdown(f'<div class="success">Predicted O Level Credits: {prediction_credits[0]:.2f}</div>', unsafe_allow_html=True)