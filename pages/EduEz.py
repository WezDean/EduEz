def EduEz():
    import streamlit as st
    import pandas as pd
    # Creating the cover header layout
    header_col1, header_col2 = st.columns([1, 2])
    with header_col1:
        st.title("EduEZ: Educational Pathways Recommendation System")
        st.write("""
            EduEZ is designed to help students explore potential educational pathways based on their O Level and A Level results. 
            Simply input your grades, and we'll recommend institutions and programs that match your qualifications.
        """)

    # Adding the image on the left
    with header_col2:
        st.image("SDG4.jpg", use_column_width=True)  # Replace with your image path or URL

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
    "Description": [
        "Laksamana College of Business is a leading educational institution offering business-related programs.",
        "Cosmopolitan College of Commerce and Technology focuses on commerce and technology courses.",
        "Kemuda Institute specializes in computing and IT programs.",
        "IBTE provides technical education and vocational training.",
        "Universiti Brunei Darussalam (UBD) is Brunei's premier university.",
        "Universiti Teknologi Brunei (UTB) offers engineering and technology programs.",
        "Universiti Islam Sultan Sharif Ali (UNISSA) focuses on Islamic studies.",
        "Politeknik Brunei provides a range of diploma programs across various fields.",
        "Micronet International College specializes in IT and business programs.",
        "International Graduate Studies College offers various diploma programs in business, computing, and multimedia."
    ],
    "Programs": [
        ["BTEC International Level 2 Certificate in Business", "BTEC International Level 3 Diploma in Business", "BTEC Higher National Diploma in Business (Accounting)", "BTEC Higher National Diploma in Business (Marketing)"],
        ["Level-1 Introductory Diploma in Business", "Level-2 International Certificate in Business", "Level-3 Diploma in Business", "Level-5 HND in Business"],
        ["BTEC Level 5 Higher National Diploma in Computing", "BTEC Level 3 Diploma in Information Technology", "BTEC Level 2 Certificate in Information Technology", "Level 1 Introductory Diploma in Information Technology"],
        ["HNTec in Aircraft Engineering", "HNTec in Electronic Engineering", "HNTec in Electronic and Communication Engineering", "HNTec in Electronic and Media Technology"],
        ["Bachelor Programs in Arts, Science, and Technology"],
        ["Bachelor Programs in Engineering and Technology"],
        ["Bachelor Programs in Islamic Studies"],
        ["Diploma in Business", "Diploma in Hospitality Management", "Diploma in IT"],
        ["Diploma in Computing", "Diploma in Business and Finance"],
        ["Diploma in Computer Studies", "Diploma in Business and Finance"]
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
    ],
    "Contact": [
        {"Website": "https://www.lcb.edu.bn", "Phone": "+673 2232451", "Address": "Jalan Ong Sum Ping, Bandar Seri Begawan, Brunei"},
        {"Website": "https://www.ccct.edu.bn", "Phone": "+673 2232452", "Address": "Simpang 47-15, Kg Kiulap, Bandar Seri Begawan, Brunei"},
        {"Website": "https://www.kemuda.edu.bn", "Phone": "+673 2232453", "Address": "Simpang 47-16, Kg Kiulap, Bandar Seri Begawan, Brunei"},
        {"Website": "https://www.ibte.edu.bn", "Phone": "+673 2232454", "Address": "Simpang 47-17, Kg Kiulap, Bandar Seri Begawan, Brunei"},
        {"Website": "https://www.ubd.edu.bn", "Phone": "+673 2232455", "Address": "Simpang 47-18, Kg Kiulap, Bandar Seri Begawan, Brunei"},
        {"Website": "https://www.utb.edu.bn", "Phone": "+673 2232456", "Address": "Simpang 47-19, Kg Kiulap, Bandar Seri Begawan, Brunei"},
        {"Website": "https://www.unissa.edu.bn", "Phone": "+673 2232457", "Address": "Simpang 47-20, Kg Kiulap, Bandar Seri Begawan, Brunei"},
        {"Website": "https://www.pb.edu.bn", "Phone": "+673 2232458", "Address": "Simpang 47-21, Kg Kiulap, Bandar Seri Begawan, Brunei"},
        {"Website": "https://www.micronet.edu.bn", "Phone": "+673 2232459", "Address": "Simpang 47-22, Kg Kiulap, Bandar Seri Begawan, Brunei"},
        {"Website": "https://www.igs.edu.bn", "Phone": "+673 2232460", "Address": "Simpang 47-23, Kg Kiulap, Bandar Seri Begawan, Brunei"}
    ]}

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
            st.markdown(f"{data['Description'][i]}")
            
            st.write("### Programs Offered:")
            for program in data['Programs'][i]:
                st.write(f"- {program}")
            
            st.write("### Entry Requirements:")
            st.write(f"- Requires at least {data['Entry Requirements'][i]['O_level_credits']} O Level credits (grades A, B, or C)")
            if "A_level_passes" in data['Entry Requirements'][i]:
                st.write(f"- Requires at least {data['Entry Requirements'][i]['A_level_passes']} A Level passes (grades A, B, C, D, or E)")

            # Additional sections for each institution
            with st.expander("More Information"):
                contact = data['Contact'][i]
                st.write(f"**Website**: [Visit Website]({contact['Website']})")
                st.write(f"**Phone**: {contact['Phone']}")
                st.write(f"**Address**: {contact['Address']}")