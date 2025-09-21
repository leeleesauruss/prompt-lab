import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="PromptLab", layout="wide")  

# Streamlit app layout
st.title('PromptLab')

# Create two columns for the Shinobi and Raikage buttons
col1, col2 = st.columns(2)

mode = st.radio("Choose a mode:", ["Proficient Level", "Apex Level"], horizontal=True)

# Retrieve the API key from Streamlit secrets
GOOGLE_API_KEY = st.secrets["GEMINI_API_KEY"]

# Configure the Google Generative AI API with your API key
genai.configure(api_key=GOOGLE_API_KEY)

# Input field for the blog topic
topic = st.text_area('Enter your prompt:')

# Display selected mode
st.write(f"You selected: {mode}")


# Shinobi and Raikage templates
Proficient_TEMPLATE = """
Analyze the following user prompt and transform it into an enhanced, structured prompt following these steps:

1. Determine the primary subject area and required expertise level
2. Formulate an expert persona introduction ("You are an expert in [subject]")
3. Define the user-AI interaction pattern
4. Create appropriate response structure:
   a. For simple topics: Use general formatting guidelines
   b. For complex topics: Create numbered sections with descriptive headers
   c. Adjust detail level based on topic complexity
5. Specify content requirements (examples, definitions, code samples, etc.)
6. Include quality guidelines for clarity, conciseness, and accessibility
7. Preserve the original user prompt at the end marked with "Input:"

Enhance the following prompt using this **structured, Proficient-level framework:**           

**Original Prompt:**  
{user_prompt}  

**Enhanced Prompt:**  
(Apply the Primer framework to generate the improved version)

"""

Apex_TEMPLATE = """
You are an elite-level [role] with deep expertise in [subject].  
Your task is to develop a structured, high-quality response following these key elements:  

## **Context**  
[Provide background information related to the task to frame the problem.]  

## **Approach**  
[Define a **step-by-step** breakdown of how to achieve the goal, focusing on methodology and best practices.]  

## **Response Format**  
[Specify the expected output structure, ensuring clarity and completeness.]  

## **Instructions**  
- [Ensure high-quality standards, best practices, and possible constraints.]  
- [Emphasize documentation, flexibility, and potential edge cases.]  

Enhance the following prompt using this **structured, expert-level framework:**  

**Original Prompt:**  
{user_prompt}  

**Enhanced Prompt:**  
(Apply the Mastermind framework to generate the improved version)    
"""
if st.button("Generate Enhanced Prompt"):
    if topic.strip():
        with st.spinner("Enhancing your prompt..."):
            # Choose the template based on the selected mode
            if mode == "Shinobi":
                prompt = Proficient_TEMPLATE.format(user_prompt=topic)
            else:
                prompt = Apex_TEMPLATE.format(user_prompt=topic)

            # Initialize the generative model
            model = genai.GenerativeModel('gemini-2.0-flash')

            # Generate enhanced prompt
            try:
                response = model.generate_content(prompt)
                enhanced_prompt = response.text  # Extract the response text
                st.subheader("🔹 Enhanced Prompt:")
                st.write(enhanced_prompt)  
            except Exception as e:
                st.error(f"❌ Error generating enhanced prompt: {e}")
    else:
        st.warning("⚠️ Please enter a prompt before generating.")
