import streamlit as st

def homepage():
    # Define the layout with columns
    col1, col2, col3, col4 = st.columns([1, 14, 11, 1], gap='medium')
    
    # Top section: Data Analysis, What's Next?, Predictive Models
    st.markdown(
    """
    <div style="display: flex; gap: 20px; margin-top: 20px;">
        <div style="flex: 1; padding: 10px; background-color: #f4faff; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">
            <h4 style="text-align: center;">📊 Data Analysis</h4>
            <p>In-depth analysis of the students in Brunei Darussalam.</p>
        </div>
        <div style="flex: 1; padding: 10px; background-color: #f4faff; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">
            <h4 style="text-align: center;">🔍 What's Next?</h4>
            <p>EduEz - Simple feature for students to know their eligible institutions.</p>
        </div>
        <div style="flex: 1; padding: 10px; background-color: #f4faff; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">
            <h4 style="text-align: center;">🤖 Predictive Models</h4>
            <p>Machine learning models to forecast several factors on quality education of students.</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True
    )

    # Middle section: Title, Header, and Image
    with col2:
        st.markdown(
            """
            <style>
            body {
                font-family: 'Playwrite MX', sans-serif;
                background-color: #D4D4CE; 
            }

            .title {
                font-family: 'Playwrite MX', sans-serif;
                font-size: 2.5em;
                font-weight: bold;
                text-align: center;
                margin-top: 40px;
                margin-bottom: 20px;
            }

            .header {
                font-family: 'Playwrite MX', sans-serif;
                font-size: 2em;
                text-align: center;
                margin-bottom: 40px;
            }

            .quote {
                font-family: 'Georgia', serif;
                font-style: italic;
                color: #95A5A6;
                font-size: 1.5em;
                text-align: center;
                margin-top: 30px;
                margin-bottom: 30px;
            }

            hr {
                border: none;
                height: 1px;
                background-color: #bdc3c7;
                margin: 20px 0;
            }

            .quote-box {
                background-color: #f8f9fa;
                border-left: 6px solid #3498db;
                padding: 20px;
                margin: 20px 0;
                font-family: 'Georgia', serif;
                color: #2C3E50;
                font-size: 1.2em;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }

            .quote-box p {
                margin: 0;
                font-style: italic;
            }

            .quote-box .author {
                text-align: right;
                font-weight: bold;
                margin-top: 15px;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        # Title and header
        st.markdown('<div class="title">Quality Education in Brunei Darussalam</div>', unsafe_allow_html=True)
        st.markdown('<div class="header">Analysis on Students of Brunei Darussalam</div>', unsafe_allow_html=True)

    # Image in the third column
    with col3:
        st.image("books.png", use_column_width=False, width= 350)

    # Bottom section: Motivational Quote
    st.markdown(
        """
        <hr>
        <div class="quote">
        "Quality education is the key to success for the future generation."
        </div>
        <hr>
        """, 
        unsafe_allow_html=True
    )

# Call the homepage function to render the content
if __name__ == "__main__":
    homepage()
