from dotenv import load_dotenv
import streamlit as st
import os
# Load environment variables from .env file
load_dotenv()
# Now you can access your API keys (and other environment variables)
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

import openai
import pandas as pd

# Set your OpenAI API key here
#openai.api_key = 'your-api-key'

def ask_question(prompt):
    completion = openai.chat.completions.create(
        model="gpt-3.5-turbo-16k",  # you can replace this with your preferred model
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500
    )
    return completion.choices[0].message.content

def interact_with_ai(message, model="gpt-3.5-turbo-16k"):
    prompt = f"Please provide a brief response to the following question to maintain the conversation flow. Do not give any advice at this stage.\nQuestion: {message}"
    completion = openai.chat.completions.create(
        model="gpt-3.5-turbo-16k",  # you can replace this with your preferred model
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150
    )
    return completion.choices[0].message.content


def recommend_hosting_with_ai(dialog, ai_tooolss_csv):
    # Read the CSV data into a string format suitable for the prompt
    hosting_data = pd.read_csv(ai_tooolss_csv)
    hosting_data_string = hosting_data.to_string(index=False)

    # Construct the prompt
    prompt = (f"Based on the following user answers:\n{dialog}\n\n"
              f"And using ONLY the following AI tools data:\n{hosting_data_string}\n\n"
              "Recommend which AI tools to use. Your recommendations should be based solely on the provided data and not on external knowledge. Please return their names, links, and a brief explanation for each recommendation.")

    # Call the OpenAI API
    completion = openai.chat.completions.create(
        model="gpt-3.5-turbo-16k",  
        messages=[{"role": "user", "content": prompt}]
    )

    return completion.choices[0].message.content



def main():
    st.title("AI tool advisor for students")  # Set a title for your app

    # Load hosting data from CSV
    file_path = 'ai_tooolss.csv'  # Update this with the path to your CSV file

    # Define the questions you're going to ask the user
    # Questions to ask the user
    questions = [
        "What is your budget for using AI tools? (e.g., free, premium with specific monthly/annual budget)",
        "What specific tasks or needs do you have for an AI tool? (e.g., writing assistance, finding papers, data analysis, presentation creation)",
        "What is your level of expertise with AI tools? (e.g., beginner, intermediate, advanced)",
        "How often do you anticipate using AI tools? (e.g., daily, weekly, occasionally)",
        "Are there specific features you are looking for in an AI tool? (e.g. plagiarism checking, quick web research, text summarization, voice transcripts, mind-maps, word clouds)"
    ]
    dialog = ""  # Initialize an empty string to hold the dialog

    st.write("Welcome to the AI tool advisor for Tilburg University students!")  # Display a welcome message

    # Create input boxes for each question
    for question in questions:
        # Streamlit provides various input methods; text_input is used here for simplicity
        user_answer = st.text_input(question, key=question)
        if user_answer:  # Check if the user has provided an answer
            dialog += f"Q: {question}\nA: {user_answer}\n"

            # Get a brief reply from the AI regarding the user's answer
            # Note: for actual deployment, consider adding conditions to prevent excessive API calls
            brief_reply = interact_with_ai(dialog)
            st.text_area("Advisor:", value=f"{brief_reply}", key=f"reply_{question}")

    if st.button('Get AI tool Recommendation'):  # Add a button to trigger recommendation
        if dialog:  # Ensure there's a dialog to process
            recommended_hosting = recommend_hosting_with_ai(dialog, file_path)
            st.text_area("Recommended AI tool(s)", value=recommended_hosting, height=300)

# The below line ensures that when you run the script, it calls the main() function
if __name__ == "__main__":
    main()
