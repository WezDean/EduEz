import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
file_path = 'Bruneian_Students_Simulated_Dataset.csv'
df = pd.read_csv(file_path)

st.title('Bruneian Students Data Analysis')

# 1. Gender Distribution Across Different School Types
st.subheader('Gender Distribution Across Different School Types')
selected_school_type = st.selectbox("Select School Type", df['School_Type'].unique())
gender_school_type = df[df['School_Type'] == selected_school_type].groupby(['Gender']).size()
st.bar_chart(gender_school_type)

# 2. Family Income Distribution by District
st.subheader('Family Income Distribution by District')
selected_district = st.multiselect("Select District(s)", df['District'].unique(), df['District'].unique())
filtered_df = df[df['District'].isin(selected_district)]
fig, ax = plt.subplots()
sns.boxplot(x='District', y='Family_Income', data=filtered_df, ax=ax)
ax.set_title('Family Income Distribution by District')
st.pyplot(fig)

# 3. Preferred Programs vs. Recommended Programs
st.subheader('Preferred Programs vs. Recommended Programs')
selected_program = st.selectbox("Select Preferred Program", df['Preferred_Program'].unique())
program_df = df[df['Preferred_Program'] == selected_program].groupby(['Preferred_Program', 'Recommended_Program']).size().unstack().fillna(0)
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(program_df, annot=True, cmap="YlGnBu", ax=ax)
ax.set_title('Preferred vs. Recommended Programs for ' + selected_program)
st.pyplot(fig)

# 4. Family Income vs. A-Level Credits by Gender and Parent Education Level
st.subheader('Family Income vs. A-Level Credits')
selected_gender = st.selectbox("Select Gender", df['Gender'].unique())
selected_parent_education = st.multiselect("Select Parent Education Level", df['Parent_Education_Level'].unique(), df['Parent_Education_Level'].unique())
filtered_income_df = df[(df['Gender'] == selected_gender) & (df['Parent_Education_Level'].isin(selected_parent_education))]
fig, ax = plt.subplots()
sns.scatterplot(x='Family_Income', y='A_Level_Credits', hue='Parent_Education_Level', data=filtered_income_df, ax=ax)
ax.set_title('Family Income vs. A-Level Credits (' + selected_gender + ')')
st.pyplot(fig)
