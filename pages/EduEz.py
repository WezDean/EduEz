import streamlit as st
import pandas as pd

def EduEz():

      # Custom CSS to change the background color to light green
    st.markdown(
        """
        <style>
        /* Change the background color */
        .stApp {
            background-color: #e6ffe6; /* Slightly light green */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Define the file paths for each institution, including the new ones
    institution_csv_mapping = {
        "Laksamana College of Business": r"C:/Users/waizz/OneDrive/Documents/GitHub/EduEz/pages/Laksamana_College.csv",
        "Cosmopolitan College of Commerce and Technology": r"C:/Users/waizz/OneDrive/Documents/GitHub/EduEz/pages/Cosmopolitan_College_of_Commerce_and_Technology_courses.csv",
        "Kemuda Institute": r"C:/Users/waizz/OneDrive/Documents/GitHub/EduEz/pages/Kemuda_Institute_courses.csv",
        "IBTE": r"C:/Users/waizz/OneDrive/Documents/GitHub/EduEz/pages/IBTE.csv",
        "Universiti Brunei Darussalam (UBD)": r"C:/Users/waizz/OneDrive/Documents/GitHub/EduEz/pages/Universiti_Brunei_Darussalam.csv",
        "Universiti Teknologi Brunei (UTB)": r"C:/Users/waizz/OneDrive/Documents/GitHub/EduEz/pages/Universiti_Teknologi_Brunei.csv",
        "International Graduate Studies College": r"C:/Users/waizz/OneDrive/Documents/GitHub/EduEz/pages/International_Graduate_Studies_College_courses.csv",
        "KUPUSB": r"C:/Users/waizz/OneDrive/Documents/GitHub/EduEz/pages/KUPUSB_courses.csv",
        "Micronet International College": r"C:/Users/waizz/OneDrive/Documents/GitHub/EduEz/pages/Micronet_International_College_courses.csv",
        "Politeknik Brunei": r"C:/Users/waizz/OneDrive/Documents/GitHub/EduEz/pages/Politeknik_Brunei_courses.csv",
        "Universiti Sultan Sharif Ali": r"C:/Users/waizz/OneDrive/Documents/GitHub/EduEz/pages/Universiti_Sultan_Sharif_Ali.csv"
    }

    # Define the O Level and A Level requirements for each institution
    institution_requirements = {
        "Laksamana College of Business": {"O_Level_Credits": 4, "A_Level_Passes": 0},
        "Cosmopolitan College of Commerce and Technology": {"O_Level_Credits": 1, "A_Level_Passes": 0},
        "Kemuda Institute": {"O_Level_Credits": 4, "A_Level_Passes": 0},
        "IBTE": {"O_Level_Credits": 4, "A_Level_Passes": 0},
        "Universiti Brunei Darussalam (UBD)": {"O_Level_Credits": 0, "A_Level_Passes": 2},
        "Universiti Teknologi Brunei (UTB)": {"O_Level_Credits": 0, "A_Level_Passes": 2},
        "International Graduate Studies College": {"O_Level_Credits": 4, "A_Level_Passes": 0},
        "Kolej Universiti Perguruan Ugama Seri Begawan (KUPUSB)": {"O_Level_Credits": 4, "A_Level_Passes": 0},
        "Micronet International College": {"O_Level_Credits": 1, "A_Level_Passes": 0},
        "Politeknik Brunei": {"O_Level_Credits": 5, "A_Level_Passes": 0},
        "Universiti Sultan Sharif Ali": {"O_Level_Credits": 0, "A_Level_Passes": 2}
    }

    # Function to load and display courses from a CSV file
    def display_courses(institution_name, csv_file_path):
        try:
            df = pd.read_csv(csv_file_path)
            st.subheader(f"{institution_name} - Courses")
            
            # Aesthetic display of courses
            for index, row in df.iterrows():
                st.markdown(f"**Program**: {row['Programs']}")
                st.markdown(f"*Minimum Entry Requirements*: {row['Entry Requirements']}")
                st.markdown("---")  # Divider for readability
                
        except FileNotFoundError:
            st.error(f"{institution_name} courses data not found. Please check the file path.")

    # Function to check eligibility based on O Level and A Level grades
    def check_eligibility(o_level_grades, a_level_grades, requirements):
        o_level_credits = sum(1 for grade in o_level_grades.values() if grade in ['A1', 'A2', 'B3', 'B4', 'C5', 'C6'])
        a_level_credits = sum(1 for grade in a_level_grades.values() if grade in ['A', 'B', 'C', 'D', 'E'])

        return o_level_credits >= requirements['O_Level_Credits'] and a_level_credits >= requirements['A_Level_Passes']

    st.title("EduEZ: Educational Pathways Eligibility System")
    
    # Header layout
    st.write("""
        EduEZ is designed to help students explore potential educational pathways based on their O Level and A Level results. 
        Simply input your grades, and see which institutions and programs that match your qualifications.
    """)

    # User Input for O Level and A Level Grades
    st.subheader("Enter Your O Level and A Level Results")

    # O Level subjects
    o_level_subjects = {
        'Mathematics (4024)': '4024', 
        'English (1123)': '1123', 
        'Malay Language (3248)': '3248', 
        'Islamic Religious Knowledge (2069)': '2069', 
        'Chemistry (5070)': '5070', 
        'Biology (5090)': '5090', 
        'Physics (5054)': '5054', 
        'Combined Science (5129)': '5129', 
        'Commerce (7100)': '7100', 
        'Economics (2281)': '2281', 
        'Computer Science (2210)': '2210', 
        'Additional Maths (4037)': '4037'
    }

    # A Level subjects
    a_level_subjects = {
        'Mathematics (9709)': '9709', 
        'English (9093)': '9093', 
        'Chemistry (9701)': '9701', 
        'Biology (9700)': '9700', 
        'Physics (9702)': '9702', 
        'Commerce (9609)': '9609', 
        'Economics (9708)': '9708', 
        'Computer Science (9608)': '9608'
    }

    # Grading options
    o_level_grades_list = ['A1', 'A2', 'B3', 'B4', 'C5', 'C6', 'D7', 'E8', 'U']
    a_level_grades_list = ['A', 'B', 'C', 'D', 'E', 'F', 'U']

    # O Level input using checkboxes for subjects with globally unique keys
    with st.expander("Select your O Level subjects"):
        st.write("Select subjects and grades:")
        o_level_grades = {}
        for i, (subject, code) in enumerate(o_level_subjects.items()):
            # Adding "O_Level" to the key to make it globally unique
            if st.checkbox(subject, key=f"O_Level_subject_{i}"):  # Unique key per iteration
                o_level_grades[subject] = st.selectbox(f'Select grade for {subject}', o_level_grades_list, key=f'O_Level_grade_{subject}_{i}')

    # A Level input using checkboxes for subjects with globally unique keys
    with st.expander("Select your A Level subjects"):
        st.write("Select subjects and grades:")
        a_level_grades = {}
        for i, (subject, code) in enumerate(a_level_subjects.items()):
            # Adding "A_Level" to the key to make it globally unique
            if st.checkbox(subject, key=f"A_Level_subject_{i}"):  # Unique key per iteration
                a_level_grades[subject] = st.selectbox(f'Select grade for {subject}', a_level_grades_list, key=f'A_Level_grade_{subject}_{i}')

    # Determine eligibility across institutions
    eligible_institutions = []
    ineligible_institutions = []

    if st.button('Submit'):
        for institution, requirements in institution_requirements.items():
            if check_eligibility(o_level_grades, a_level_grades, requirements):
                eligible_institutions.append(institution)
            else:
                ineligible_institutions.append(institution)

        # Display eligible institutions inside an expander
        with st.expander("Eligible Institutions", expanded=False):
            if eligible_institutions:
                for institution in eligible_institutions:
                    st.write(f"- {institution}")
            else:
                st.write("- None")

        # Display ineligible institutions inside an expander
        with st.expander("Ineligible Institutions", expanded=False):
            if ineligible_institutions:
                for institution in ineligible_institutions:
                    st.write(f"- {institution}")
            else:
                st.write("- None")

    # Load the contact data from the uploaded CSV file
    contact_data = pd.read_csv(r"C:/Users/waizz/OneDrive/Documents/GitHub/EduEz/pages/EduEZ_institutions_updated_data.csv")

    # Function to display contact and website information for an institution
    def display_institution_info(institution_name, contact_data):
        try:
            # Filter the contact data for the selected institution
            info = contact_data[contact_data['Institution'] == institution_name].iloc[0]

            # Display in an expander box
            with st.expander(f"{institution_name} - More Information"):
                st.write(f"**Description**: {info['Description']}") 
                st.write(f"**Contact**: {info['Contact']}")
                st.write(f"**Email**: {info['Email']}")
                st.write(f"**Website**: [Visit Website]({info['Website']})")
                st.write(f"**Location**: {info['Location']}")
        except IndexError:
            st.error(f"Contact information for {institution_name} is not available.")

    # Section where the user selects an institution to explore courses
    selected_tab = st.selectbox("Choose an Institution to Explore Courses", list(institution_csv_mapping.keys()))

    if selected_tab:
        # Display courses for the selected institution
        display_courses(selected_tab, institution_csv_mapping[selected_tab])

        # Display contact and website details for the selected institution
        display_institution_info(selected_tab, contact_data)



# Call the EduEz function to run the app
EduEz()