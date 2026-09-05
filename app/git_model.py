import os
from openai import OpenAI

endpoint= "https://generativelanguage.googleapis.com/v1beta/openai/"
model= "gemini-3.5-flash-lite"

clients = {}

def get_client(token):
    if token not in clients:
        clients[token] = OpenAI(
            base_url=endpoint,
            api_key=token
        )
    return clients[token]

def generate(prompt, token):
    client= get_client(token)
    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                # "content": "jawablah dengan pilihan gandanya saja atau hurufnya saja tanpa titik",
                "content": "Jawab hanya dengan satu huruf pilihan (A, B, C, D, atau E) tanpa teks tambahan.",
            },
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model=model,
        temperature=0
    )
    return response.choices[0].message.content
