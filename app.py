from flask import Flask, render_template, request, session
from openai import OpenAI

app = Flask(__name__)
app.secret_key = 'f3d1d72d8701580aa94542ce04491a79'


client = OpenAI(api_key="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")  

def generate_trivia_question(topic):
    prompt = f"Generate a trivia question and its answer based on the topic: {topic}. Format it as 'Question: ... Answer: ...'"
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    content = response.choices[0].message.content
    if "Question:" in content and "Answer:" in content:
        question = content.split("Question:")[1].split("Answer:")[0].strip()
        answer = content.split("Answer:")[1].strip()
        return question, answer
    return "No question generated.", "Unknown"


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    topic = request.form['prompt']
    question, answer = generate_trivia_question(topic)
    session['question'] = question
    session['answer'] = answer
    return render_template('greet.html', question=question)


@app.route('/answer', methods=['POST'])
def answer():
    user_answer = request.form['topic']
    correct_answer = session.get('answer', '').lower()
    feedback = "✅ Correct!" if user_answer.strip().lower() == correct_answer else f"❌ Incorrect. The correct answer was: {session.get('answer')}"
    return render_template('greet.html', question=session.get('question'), feedback=feedback)

if __name__ == '__main__':
    app.run(debug=True)
