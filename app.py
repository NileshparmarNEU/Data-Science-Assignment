import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

@st.cache_resource
def load_data():
    # Load the dataset (make sure to use the correct path to your CSV)
    data = pd.read_csv('NewPeanut.csv')
    return data

# Function to filter recipes based on user input
def filter_recipes(df, dietary_restrictions, meal_type):
    # Filter by dietary restrictions
    for restriction in dietary_restrictions:
        if restriction not in df.columns:
            st.error(f"We don't have data for {restriction} recipes yet.")
            return pd.DataFrame()
    df = df[np.all([df[restriction] for restriction in dietary_restrictions], axis=0)]

    # Filter by meal type
    if meal_type and meal_type != 'Any':
        df = df[df['meal_type'].str.contains(meal_type, case=False, na=False)]

    return df

# Function to style pandas DataFrame
def style_dataframe(df):
    return df.style.set_table_styles(
        [{'selector': 'th', 'props': [('font-size', '18px')]}]
    ).set_properties(**{
        'background-color': '#f4f4f2',
        'color': 'black',
        'border-color': 'white'
    })

def main():
    st.set_page_config(layout="wide", page_title="🍲 NutriMeal Navigator")

    # Custom CSS to inject into the Streamlit app for a larger font title and styled button
    st.markdown(
        """
        <style>
        .big-font {
            font-size:400% !important;
            font-weight:bold;
            color: #FF4B4B;
        }
        .stButton>button {
            width: 100%;
            border-radius: 10px;
            border: none;
            background-color: #FF4B4B;
            color: white;
            font-size: 20px;
            padding: 15px 0;
            margin-top: 20px;
            transition: background-color 0.3s, color 0.3s;
        }
        .stButton>button:hover {
            background-color: white;
            color: #FF4B4B;
        }
        .stDataFrame {
            font-size: 16px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Display the app title in the main page body
    st.markdown('<div class="big-font">🍲 NutriMeal Navigator</div>', unsafe_allow_html=True)

    # Load the data
    df = load_data()

    # Sidebar for user inputs
    with st.sidebar:
        st.header('Select dietary restrictions and meal type')
        dietary_restrictions = st.multiselect(
            'Select dietary restrictions',
            ['Vegetarian', 'Vegan', 'Gluten-Free', 'Peanut-Free'],
            help="Choose one or more dietary restrictions to filter recipes."
        )
        meal_type = st.radio(
            'What type of meal are you looking for?',
            ('Any', 'Breakfast', 'Lunch', 'Dinner', 'Dessert'),
            help="Select the type of meal you are interested in."
        )
        submit_button = st.button('Find Recipes')

    # Main body for displaying recipes
    if submit_button:
        filtered_df = filter_recipes(df, dietary_restrictions, meal_type)
        if not filtered_df.empty:
            st.write(f"Found {len(filtered_df)} recipes:")
            st.dataframe(style_dataframe(filtered_df[['title', 'rating', 'meal_type']]))
        else:
            st.error("No recipes found with the selected criteria.")

if __name__ == '__main__':
    main()