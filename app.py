from flask import Flask, render_template, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Initial score state
score = {
    'runs': 0,
    'wickets': 0,
    'overs': 0,
    'balls': 0,
    'team1': 'Team A',
    'team2': 'Team B',
    'batting_team': 'Team A',
    'bowling_team': 'Team B'
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/score', methods=['GET'])
def get_score():
    return jsonify(score)

@app.route('/api/update', methods=['POST'])
def update_score():
    global score
    data = request.json
    
    if 'runs' in data:
        score['runs'] += data['runs']
    if 'wickets' in data:
        score['wickets'] += data['wickets']
    if 'balls' in data:
        score['balls'] += data['balls']
        if score['balls'] == 6:
            score['overs'] += 1
            score['balls'] = 0
    
    return jsonify(score)

@app.route('/api/reset', methods=['POST'])
def reset_score():
    global score
    score = {
        'runs': 0,
        'wickets': 0,
        'overs': 0,
        'balls': 0,
        'team1': score['team1'],
        'team2': score['team2'],
        'batting_team': score['batting_team'],
        'bowling_team': score['bowling_team']
    }
    return jsonify(score)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001) 