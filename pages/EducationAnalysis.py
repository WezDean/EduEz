

def EducationAnalysis():
    import streamlit as st
    import pandas as pd
    import altair as alt
    import matplotlib.pyplot as plt

    class OLevelGradesChart:
        def __init__(self, df):
            self.df = df

        def generate_chart(self, selected_subject):
            # Filter the DataFrame based on the selected subject
            df_filtered = self.df[['Student_ID', f'O_Level_{selected_subject}']].dropna()
            
            # Count the occurrences of each grade
            grade_counts = df_filtered[f'O_Level_{selected_subject}'].value_counts().reset_index()
            grade_counts.columns = ['Grade', 'Count']

            # Generate bar chart
            chart = alt.Chart(grade_counts).mark_bar().encode(
                x=alt.X('Grade', sort=alt.EncodingSortField(field='Grade', order='ascending')),
                y=alt.Y('Count', scale=alt.Scale(domain=[0, 200])),
                color='Grade'
            ).properties(
                title=f'Grade Distribution for O Level {selected_subject}',
                width=600
            )
            return chart

    class ALevelGradesChart:
        def __init__(self, df):
            self.df = df

        def generate_chart(self, selected_subject):
            # Filter the DataFrame based on the selected subject
            df_filtered = self.df[['Student_ID', f'A_Level_{selected_subject}']].dropna()
            
            # Count the occurrences of each grade
            grade_counts = df_filtered[f'A_Level_{selected_subject}'].value_counts().reset_index()
            grade_counts.columns = ['Grade', 'Count']

            # Generate bar chart
            chart = alt.Chart(grade_counts).mark_bar().encode(
                x=alt.X('Grade', sort=alt.EncodingSortField(field='Grade', order='ascending')),
                y=alt.Y('Count', scale=alt.Scale(domain=[0, 30])),
                color='Grade'
            ).properties(
                title=f'Grade Distribution for A Level {selected_subject}',
                width=600
            )
            return chart

    class OLevelGradeDistribution:
        def __init__(self, df):
            self.df = df

        def generate_pie_chart(self, selected_grade):
            # Filter the DataFrame for the selected grade across all O Level subjects
            o_level_subjects = [col for col in self.df.columns if col.startswith('O_Level_')]
            grade_counts = {}

            for subject in o_level_subjects:
                count = self.df[self.df[subject] == selected_grade].shape[0]
                grade_counts[subject.replace('O_Level_', '')] = count

            # Convert the dictionary to a DataFrame
            df_grade_distribution = pd.DataFrame(list(grade_counts.items()), columns=['Subject', 'Count'])
            df_grade_distribution = df_grade_distribution[df_grade_distribution['Count'] > 0]  # Filter out subjects with zero count

            # Generate pie chart
            chart = alt.Chart(df_grade_distribution).mark_arc().encode(
                theta=alt.Theta(field="Count", type="quantitative"),
                color=alt.Color(field="Subject", type="nominal"),
                tooltip=['Subject', 'Count']
            ).properties(
                title=f'Distribution of Subjects for Grade {selected_grade} (O Level)',
                width=400,
                height=400
            )

            return chart

    class ALevelGradeDistribution:
        def __init__(self, df):
            self.df = df

        def generate_pie_chart(self, selected_grade):
            # Filter the DataFrame for the selected grade across all A Level subjects
            a_level_subjects = [col for col in self.df.columns if col.startswith('A_Level_')]
            grade_counts = {}

            for subject in a_level_subjects:
                count = self.df[self.df[subject] == selected_grade].shape[0]
                grade_counts[subject.replace('A_Level_', '')] = count

            # Convert the dictionary to a DataFrame
            df_grade_distribution = pd.DataFrame(list(grade_counts.items()), columns=['Subject', 'Count'])
            df_grade_distribution = df_grade_distribution[df_grade_distribution['Count'] > 0]  # Filter out subjects with zero count

            # Generate pie chart
            chart = alt.Chart(df_grade_distribution).mark_arc().encode(
                theta=alt.Theta(field="Count", type="quantitative"),
                color=alt.Color(field="Subject", type="nominal"),
                tooltip=['Subject', 'Count']
            ).properties(
                title=f'Distribution of Subjects for Grade {selected_grade} (A Level)',
                width=400,
                height=400
            )

            return chart

    class InstitutionApplicationDistribution:
        def __init__(self, df):
            self.df = df

        def generate_horizontal_bar_chart(self):
            # Count the number of students who applied to each institution
            institution_counts = self.df['Applied_Institution'].value_counts().reset_index()
            institution_counts.columns = ['Institution', 'Count']

            # Generate the horizontal bar chart
            chart = alt.Chart(institution_counts).mark_bar().encode(
                x=alt.X('Count:Q', title='Number of Applications'),
                y=alt.Y('Institution:N', sort='-x', title='Institution'),
                color=alt.Color('Institution:N', legend=None),
                tooltip=['Institution', 'Count']
            ).properties(
                title='Distribution of Applications by Institution',
                width=1200,
                height=400
            ).configure_axis(
                labelFontSize=12,
                titleFontSize=14
            ).configure_title(
                fontSize=16
            )

            return chart

    class OLevelDistributionAltair:
        def __init__(self, df):
            self.df = df

        def plot_distribution(self):
            # Create the histogram for O Level credits using Altair
            chart = alt.Chart(self.df).mark_bar().encode(
                alt.X('O_Level_Credits:Q', bin=alt.Bin(maxbins=13), title='Number of O Level Credits'),
                alt.Y('count()', title='Number of Students')
            ).properties(
                title='Distribution of O Level Credits'
            ).configure_axis(
                labelFontSize=12,
                titleFontSize=14
            ).configure_title(
                fontSize=16
            )

            st.altair_chart(chart, use_container_width=True)

    class ALevelDistributionAltair:
        def __init__(self, df):
            self.df = df

        def plot_distribution(self):
            # Filter out students who didn't take any A Level subjects (null values)
            filtered_df = self.df.dropna(subset=['A_Level_Credits'])

            # Create the histogram for A Level credits using Altair
            chart = alt.Chart(filtered_df).mark_bar().encode(
                alt.X('A_Level_Credits:Q', bin=alt.Bin(maxbins=3), title='Number of A Level Credits'),
                alt.Y('count()', title='Number of Students')
            ).properties(
                title='Distribution of A Level Credits'
            ).configure_axis(
                labelFontSize=12,
                titleFontSize=14
            ).configure_title(
                fontSize=16
            )

            st.altair_chart(chart, use_container_width=True)

    # Load the dataset
    df = pd.read_csv("C:/Users/waizz/OneDrive/Documents/GitHub/EduEz/Bruneian_Students_Simulated_Dataset.csv")

    # List of available O Level subjects
    o_level_subjects = ['Mathematics', 'English', 'Malay_Language', 'Islamic_Religious_Knowledge', 'Chemistry', 
                        'Biology', 'Physics', 'Combined_Science', 'Commerce', 'Economics', 'Computer_Science', 'Additional_Maths']

    # List of available A Level subjects
    a_level_subjects = ['Mathematics', 'English', 'Chemistry', 'Biology', 'Physics', 
                        'Commerce', 'Economics', 'Computer_Science']

    # Instantiate the classes
    o_level_chart = OLevelGradesChart(df)
    a_level_chart = ALevelGradesChart(df)
    o_level_distribution = OLevelGradeDistribution(df)
    a_level_distribution = ALevelGradeDistribution(df)
    institution_distribution = InstitutionApplicationDistribution(df)
    o_level_dist = OLevelDistributionAltair(df)
    a_level_dist = ALevelDistributionAltair(df)

    # Creating the cover header layout
    header_col1, header_col2 = st.columns([1, 2])

    # Adding the title and description on the right
    with header_col1:
        st.title("Student's Data Insights")
        st.write("""
            This section of the Web Application showcases the trends and patterns found in the Simulated Dataset of the Students Data.
        """)

    # Adding the image on the left
    #with header_col2:
        #st.image("books.png", use_column_width=False, width= 400)

    # Custom CSS
    st.markdown("""
        <style>
        /* Style for the tabs */
        div[role="tablist"] > div[role="tab"] {
            background-color: #f0f0f5;
            color: black;
            font-weight: bold;
            margin: 0 5px;
            padding: 10px;
            border-radius: 5px;
        }

        /* Style for the selected tab */
        div[role="tablist"] > div[role="tab"]:first-child {
            background-color: #0066cc;
            color: white;
        }

        /* Style on hover */
        div[role="tablist"] > div[role="tab"]:hover {
            background-color: #d9d9d9;
        }
        
        /* Style for the tab content */
        div[role="tabpanel"] {
            padding: 10px;
            background-color: #f9f9f9;
            border: 1px solid #ddd;
            border-radius: 5px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Display the charts side by side
    tabs = st.tabs(["Results", "Demographics"])
    # EduEZ Tab
    with tabs[0]:
        col1, col2 = st.columns(2)

        with col1:
            # O Level Subject selection
            st.header("O Level Grades")
            selected_o_level_subject = st.selectbox("Select O Level Subject to View:", o_level_subjects)
            st.altair_chart(o_level_chart.generate_chart(selected_o_level_subject))

        with col2:
            # A Level Subject selection
            st.header("A Level Grades")
            selected_a_level_subject = st.selectbox("Select A Level Subject to View:", a_level_subjects)
            st.altair_chart(a_level_chart.generate_chart(selected_a_level_subject))

        col3, col4 = st.columns(2)

        with col3:
            st.header("O Level Grade Distribution")
            selected_o_level_grade = st.selectbox("Select O Level Grade to View:", ['A', 'B', 'C', 'D', 'E', 'U'])
            st.altair_chart(o_level_distribution.generate_pie_chart(selected_o_level_grade))

        with col4:
            st.header("A Level Grade Distribution")
            selected_a_level_grade = st.selectbox("Select A Level Grade to View:", ['A', 'B', 'C', 'D', 'E', 'U'])
            st.altair_chart(a_level_distribution.generate_pie_chart(selected_a_level_grade))

        st.altair_chart(institution_distribution.generate_horizontal_bar_chart())   

        col5, col6 = st.columns(2)

            # O Level Distribution
        with col5:
            o_level_dist.plot_distribution()

            # A Level Distribution
        with col6:
            a_level_dist.plot_distribution()