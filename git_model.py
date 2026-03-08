import os
from openai import OpenAI

#cmd => set GITHUB_TOKEN= token
token = os.environ["GITHUB_TOKEN"]
endpoint = "https://models.github.ai/inference"
model = "openai/gpt-4.1-nano"

client = OpenAI(
    base_url=endpoint,
    api_key=token,
)
def generate(prompt):
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
