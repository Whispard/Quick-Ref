import openai
openai.api_key = ""

prompt = "Summarize : dog laughed so bad it ruined party"

response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]
)

print(response)
print(response["choices"][0]["message"]["content"])