import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Set page title
st.set_page_config(page_title="Parts Analysis", layout="wide")

# Function to load data
@st.cache_data
def load_data(file):
    return pd.read_excel(file)

# Function to create and display the plot
def create_and_display_plot(df):
    # Calculate median values
    median_value = np.median(df['maintenance_value'])
    median_removals = np.median(df['n_removals_ltm'])

    # Create the scatter plot
    fig = px.scatter(
        df,
        x='n_removals_ltm',
        y='maintenance_value',
        hover_data=['part_desc'],
        title='Value vs Number of Removals (LTM)',
        labels={
            'n_removals_ltm': 'Number of Removals',
            'maintenance_value': 'Maintenance Value'
        }
    )

    # Add vertical line for median x value
    fig.add_vline(x=median_removals, line_dash="dash", line_color="red", 
                  annotation_text=f"Median Removals: {median_removals:.2f}", 
                  annotation_position="top right")

    # Add horizontal line for median y value
    fig.add_hline(y=median_value, line_dash="dash", line_color="green", 
                  annotation_text=f"Median Value: {median_value:.2f}", 
                  annotation_position="top right")

    # Update layout for better readability
    fig.update_layout(
        annotations=[
            dict(x=1, y=1.05, xref="paper", yref="paper", text="Median Lines:", showarrow=False),
            dict(x=1, y=1.02, xref="paper", yref="paper", text="Removals (Red) | Value (Green)", showarrow=False)
        ]
    )

    # Display the scatter plot
    st.plotly_chart(fig, use_container_width=True)

    # Display median values in sidebar
    st.sidebar.header("Median Values")
    st.sidebar.write(f"Median Maintenance Value: {median_value:.2f}")
    st.sidebar.write(f"Median Removals (LTM): {median_removals:.2f}")

# Add page title
st.title("Parts Analysis")

# Initialize session state
if 'current_file' not in st.session_state:
    st.session_state.current_file = None
if 'plot_key' not in st.session_state:
    st.session_state.plot_key = 0

# File uploader
uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx", key=f"uploader_{st.session_state.plot_key}")

# Clear plot button
if st.button("Clear Plot"):
    st.session_state.current_file = None
    st.session_state.plot_key += 1
    st.experimental_rerun()

# Check if a new file has been uploaded
if uploaded_file is not None and uploaded_file != st.session_state.current_file:
    # Update the current file in session state
    st.session_state.current_file = uploaded_file
    
    # Load the new file
    df = load_data(uploaded_file)
    
    # Create and display the new plot
    create_and_display_plot(df)
    
    # Optional: Display dataframe
    if st.checkbox("Show raw data"):
        st.dataframe(df)
elif st.session_state.current_file is None:
    # If no file has been uploaded yet, try to load the default file
    try:
        df = load_data('parts.xlsx')
        create_and_display_plot(df)
        
        # Optional: Display dataframe
        if st.checkbox("Show raw data"):
            st.dataframe(df)
    except FileNotFoundError:
        st.error("Default 'parts.xlsx' file not found. Please upload a file.")

# If a file has been previously loaded but not changed, maintain the current view
elif st.session_state.current_file is not None:
    df = load_data(st.session_state.current_file)
    create_and_display_plot(df)
    
    # Optional: Display dataframe
    if st.checkbox("Show raw data"):
        st.dataframe(df)