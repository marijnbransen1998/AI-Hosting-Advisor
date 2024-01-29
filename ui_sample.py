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
        model="gpt-3.5-turbo-1106",  # you can replace this with your preferred model
        messages=[{"role": "user", "content": prompt}],
        max_tokens=400
    )
    return completion.choices[0].message.content

#def interact_with_ai(message, model="gpt-3.5-turbo-16k"):
    #prompt = f"Please provide a brief response to the following question to maintain the conversation flow. Do not give any advice at this stage.\nQuestion: {message}"
    #completion = openai.chat.completions.create(
       # model="gpt-3.5-turbo-16k",  # you can replace this with your preferred model
        #messages=[{"role": "user", "content": prompt}],
        #max_tokens=150
    #)
   # return completion.choices[0].message.content


def recommend_hosting_with_ai(dialog, transposed_ai_tools2_csv):
    # Read the CSV data into a string format suitable for the prompt
    hosting_data = pd.read_csv(transposed_ai_tools2_csv)
    hosting_data_string = hosting_data.to_string(index=False)

# construct the prompt
    prompt = (f"Based on the following user answers:\n{dialog}\n\n"
          f"You are an AI tool advisor. Use the following AI tools data to find matches. Prioritize tools that have features closely matching the user's request:\n{hosting_data_string}\n\n"
          "Recommend AI tools that best fit the user's specified needs. List maximum 5 tools starting with the best recommendation to the least best recommendation. For each tool, provide the tool name in **bold**, followed by sections for **Pricing**, **Website**, and **Explanation**, each labeled in **bold**. Explain why each tool is a good match based on the features mentioned. Note: Recommendations should be based solely on the provided data and not on external knowledge.\n\n"
          "Inform the user that these recommendations are based on the article 'The 20 Best AI Tools' from tilburg.ai and for more options to find specific AI tools, they can visit: https://www.futuretools.io/")


    # Call the OpenAI API
    completion = openai.chat.completions.create(
        model="gpt-3.5-turbo-1106",  
        messages=[{"role": "user", "content": prompt}]
    )

    return completion.choices[0].message.content



def main():
    st.title("AI tool advisor for students")  # Set a title for your app

    # Load hosting data from CSV
    file_path = 'transposed_ai_tools2.csv'  # Update this with the path to your CSV file

    # Define the questions you're going to ask the user
    questions = [
        "What specific tasks or needs do you have for the AI tool? (e.g., writing assistance, finding papers, data analysis, presentation creation, meeting assistant)",
        "What is your budget for using AI tools? (e.g., free, free but with paid features, premium with specific monthly/annual budget)",
        "Are there specific features you are looking for in an AI tool? (e.g. plagiarism checking, guides and documentation, quick web research, text summarization, voice transcripts, mind-maps, word clouds)",
        "What is the primary motivation behind your search for an AI tool? (e.g., time saving, improved results, efficiency, research)"
    ]

    # Initialize an empty dictionary to hold the user responses
    user_responses = {}

    st.write("Welcome to the AI tool advisor for University students!")  # Display a welcome message

    # Create input boxes for each question
    for question in questions:
        response = st.text_input(question, key=question)
        user_responses[question] = response

    # Check if all questions have been answered
    all_answered = all(user_responses.values())

    if st.button('Get AI tool Recommendation', key='get_recommendation') and all_answered:
        # Display a message indicating that the recommendation is being generated
        with st.spinner('Generating recommendations... This may take up to 1 to 2 minutes to get the best results. Thank you for your patience.'):
            dialog = "\n".join(f"Q: {q}\nA: {a}" for q, a in user_responses.items())
            recommended_hosting = recommend_hosting_with_ai(dialog, file_path)
        # Indentation starts here for the block under the if statement
            dialog = "\n".join(f"Q: {q}\nA: {a}" for q, a in user_responses.items())
            recommended_hosting = recommend_hosting_with_ai(dialog, file_path)
        # st.text_area("Recommended AI tool(s)", value=recommended_hosting, height=300)
        st.markdown(recommended_hosting, unsafe_allow_html=True)
    elif st.button('Check if all questions answered', key='check_answers') and not all_answered:
        # Indentation starts here for the block under the elif statement
        st.error("Please answer all questions before getting recommendations.")

if __name__ == "__main__":
    main()

