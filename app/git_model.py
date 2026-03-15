import os
from openai import OpenAI

endpoint = "https://models.github.ai/inference"
model = "openai/gpt-4.1-nano"

clients = {}

def get_client(token):
    if token not in clients:
        clients[token] = OpenAI(
            base_url="https://models.github.ai/inference",
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
