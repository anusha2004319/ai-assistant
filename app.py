from flask import Flask, render_template, request
from openai import OpenAI

# Replace with your actual OpenAI API key
client = OpenAI(api_key="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")

app = Flask(__name__)

def ask_openai(prompt, temperature=0.7):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # or use "gpt-4" if your key supports it
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=temperature,
        max_tokens=500
    )
    return response.choices[0].message.content.strip()

@app.route('/', methods=['GET', 'POST'])
def index():
    result = ""
    if request.method == 'POST':
        task = request.form.get('task')
        user_input = request.form.get('user_input')
        feedback = request.form.get('feedback')

        if task == "answer":
            prompt = f"Answer the following factual question:\n{user_input}"
            result = ask_openai(prompt, temperature=0.3)
        elif task == "summarize":
            prompt = f"Summarize the following text:\n{user_input}"
            result = ask_openai(prompt)
        elif task == "creative":
            prompt = f"Generate a creative output based on this input:\n{user_input}"
            result = ask_openai(prompt, temperature=0.9)

        if feedback:
            with open("feedback_log.txt", "a") as f:
                f.write(f"\n---\nTask: {task}\nInput: {user_input}\nResponse: {result}\nFeedback: {feedback}\n")

    return render_template('index.html', result=result)
if __name__ == '__main__':
    app.run(debug=True)
