import os
from transformers import pipeline, logging

logging.set_verbosity_error()

pipe = pipeline("text-generation", model="openai-community/gpt2")


def process_text(text):
    print("processando texto")
    completion = pipe(text, max_length=50, truncation=True, num_return_sequences=1)[0][
        "generated_text"
    ]
    print("texto processado")
    return completion
