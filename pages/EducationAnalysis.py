def EducationAnalysis():
    import streamlit as st
    import pandas as pd
    import plotly.express as px
    import plotly.graph_objects as go
    import numpy as np

    # Inject custom CSS to change the sidebar theme
    st.markdown(
        """
        <style>
        /* Sidebar background color */
        .css-1d391kg {
            background-color: #73c6b6;  /* Teal for sidebar */
        }

        /* Sidebar text color */
        .css-1d391kg .stText, .css-1d391kg .stMarkdown, .css-1d391kg .stSelectbox, .css-1d391kg .stMultiSelect, .css-1d391kg .stSlider {
            color: #ffffff;  /* White text in sidebar */
        }

        /* Sidebar header color */
        .css-1d391kg h1, .css-1d391kg h2, .css-1d391kg h3, .css-1d391kg h4, .css-1d391kg h5, .css-1d391kg h6 {
            color: #ffffff;  /* White headers in sidebar */
        }

        /* Sidebar input field background and text */
        .css-1d391kg .stTextInput, .css-1d391kg .stSelectbox, .css-1d391kg .stMultiSelect, .css-1d391kg .stSlider {
            background-color: #ffffff;  /* White background for input fields */
            color: #2c3e50;  /* Dark text for input fields */
            border-radius: 8px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    

    # Load your dataset
    file_path = "C:/Users/waizz/OneDrive/Documents/GitHub/EduEz/pages/Updated_Bruneian_Students_Simulated_Dataset.csv"
    df = pd.read_csv(file_path)

    # Mapping of O Level and A Level subjects to their corresponding Syllabus Codes
    o_level_subjects = {
        'O_Level_Mathematics': 'Mathematics (Syllabus Code: 4024)',
        'O_Level_English': 'English Language (Syllabus Code: 1120)',
        'O_Level_Malay_Language': 'Bahasa Melayu (Syllabus Code: 3248)',
        'O_Level_Islamic_Religious_Knowledge': 'Islamic Religious Knowledge (Syllabus Code: 2069)',
        'O_Level_Chemistry': 'Chemistry (Syllabus Code: 5070)',
        'O_Level_Biology': 'Biology (Syllabus Code: 5090)',
        'O_Level_Physics': 'Physics (Syllabus Code: 5054)',
        'O_Level_Combined_Science': 'Combined Science (Syllabus Code: 5129)',
        'O_Level_Commerce': 'Commerce (Syllabus Code: 7100)',
        'O_Level_Economics': 'Economics (Syllabus Code: 2281)',
        'O_Level_Computer_Science': 'Computer Science (Syllabus Code: 2210)',
        'O_Level_Additional_Maths': 'Additional Mathematics (Syllabus Code: 4037)'
    }

    a_level_subjects = {
        'A_Level_Mathematics': 'Mathematics (Syllabus Code: 9709)',
        'A_Level_English': 'English Language (Syllabus Code: 9093)',
        'A_Level_Chemistry': 'Chemistry (Syllabus Code: 9701)',
        'A_Level_Biology': 'Biology (Syllabus Code: 9700)',
        'A_Level_Physics': 'Physics (Syllabus Code: 9702)',
        'A_Level_Commerce': 'Commerce (Syllabus Code: 9609)',
        'A_Level_Economics': 'Economics (Syllabus Code: 9708)',
        'A_Level_Computer_Science': 'Computer Science (Syllabus Code: 9608)'
    }

    # Sidebar filters
    st.sidebar.header('Filter Options')
    exam_level = st.sidebar.selectbox('Select Exam Level', ['O Level', 'A Level'])
    school_type = st.sidebar.selectbox('Select School Type', ['All', 'Public', 'Private', 'International'])
    district = st.sidebar.multiselect('Select District', options=df['District'].unique(), default=df['District'].unique())
    gender = st.sidebar.multiselect('Select Gender', options=df['Gender'].unique(), default=df['Gender'].unique())
    age_range = st.sidebar.slider('Select Age Range', min_value=int(df['Age'].min()), max_value=int(df['Age'].max()), value=(int(df['Age'].min()), int(df['Age'].max())))

    # Filter the dataset based on sidebar inputs
    filtered_df = df[
        (df['District'].isin(district)) &
        (df['Gender'].isin(gender)) &
        (df['Age'].between(age_range[0], age_range[1]))
    ]

    if school_type != 'All':
        filtered_df = filtered_df[filtered_df['School_Type'] == school_type]

    # Display results based on exam level
    if exam_level == 'O Level':
        o_level_columns = [col for col in o_level_subjects.keys()]
        o_level_labels = {col: o_level_subjects[col] for col in o_level_columns}
        st.write(f"### O Level Exam Results Analysis")
        
        # Define the grade order for O Level
        o_level_grade_order = ['A1', 'A2', 'B3', 'B4', 'C5', 'C6', 'D7', 'E8', 'U']

        # 1. Bar Chart: Performance in O Level Subjects
        selected_subject = st.selectbox('Select O Level Subject', options=o_level_columns, format_func=lambda x: o_level_labels[x])
        fig = px.histogram(filtered_df, x=selected_subject, color='School_Type', barmode='group',
                        title=f'O Level Performance in {o_level_labels[selected_subject]}',
                        category_orders={selected_subject: o_level_grade_order},  # Set grade order
                        labels={'x': 'Grades', 'y': 'Count'})
        st.plotly_chart(fig)  # This is the first visualization (by itself)

        # 2. Pie Chart: Overall O Level Results Distribution
        fig2 = px.pie(filtered_df, names=selected_subject, title=f'O Level {o_level_labels[selected_subject]} Grade Distribution',
                    category_orders={selected_subject: o_level_grade_order})  # Set grade order

    elif exam_level == 'A Level':  # Ensure that A Level variables are only used within this block
        a_level_columns = [col for col in a_level_subjects.keys()]
        a_level_labels = {col: a_level_subjects[col] for col in a_level_columns}
        st.write(f"### A Level Exam Results Analysis")
        
        # Define the grade order for A Level
        a_level_grade_order = ['A', 'B', 'C', 'D', 'E', 'U']

        # 1. Bar Chart: Performance in A Level Subjects
        selected_subject = st.selectbox('Select A Level Subject', options=a_level_columns, format_func=lambda x: a_level_labels[x])
        fig = px.histogram(filtered_df, x=selected_subject, color='School_Type', barmode='group',
                        title=f'A Level Performance in {a_level_labels[selected_subject]}',
                        category_orders={selected_subject: a_level_grade_order},  # Set grade order
                        labels={'x': 'Grades', 'y': 'Count'})
        st.plotly_chart(fig)  # This is the first visualization (by itself)

        # 2. Pie Chart: Overall A Level Results Distribution
        fig2 = px.pie(filtered_df, names=selected_subject, title=f'A Level {a_level_labels[selected_subject]} Grade Distribution',
                    category_orders={selected_subject: a_level_grade_order})  # Set grade order

    # Display the second and third visualizations side by side
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig2)  # Pie Chart in column 1

    # 3. Box plot for overall results
    if exam_level == 'O Level':
        fig3 = px.box(filtered_df, y='O_Level_Results', color='School_Type', title='O Level Results by School Type')
    else:
        fig3 = px.box(filtered_df, y='A_Level_Results', color='School_Type', title='A Level Results by School Type')

    with col2:
        st.plotly_chart(fig3)  # Box plot in column 2

    # Display the Top 5 and Bottom 5 visualizations side by side

    # 4. Difficulty of Subjects Barcharts
    grade_mapping = {
        'A1': 1, 'A2': 2, 'B3': 3, 'B4': 4, 'C5': 5, 'C6': 6, 'D7': 7, 'E8': 8, 'U': 9,  # O Level
        'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'U': 6  # A Level
    }

    # List of columns that are NOT subjects
    non_subject_columns = ['A_Level_Results', 'O_Level_Results', 'A_Level_Credits', 'O_Level_Credits']

    # Map grades to numerical values for easier calculation of average performance
    for col in df.columns:
        if 'O_Level' in col or 'A_Level' in col:
            if col not in non_subject_columns:  # Exclude non-subject columns
                df[col] = df[col].map(grade_mapping)

    col3, col4 = st.columns(2)

    # Toggle between O Level and A Level
    if exam_level == 'O Level':
        # Calculate the average performance per subject for O Levels, excluding non-subject columns
        o_level_columns = [col for col in df.columns if 'O_Level' in col and col not in non_subject_columns]
        o_level_averages = df[o_level_columns].mean().sort_values()

        # Plot top 5 and bottom 5 performing subjects for O Levels
        top_5_o_level = o_level_averages.head(5)
        bottom_5_o_level = o_level_averages.tail(5)

        # Bar chart for top 5 O Level subjects
        fig_top_o_level = px.bar(top_5_o_level, x=top_5_o_level.index, y=top_5_o_level.values,
                                title='Top 5 Performing O Level Subjects',
                                labels={'x': 'Subject', 'y': 'Average Grade'},
                                color=top_5_o_level.values, color_continuous_scale='Blues')

        # Bar chart for bottom 5 O Level subjects
        fig_bottom_o_level = px.bar(bottom_5_o_level, x=bottom_5_o_level.index, y=bottom_5_o_level.values,
                                    title='Bottom 5 Performing O Level Subjects',
                                    labels={'x': 'Subject', 'y': 'Average Grade'},
                                    color=bottom_5_o_level.values, color_continuous_scale='Reds')

        # Display charts in Streamlit side by side
        with col3:
            st.plotly_chart(fig_top_o_level)

        with col4:
            st.plotly_chart(fig_bottom_o_level)

    elif exam_level == 'A Level':
        # Calculate the average performance per subject for A Levels, excluding non-subject columns
        a_level_columns = [col for col in df.columns if 'A_Level' in col and col not in non_subject_columns]
        a_level_averages = df[a_level_columns].mean().sort_values()

        # Plot top 5 and bottom 5 performing subjects for A Levels
        top_5_a_level = a_level_averages.head(5)
        bottom_5_a_level = a_level_averages.tail(5)

        # Bar chart for top 5 A Level subjects
        fig_top_a_level = px.bar(top_5_a_level, x=top_5_a_level.index, y=top_5_a_level.values,
                                title='Top 5 Performing A Level Subjects',
                                labels={'x': 'Subject', 'y': 'Average Grade'},
                                color=top_5_a_level.values, color_continuous_scale='Blues')

        # Bar chart for bottom 5 A Level subjects
        fig_bottom_a_level = px.bar(bottom_5_a_level, x=bottom_5_a_level.index, y=bottom_5_a_level.values,
                                    title='Bottom 5 Performing A Level Subjects',
                                    labels={'x': 'Subject', 'y': 'Average Grade'},
                                    color=bottom_5_a_level.values, color_continuous_scale='Reds')

        # Display charts in Streamlit side by side
        with col1:
            st.plotly_chart(fig_top_a_level)

        with col2:
            st.plotly_chart(fig_bottom_a_level)

    
    # Divider for Demographics section
    st.divider()
    st.write("## Demographics")

    # Use the filtered dataset for demographics visualizations (applying the universal filters)
    filtered_df_demographics = filtered_df

    # Organize demographic visualizations into columns
    col1, col2 = st.columns(2)

    # 1. Student Gender Distribution (Pie Chart)
    with col1:
        fig_gender = px.pie(filtered_df_demographics, names='Gender', title='Student Gender Distribution')
        st.plotly_chart(fig_gender)

    # 2. Student Age Distribution (Line Chart)
    # Fixing age to be whole numbers
    filtered_df_demographics['Age'] = filtered_df_demographics['Age'].astype(int)

    # Create line chart for age distribution
    age_counts = filtered_df_demographics['Age'].value_counts().sort_index()
    fig_age_line = px.line(x=age_counts.index, y=age_counts.values, title='Student Age Distribution',
                        labels={'x': 'Age', 'y': 'Number of Students'}, markers=True)

    with col2:
        st.plotly_chart(fig_age_line)

    col3, col4 = st.columns(2)

    with col3:
        # Specify the desired order for the districts
        district_order = ['Brunei-Muara', 'Belait', 'Tutong', 'Temburong']

        # 3. Students by District (Bar Chart)
        fig_district = px.bar(filtered_df_demographics, x='District', title='Number of Students by District',
                            labels={'x': 'District', 'y': 'Count'},
                            category_orders={'District': district_order})  # Set the order of districts

        st.plotly_chart(fig_district)

    with col4:
        # 4. Family Income Distribution by District (Box Plot)
        fig_income = px.box(filtered_df, x='District', y='Family_Income', title='Family Income Distribution by District',
                            labels={'Family_Income': 'Family Income', 'District': 'District'},
                            category_orders={'District': district_order})  # Set the order of districts

        st.plotly_chart(fig_income)



    # Divider for Additional Insights section
    st.divider()
    st.write("## Additional Insights")

    # Define the list of subjects (O Level and A Level columns)
    subjects = [col for col in df.columns if 'O_Level' in col or 'A_Level' in col]

    # 1. Study Hours vs. Exam Performance (Bubble Chart)
    # Subject selection for the bubble chart (multiple subjects)
    selected_subjects_bubble = st.multiselect("Select Subjects for Study Hours vs Exam Performance", subjects, default=subjects[:3])

    # Calculate average study hours and average performance for the selected subjects
    average_study_hours = df.groupby('Study_Hours')[selected_subjects_bubble].mean().reset_index()

    # Reshape the dataframe to long format for easier plotting
    long_df_bubble = average_study_hours.melt(id_vars='Study_Hours', var_name='Subject', value_name='Average_Grade')

    # Bubble chart for selected subjects
    fig_bubble = px.scatter(long_df_bubble, x='Study_Hours', y='Average_Grade', size='Average_Grade',
                            color='Subject', title='Study Hours vs Exam Performance (Bubble Chart)',
                            labels={'Study_Hours': 'Study Hours', 'Average_Grade': 'Average Grade'},
                            hover_name='Subject', size_max=60)

    st.plotly_chart(fig_bubble)

    # Specify the desired order for the districts
    district_order = ['Brunei-Muara', 'Belait', 'Tutong', 'Temburong']

    # 2. Performance by District (Bar Chart)
    # Subject selection for the bar chart (multiple subjects)
    selected_subjects_district = st.multiselect("Select Subjects for Performance by District", subjects, default=subjects[:3])

    # Calculate average performance per district for the selected subjects
    average_performance_by_district = df.groupby('District')[selected_subjects_district].mean().reset_index()

    # Reshape the dataframe to long format for easier plotting
    long_district_df = average_performance_by_district.melt(id_vars='District', var_name='Subject', value_name='Average_Grade')

    # Bar chart for performance by district with ordered categories
    fig_district = px.bar(long_district_df, x='District', y='Average_Grade', color='Subject', barmode='group',
                        title='Performance by District', labels={'District': 'District', 'Average_Grade': 'Average Grade'},
                        category_orders={'District': district_order})  # Set the order of districts

    st.plotly_chart(fig_district)






