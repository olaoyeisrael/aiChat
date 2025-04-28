# from openai import OpenAI
# import os
# from dotenv import load_dotenv
# load_dotenv()

# client = OpenAI(
#     # base_url="https://router.huggingface.co/together/v1",
#     base_url="https://api.together.xyz/v1",
#     api_key=os.getenv('TOGETHER_API_KEY')
# )
# # def answer_question(question, context):
# #     try:
# #         print(context)
# #         prompt = f"""
# #         You are a smart academic tutor named *Israel Tutor*.

# # Use the information below to answer the question clearly and helpfully.

# # If the information isn't sufficient or relevant, respond with:
# # "I'm sorry, I don't have enough information to answer that question accurately."

# # Do not mention that you are using context.

# # Format your answer in Markdown using:
# # - **Headings**
# # - Bullet points
# # - Step-by-step explanation if needed

# # ---

# # ### Information:
# # {context}

# # ---

# # ### Question:
# # {question}

# # ---

# # ### Answer:
# # """

    

# #         completion = client.chat.completions.create(
# #             model="meta-llama/Llama-4-Scout-17B-16E-Instruct",
# #             messages = [
# #                 {"role": "system", "content": "You are an academic assistant." },
# #                 { "role": "user", "content": prompt } 
# #             ],
# #             max_tokens=512,
# #         )

# #         return completion.choices[0].message.content

# #     except Exception as e:
# #         return f"❌ Error: {e}"

# def answer_question(question: str, context: str = None, chat_history: list=None, mode: str = "rag") -> tuple:
#     try:
#         if mode == "chat" or not context:
#             prompt = f"You are a friendly assistant named Lextorah Tutor.\n\nUser: {question}\nAssistant:"
#         else:
#             chat_history.append({"role": "user", "content": question})
# #             prompt = f"""
# # You're a friendly tutor named *Lextorah Tutor*. Your goal is not to give direct answers, but to **guide students with questions** and help them think critically.

# # Start by asking the student what they already know about the topic, then follow up with clarifying questions that lead them to the correct concept.

# # ---

# # ### Student's Question:
# # {question}

# # ---

# # ### Your Response (as the tutor):
# # """.strip()
     
# #             prompt = f"""
# # You are a smart academic tutor named *Lextorah Tutor*.

# # Use the following information if it is relevant, but always do your best to answer the question — even if the information is not very related.

# # Do not mention "context" or say whether the information is sufficient or not.

# # Format your answer in **Markdown** using:
# # - **Headings**
# # - Bullet points
# # - Step-by-step explanations if needed

# # ---

# # ### Information:
# # {context}

# # ---

# # ### Question:
# # {question}

# # ---

# # ### Answer:
# # """.strip()
        
#         completion = client.chat.completions.create(
#             model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
#             messages=chat_history,
#             max_tokens=512,
#             temperature=0.3 if mode == "rag" else 0.7
#         )
    
#         res = completion.choices[0].message.content
#         return res, chat_history

#     except Exception as e:
#         return f"❌ Error: {e}"
    
# # def classify_query_type(question: str) -> str:
# #     prompt = f"""
# # Classify the following user input as either:

# # - "chitchat" → casual talk like greetings, thanks, small talk
# # - "knowledge" → academic or factual questions

# # Respond with one word: chitchat or knowledge.

# # Input: "{question}"
# # Answer:
# # """

# #     try:
        
# #         response = client.chat.completions.create(
# #             model="meta-llama/Llama-4-Scout-17B-16E-Instruct",
# #             messages=[{"role": "user", "content": prompt}],
# #             max_tokens=1
# #         )
        
# #         return response.choices[0].message.content.strip().lower()

# #     except Exception as e:
# #         return "knowledge"  

from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://api.together.xyz/v1",
    api_key=os.getenv('TOGETHER_API_KEY')
)


def answer_question(user_message: str,context: str, chat_history: list) -> tuple:
    try:
        system_prompt = system_prompt = (
                    "You are Lextorah Tutor, a Socratic academic assistant. "
                    "Guide students by asking critical thinking questions rather than giving direct answers. "
                    "Use the provided information only if it is helpful to answer the student's question. "
                    "**If the context is not helpful or not related, ignore it and answer normally.** "
                    "Do not mention the word 'context'. "
                    f"\n\n### Information:\n{context}\n"
                )
    
        # Add user's new question to history
        chat_history.append({"role": "user", "content":user_message})

        # Build special system prompt INCLUDING context
        
        print(chat_history, "1")
        # Replace the first system message (dynamic system prompt now)
        chat_history[0] =  {"role": "system", "content": system_prompt}
        print(chat_history)

        # Call Together API
        completion = client.chat.completions.create(
            model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
            messages=chat_history,
            max_tokens=512,
            temperature=0.5
        )

        assistant_message = completion.choices[0].message.content.strip()

        # Append assistant reply
        chat_history.append({"role": "assistant", "content": assistant_message})

        return assistant_message, chat_history

    except Exception as e:
        return f"❌ Error: {e}", chat_history