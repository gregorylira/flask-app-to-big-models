from huggingface_hub import InferenceClient
import os

client = InferenceClient(provider="novita", api_key=os.getenv("HUGGINGFACE_API_KEY"))


def process_text(text):
    messages = [{"role": "user", "content": text}]

    completion = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-R1",
        messages=messages,
        max_tokens=500,
    )

    return completion.choices[0].message
