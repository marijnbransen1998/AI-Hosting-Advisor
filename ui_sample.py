import streamlit as st
import os
# set openai api key for streamlit

import openai
import pandas as pd

# Set your OpenAI API key here
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
openai.api_key = OPENAI_API_KEY

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


def recommend_hosting_with_ai(dialog, transposed_ai_tools7_csv):
    # Read the CSV data into a string format suitable for the prompt
    hosting_data = pd.read_csv(transposed_ai_tools7_csv)
    hosting_data_string = hosting_data.to_string(index=False)

    # construct the prompt
    prompt = (f"Based on the following user answers:\n{dialog}\n\n"
          f"Act as an AI tool advisor. Use the AI tools data from {hosting_data_string} to match AI tools with the user's needs from the {dialog}. Focus on tools whose 'Features', 'Suitable For', and 'Pros' from the {hosting_data_string} that align with the user's requirements:\n{dialog}\n\n"
          "Recommendations:\n"
    "- List all the tools from the {hosting_data_string} dataset that match with the user requests from the {dialog}\n" 
    "- List at least 7 recommendations of possible tools \n" 
    "- Please match them mainly on the basis of keyword match.\n"
    "- Try to list tools that are matching and DO NOT make up matches. If a tool is not an exact match than tell this in the explanation.\n" 
    "- In any case do not list more than 10 tools.\n"
    "- For each tool, include:\n"
    "   - **Name** (in bold)\n"
    "   - **Pricing** (in bold)\n"
    "   - **Website Link** (in bold)\n"
    "   - **Explanation** (in bold): Detail in minumum two sentences how each tool matches the user's needs based on their answers in 'dialog' and the tool's features, pros, and suitability from {hosting_data_string}.\n"
    "Note: Base recommendations solely on the {dialog} and {hosting_data_string} data.\n\n"
    "Closing Note:\n"
    "- Inform the user that recommendations are based on 'The 21 Best AI Tools' from tilburg.ai and may not be entirely accurate.\n"
    "- Inform the user that they generate recommendations more than once by simply changing their answers. \n"
    "- Inform the user that For more AI tool options, they can visit https://www.futuretools.io/ or read the full article at https://tilburg.ai/2024/01/best-ai-tools-for-university-students/\n")

    # Call the OpenAI API
    completion = openai.chat.completions.create(
        model="gpt-3.5-turbo-1106",  
        messages=[{"role": "user", "content": prompt}]
    )

    return completion.choices[0].message.content



def main():
    # Add the code to display the logo here
    logo_path = 'tilburg-ai.png'  # Replace with the actual path to your logo image
    # Define custom CSS style for logo positioning and size
    logo_css = """
    <style>
        /* Custom CSS styles for logo positioning and size */
        .logo-container {
            position: absolute;
            top: 10px; /* Adjust the top position as needed */
            left: 10px; /* Adjust the left position as needed for top-left */
        }
        .logo {
            width: 150px; /* Adjust the width as needed */
            height: auto; /* Maintain aspect ratio */
            display: block;
        }
    </style>
    """
    
    # Apply custom CSS for logo positioning and size
    st.markdown(logo_css, unsafe_allow_html=True)
    
     # Display the logo image
    st.image(logo_path, caption='', use_column_width=False)
    
    st.title("AI tool advisor for students")  # Set a title for your app

    # Load hosting data from CSV
    file_path = 'transposed_ai_tools7.csv'  # Update this with the path to your CSV file

    # Define the questions you're going to ask the user
    questions = [
        "What is your role? (Student, Teacher, Researcher, Academic, Professional, etc",
        "What specific tasks or needs do you have for the AI tool? (e.g., writing, coding support, only free tools, finding papers for thesis, data analysis). **Try to be as specific as possible!**"
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

    if st.button('Get AI tool Recommendation', key='get_recommendation'):
        if all_answered:
            # Display a message indicating that the recommendation is being generated
            with st.spinner('Generating recommendations... This may take up to 1 minute to get the best results. Thank you for your patience.'):
                dialog = "\n".join(f"Q: {q}\nA: {a}" for q, a in user_responses.items())
                recommended_hosting = recommend_hosting_with_ai(dialog, file_path)
            # Indentation starts here for the block under the if statement
                dialog = "\n".join(f"Q: {q}\nA: {a}" for q, a in user_responses.items())
                recommended_hosting = recommend_hosting_with_ai(dialog, file_path)
            # st.text_area("Recommended AI tool(s)", value=recommended_hosting, height=300)
            st.markdown(recommended_hosting, unsafe_allow_html=True)
        else:
            st.error("Please answer all questions before getting recommendations.")

if __name__ == "__main__":
    main()

