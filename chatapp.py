from flask import Flask, render_template, request, redirect, url_for, session
import random
import string

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# In-memory store for chatrooms and messages
chatrooms = {}

# Home page: Choose a username
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('chatroom_options'))
    return render_template('index.html')

# Chatroom options: Join or create
@app.route('/chatroom-options', methods=['GET', 'POST'])
def chatroom_options():
    if request.method == 'POST':
        option = request.form['option']
        if option == 'join':
            return redirect(url_for('join_chatroom'))
        elif option == 'create':
            return redirect(url_for('create_chatroom'))
    return render_template('chatroom_options.html')

# Join a chatroom
@app.route('/join', methods=['GET', 'POST'])
def join_chatroom():
    if request.method == 'POST':
        code = request.form['code']
        if code in chatrooms:
            session['chatroom'] = code
            return redirect(url_for('chatroom', code=code))
        else:
            return "Chatroom not found!", 404
    return render_template('join.html')

# Create a chatroom
@app.route('/create', methods=['GET'])
def create_chatroom():
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    chatrooms[code] = []
    session['chatroom'] = code
    return redirect(url_for('chatroom', code=code))

# Chatroom page
@app.route('/chatroom/<code>', methods=['GET', 'POST'])
def chatroom(code):
    if request.method == 'POST':
        message = request.form['message']
        chatrooms[code].append({'user': session['username'], 'message': message})
    messages = chatrooms[code]
    return render_template('chatroom.html', code=code, messages=messages)

if __name__ == "__main__":
    app.run(debug=True)
