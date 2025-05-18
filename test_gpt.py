from transformers import pipeline, set_seed

generator = pipeline("text-generation", model="gpt2")
set_seed(42)

output = generator(
    "Create a game board layout for 4 tiles:", max_length=100, num_return_sequences=1
)
print(output[0]["generated_text"])
