from core.llm.kern_chat import kern_chat

response = kern_chat([
    {"role": "user", "content": "Why do I keep sabotaging my own momentum?"}
])

print(response.choices[0].message.content)
