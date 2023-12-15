import openai

openai.api_key = "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"

def text_generator(prompt):
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        temperature=0.1,
        max_tokens=150)
    return response.choices[0].text