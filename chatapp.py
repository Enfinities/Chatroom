from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# In-memory storage for chatrooms (replace with a proper database in production)
chatrooms = {}

# Discord webhook URL (replace with your actual URL)
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1276309974015803484/BY9LSi-RlZk6Iyh1dLcqFMVjqJEgl7ozaDT00f3wuIfiE_7B4z2f3nGJgYuDiV5i9m-M"


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        session['username'] = username
        return redirect(url_for('chatroom_options'))
    return render_template('index.html')


@app.route('/options', methods=['GET', 'POST'])
def chatroom_options():
    if request.method == 'POST':
        option = request.form['option']
        if option == 'join':
            return redirect(url_for('join'))
        elif option == 'create':
            code = str(len(chatrooms) + 1)  # Generate a simple code (e.g., '1', '2', etc.)
            chatrooms[code] = []
            return redirect(url_for('chatroom', code=code))
    return render_template('chatroom_options.html')


@app.route('/join', methods=['GET', 'POST'])
def join_chatroom():
    if request.method == 'POST':
        code = request.form['code']
        if code in chatrooms:
            return redirect(url_for('chatroom', code=code))
    return render_template('join.html')


@app.route('/chat/<code>', methods=['GET', 'POST'])
def chatroom(code):
    if code not in chatrooms:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = session.get('username', 'Anonymous')
        message = request.form['message']
        chatrooms[code].append({'user': username, 'message': message})

        # Send message to Discord webhook
        post_to_discord(f"{username}: {message}")

    return render_template('chatroom.html', code=code, messages=chatrooms[code])


@app.route('/get_messages/<code>', methods=['GET'])
def get_messages(code):
    messages = chatrooms.get(code, [])
    return jsonify(messages)


def post_to_discord(message):
    data = {"content": message}
    response = requests.post(DISCORD_WEBHOOK_URL, json=data)
    if response.status_code == 204:
        print("Message posted to Discord successfully!")
    else:
        print(f"Failed to post to Discord: {response.status_code}")


if __name__ == '__main__':
    app.run(debug=True)
