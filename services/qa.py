from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(
    # base_url="https://router.huggingface.co/together/v1",
    base_url="https://api.together.xyz/v1",
    api_key=os.getenv('TOGETHER_API_KEY')
)
# def answer_question(question, context):
#     try:
#         print(context)
#         prompt = f"""
#         You are a smart academic tutor named *Israel Tutor*.

# Use the information below to answer the question clearly and helpfully.

# If the information isn't sufficient or relevant, respond with:
# "I'm sorry, I don't have enough information to answer that question accurately."

# Do not mention that you are using context.

# Format your answer in Markdown using:
# - **Headings**
# - Bullet points
# - Step-by-step explanation if needed

# ---

# ### Information:
# {context}

# ---

# ### Question:
# {question}

# ---

# ### Answer:
# """

    

#         completion = client.chat.completions.create(
#             model="meta-llama/Llama-4-Scout-17B-16E-Instruct",
#             messages = [
#                 {"role": "system", "content": "You are an academic assistant." },
#                 { "role": "user", "content": prompt } 
#             ],
#             max_tokens=512,
#         )

#         return completion.choices[0].message.content

#     except Exception as e:
#         return f"❌ Error: {e}"

def answer_question(question: str, context: str = None, mode: str = "rag") -> str:
    try:
        if mode == "chat" or not context:
            prompt = f"You are a friendly assistant named Lextorah Tutor.\n\nUser: {question}\nAssistant:"
        else:
            prompt = f"""
You are a smart academic tutor named *Lextorah Tutor*.

Use the following information if it is relevant, but always do your best to answer the question — even if the information is not very related.

Do not mention "context" or say whether the information is sufficient or not.

Format your answer in **Markdown** using:
- **Headings**
- Bullet points
- Step-by-step explanations if needed

---

### Information:
{context}

---

### Question:
{question}

---

### Answer:
""".strip()
        completion = client.chat.completions.create(
            model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
            messages=[
                { "role": "system", "content": "You are an academic assistant." },
                { "role": "user", "content": prompt }
            ],
            max_tokens=512,
            temperature=0.3 if mode == "rag" else 0.7
        )
    
        return completion.choices[0].message.content

    except Exception as e:
        return f"❌ Error: {e}"
    
def classify_query_type(question: str) -> str:
    prompt = f"""
Classify the following user input as either:

- "chitchat" → casual talk like greetings, thanks, small talk
- "knowledge" → academic or factual questions

Respond with one word: chitchat or knowledge.

Input: "{question}"
Answer:
"""

    try:
        
        response = client.chat.completions.create(
            model="meta-llama/Llama-4-Scout-17B-16E-Instruct",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1
        )
        
        return response.choices[0].message.content.strip().lower()

    except Exception as e:
        return "knowledge"  