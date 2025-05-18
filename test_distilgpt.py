from transformers import pipeline, set_seed

# بارگذاری مدل سبک
generator = pipeline("text-generation", model="distilgpt2")
set_seed(42)

prompt = "Generate a layout for 8 colored game tiles in a 600x600 space:"
output = generator(prompt, max_length=100, num_return_sequences=1)

print("🔹 Prompt:")
print(prompt)
print("\n🔸 Output:")
print(output[0]["generated_text"])
