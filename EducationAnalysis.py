import streamlit as st
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt

# Set page config
st.set_page_config(layout="wide")

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
df = pd.read_csv("C:/Users/waizz/OneDrive/Documents/School/Semester 5/fyp/Bruneian_Students_Simulated_Dataset.csv")

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
    st.title("EduEZ: Educational Pathways Recommendation System")
    st.write("""
        EduEZ is designed to help students explore potential educational pathways based on their O Level and A Level results. 
        Simply input your grades, and we'll recommend institutions and programs that match your qualifications.
    """)

# Adding the image on the left
with header_col2:
    st.image("SDG4.jpg", use_column_width=True)  # Replace with your image path or URL

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
tabs = st.tabs(["Results Analysis", "EduEz"])
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

with tabs[1]:
    import streamlit as st
    import pandas as pd

    # Title and header
    st.title("EduEZ: Educational Pathways Recommendation System")
    st.header("Enter your O Level / A Level results to find eligible institutions")

    # List of subjects
    o_level_subjects = [
        'Mathematics', 'English', 'Malay Language', 'Islamic Religious Knowledge', 
        'Chemistry', 'Biology', 'Physics', 'Combined Science', 
        'Commerce', 'Economics', 'Computer Science', 'Additional Maths'
    ]
    a_level_subjects = [
        'Mathematics', 'English', 'Chemistry', 'Biology', 'Physics', 
        'Commerce', 'Economics', 'Computer Science'
    ]

    # Grades
    grades = ['A', 'B', 'C', 'D', 'E', 'F', 'U']

    # O-Level grades input form
    st.subheader("O Level Grades")
    selected_o_level_subjects = st.multiselect("Select O Level Subjects:", o_level_subjects)
    o_level_grades = {}
    for subject in selected_o_level_subjects:
        o_level_grades[subject] = st.selectbox(f'Select grade for {subject}:', grades, key=f'o_level_{subject}')

    # A-Level grades input form (optional)
    st.subheader("A Level Grades (if applicable)")
    selected_a_level_subjects = st.multiselect("Select A Level Subjects:", a_level_subjects)
    a_level_grades = {}
    for subject in selected_a_level_subjects:
        a_level_grades[subject] = st.selectbox(f'Select grade for {subject}:', grades, key=f'a_level_{subject}')

    # Example data
    data = {
        "Institution": [
            "Laksamana College of Business", 
            "Cosmopolitan College of Commerce and Technology", 
            "Kemuda Institute", 
            "IBTE", 
            "Universiti Brunei Darussalam (UBD)",
            "Universiti Teknologi Brunei (UTB)",
            "Universiti Islam Sultan Sharif Ali (UNISSA)",
            "Politeknik Brunei",
            "Micronet International College",
            "International Graduate Studies College"
        ],
        "Programs": [
            ["BTEC International Level 2 Certificate in Business", "BTEC International Level 3 Diploma in Business", "BTEC Higher National Diploma in Business (Accounting)", "BTEC Higher National Diploma in Business (Marketing)", "University Foundation Course", "BA Common Year One", "BA (Hons) Accounting & Finance", "BA (Hons) Business Management", "BA (Hons) Marketing", "KCB Professional Pathway Certificate in Business Management", "KCB Professional Pathway Diploma in Business Management", "KCB Professional Pathway Advanced Diploma in Business Management", "KCB Professional Pathway Higher Diploma in Business Management"],
            ["Level-1 Introductory Diploma in Business", "Level-2 International Certificate in Business", "Level-3 Diploma in Business", "Level-5 HND in Business", "Level-1 Introductory Diploma in Information Technology", "Level-2 International Certificate in Information Technology", "Level-3 Diploma in Information Technology", "Level-5 HND in Computing"],
            ["BTEC Level 5 Higher National Diploma in Computing", "BTEC Level 3 Diploma in Information Technology", "BTEC Level 2 Certificate in Information Technology", "Level 1 Introductory Diploma in Information Technology"],
            ["HNTec in Aircraft Engineering", "HNTec in Electronic Engineering", "HNTec in Electronic and Communication Engineering", "HNTec in Electronic and Media Technology", "HNTec Apprenticeship in Telecommunication Network Engineering", "HNTec in Hospitality Operations", "HNTec in Tourism Operations"],
            ["Bachelor Programs in Arts, Science, and Technology"],
            ["Bachelor Programs in Engineering and Technology"],
            ["Bachelor Programs in Islamic Studies"],
            [
                "School of Business: Human Capital Management", "School of Business: Entrepreneurship & Marketing Strategies", 
                "School of Business: Apprenticeship Hospitality Management & Operations", "School of Business: Business Accounting & Finance",
                "School of Health Sciences: Public Health", "School of Health Sciences: Cardiovascular Technology", 
                "School of Health Sciences: Paramedic", "School of Health Sciences: Nursing", "School of Health Sciences: Midwifery",
                "School of Information and Communication Technology: Digital Arts & Media", "School of Information and Communication Technology: Data Analytics", 
                "School of Information and Communication Technology: Web Technology", "School of Information and Communication Technology: Cloud and Networking", 
                "School of Information and Communication Technology: Application Development",
                "School of Science and Engineering: Electronic and Communication Engineering", "School of Science and Engineering: Electrical Engineering", 
                "School of Science and Engineering: Civil Engineering", "School of Science and Engineering: Petroleum Engineering", 
                "School of Science and Engineering: Mechanical Engineering", "School of Science and Engineering: Interior Design", 
                "School of Science and Engineering: Architecture",
                "School of Petrochemical: Storage and Transportation Technology", "School of Petrochemical: Chemical Equipment Technology", 
                "School of Petrochemical: Laboratory Technology", "School of Petrochemical: Water Treatment Technology", 
                "School of Petrochemical: Chemical Engineering", "School of Petrochemical: Power Plant and Power System", 
                "School of Petrochemical: Thermal Power Plant Technology"
            ],
            ["Diploma in Information Technology", "Diploma in Computing", "Higher National Diploma in Computing"],
            ["Diploma in Computer Studies", "Diploma in Business and Finance", "Diploma in Multimedia and Broadcasting", "Diploma in Art & Humanities", "Higher National Diploma in Computing", "Higher National Diploma in Business Management", "Part time course in LCCI Diploma Accounting", "Part time course in Diploma in Marketing", "Part time course in Private Secretary's Diploma"]
        ],
        "Entry Requirements": [
            {"O_level_credits": 4},
            {"O_level_credits": 1},
            {"O_level_credits": 4},
            {"O_level_credits": 4},
            {"O_level_credits": 5, "A_level_passes": 2},
            {"O_level_credits": 5, "A_level_passes": 2},
            {"O_level_credits": 5, "A_level_passes": 2},
            {"O_level_credits": 5},
            {"O_level_credits": 4},
            {"O_level_credits": 4}
        ]
    }

    # Convert the data to a DataFrame
    df = pd.DataFrame(data)

    # Grading criteria function
    def calculate_credits(grades):
        return sum(1 for g in grades.values() if g in ['A', 'B', 'C'])

    def is_eligible(o_level_grades, a_level_grades, requirements):
        actual_o_level_credits = calculate_credits(o_level_grades)
        actual_a_level_passes = calculate_credits(a_level_grades)
        
        required_o_level_credits = requirements.get("O_level_credits", 0)
        required_a_level_passes = requirements.get("A_level_passes", 0)
        
        if actual_o_level_credits < required_o_level_credits:
            return False
        if required_a_level_passes > 0 and actual_a_level_passes < required_a_level_passes:
            return False
        
        return True

    # Combine all grades
    all_grades = {**o_level_grades, **a_level_grades}

    # Submit button
    if st.button('Submit'):
        eligible_institutions = []
        ineligible_institutions = []
        for i, institution in enumerate(data['Institution']):
            if is_eligible(o_level_grades, a_level_grades, data['Entry Requirements'][i]):
                eligible_institutions.append(institution)
            else:
                ineligible_institutions.append(institution)
        
        st.write(f'You entered O Level Grades: {o_level_grades}')
        st.write(f'You entered A Level Grades: {a_level_grades}')
        
        st.subheader("Eligible Institutions")
        if eligible_institutions:
            for institution in eligible_institutions:
                st.write(f"- {institution}")
        else:
            st.write("- none")
        
        st.subheader("Ineligible Institutions")
        with st.expander("Click to view ineligible institutions"):
            if not ineligible_institutions:
                st.write("- none")
            else:
                for institution in ineligible_institutions:
                    st.write(f"- {institution}")

    # Tabs for each institution
    tabs = st.tabs(data['Institution'])

    for i, tab in enumerate(tabs):
        with tab:
            st.subheader(f"{data['Institution'][i]}")
            st.write("### Programs Offered:")
            for program in data['Programs'][i]:
                st.write(f"- {program}")
            st.write("### Entry Requirements:")
            st.write(f"- Requires at least {data['Entry Requirements'][i]['O_level_credits']} O Level credits (grades A, B, or C)")
            if "A_level_passes" in data['Entry Requirements'][i]:
                st.write(f"- Requires at least {data['Entry Requirements'][i]['A_level_passes']} A Level passes (grades A, B, C, D, or E)")

    # Additional sections
    with st.expander("More Information"):
        st.write("Here is more detailed information about the eligibility criteria and application process.")
        