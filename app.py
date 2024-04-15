import streamlit as st
from streamlit.components.v1 import html
from streamlit_pandas_profiling import st_profile_report
from pathlib import Path
import pandas as pd
import base64
import ydata_profiling
from IPython.display import HTML
import uuid


st.markdown(
    """
    <style>
    a {
        text-decoration: none;
        color: inherit;
    };

    /* Set the background of the profiling report to transparent */
    .stProfileReport body {
        background-color: transparent !important;
    };

    /* Set the background of the profiling report iframe to transparent */
    .stProfileReport iframe {
        background-color: transparent !important;
    };

    const iframe = document.querySelector('.stProfileReport iframe');
    iframe.onload = function() {
        const doc = iframe.contentDocument || iframe.contentWindow.document;
        doc.body.style.backgroundColor = 'transparent';
    };

    /* Set the background of the profiling report to transparent */
    .profile_report {
        background-color: transparent !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar menu options
menu_options = {
    'About': 'About',
    'Upload': 'Upload Your Data for Modelling:',
    'Profiling': 'Automated Exploratory Data Analysis'
}

# Load dataset into session state
def load_data(file):
    try:
        file_extension = Path(file.name).suffix.lower()
        if file_extension == ".csv":
            return pd.read_csv(file, index_col=None)
        elif file_extension in [".xls", ".xlsx"]:
            return pd.read_excel(file, engine='openpyxl', dtype=str)
        else:
            st.warning("Unsupported File Format! Only csv, xlsx, and xls files are allowed.")
            return pd.DataFrame()
    except Exception as e:
        st.warning('Error reading the file: {}'.format(e))
        st.warning("Please try uploading again a valid .csv, .xlsx, or .xls file.")
        return pd.DataFrame()

# Main function
def main():
    # Set up the sidebar menu
    st.sidebar.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS7dMeD4Xyh5GrERbuXdCv-dx1-MmOVLVd14Q&usqp=CAU")
    st.sidebar.title("EDA - Exploratory Data Analysis")
    choice = st.sidebar.radio("Navigation", list(menu_options.keys()))
    st.sidebar.info("Made by Ciprian Maru")

    if 'df' not in st.session_state:
        st.session_state.df = pd.DataFrame()

    # Page contents based on user choice
    

    

    if choice == 'About':
        
        description = '''
        This application leverages the principles of Exploratory Data Analysis (EDA) to automatically analyze any given dataset. The application provides a comprehensive set of standard key performance indicators (KPIs) and analysis, which can be presented in various formats, including informative text, charts, and other visualizations. With the integration of these technologies, users can gain valuable insights into their data effortlessly.

         Was created using:
        - Python: The programming language used as the core of the application.
        - Streamlit: A Python library used for building interactive web applications.
        - Pandas Profiling: A library for generating detailed exploratory data analysis reports.
        - JavaScript: A programming language used for adding interactivity and dynamic features to the app.
        - CSS: Cascading Style Sheets used for styling and formatting the visual elements of the app.

        '''

        st.info(description)
        st.subheader("What is EDA")
          # Add the image as the banner
        
        # Embed local video file using Streamlit's video method
        video_path = "eda_video.mp4"
        video_file = open(video_path, "rb")
        video_bytes = video_file.read()

        # Generate a unique ID for the video element
        video_id = str(uuid.uuid4())

        # Generate JavaScript code to autoplay the video
        js_code = f"""
        <script>
            var video = document.getElementById("{video_id}");
            video.currentTime = 3;
            video.volume = 0.25;
            video.play();
        </script>
        """

        # Embed the video with the generated ID and JavaScript code
        st.video(video_bytes, format="video/mp4", start_time=0)

        # Inject the JavaScript code into the Streamlit app
        st.write(js_code, unsafe_allow_html=True)
        image_url = "https://datos.gob.es/sites/default/files/u322/grafico.jpg"
        st.image(image_url, width=700)


        st.warning("To start go to 'Upload' tab and upload your dataset")



    elif choice == "Upload":
        st.title(menu_options[choice])
        file = st.file_uploader("Upload your Dataset Here")
        if file is not None:
            try:
                st.session_state.df = load_data(file)
                # Check if dataframe is not empty or null
                if st.session_state.df.empty:
                    st.warning('Selected File has no Data, or File Format is not Allowed.')
                else:
                    st.success('File Uploaded Successfully!')
                    st.dataframe(st.session_state.df)
                    # Add "GO TO PROFILING" button
                    st.info("Click the 'Profiling' button on the sidebar to move to the next")

            except Exception as e:
                st.warning('Error reading the file: {}'.format(e))
                st.warning("Please try uploading a valid .csv file.")

    elif choice == 'Profiling':
        st.title(menu_options[choice])
        if st.session_state.df.empty:
            st.warning("No data was uploaded in order to execute profiling.")
            st.warning("Go to Navigation Bar and Upload your dataset first.")
        else:
            with st.spinner('Profiling in progress...'):
                profile_report = st.session_state.df.profile_report()
                # Add download button
                download_button = st.download_button(label="Download Report",
                                                     data=profile_report.to_html(),
                                                     file_name='profile_report.html',
                                                     mime='text/html')
                st_profile_report(profile_report)
                st.success("Profiling completed!")

    st.sidebar.markdown(
        """
        Find me on email: <br>maruciprian99@gmail.com
        <br>Or on socials:
        <br>
        <a href="https://www.linkedin.com/in/ionut-ciprian-maru-bb55951b9/" target="_blank">
            <img src="https://cdn1.iconfinder.com/data/icons/logotypes/32/circle-linkedin-256.png" alt="LinkedIn" width="24" height="24">
        </a>
        &nbsp;&nbsp;&nbsp;
        <a href="https://github.com/maruciprian99" target="_blank">
            <img src="https://cdn1.iconfinder.com/data/icons/logotypes/32/github-256.png" alt="GitHub" width="24" height="24">
        </a>
        &nbsp;&nbsp;&nbsp;
        <a href="https://www.instagram.com/maruciprian/" target="_blank">
            <img src="https://cdn3.iconfinder.com/data/icons/2018-social-media-logotypes/1000/2018_social_media_popular_app_logo_instagram-512.png" alt="Instagram" width="24" height="24">
        </a>
        """,
        unsafe_allow_html=True
    )


if __name__ == '__main__':
    main()
