import gradio as gr
from openai import OpenAI

# Initialize OpenAI client with AIML API key
client = OpenAI(
    base_url="https://api.aimlapi.com/v1",
    api_key="0493dc14e46240348762be8b886d04aa"  # Replace with your actual API key
)

def chatbot(user_message):
    """Handles user queries while optimizing API usage."""
    if not user_message.strip():
        return "Please enter a valid question."

    try:
        # Send a single query to avoid multiple API calls
        response = client.chat.completions.create(
            model="deepseek/deepseek-r1",
            messages=[
                {"role": "system", "content": 
                 "You are an AI chatbot that provides expert engineering answers and optimization techniques."},
                {"role": "user", "content": f"Provide an answer and suggest optimizations for: {user_message}"}
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        if "429" in str(e):  
            return "You've reached the free API limit. Try again later or upgrade your plan."
        return f"Error: {e}"

# Create Gradio Interface
iface = gr.Interface(
    fn=chatbot,
    inputs=gr.Textbox(placeholder="Ask an engineering question..."),
    outputs="text",
    title="Engineering AI Chatbot",
    description="Ask about Civil, Chemical, Electrical, and other engineering fields. The chatbot also suggests optimizations."
)

# Launch the Gradio app
if __name__ == "__main__":
    iface.launch(server_name="0.0.0.0", server_port=7860)
