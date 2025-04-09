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
    'bowling_team': 'Team B',
    'is_first_innings': True,
    'first_innings_score': 0,
    'is_all_out': False,
    'target': 0,
    'result': None
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
    
    if score['is_all_out']:
        return jsonify({'error': 'Innings is over'}), 400
    
    if 'runs' in data:
        score['runs'] += data['runs']
        if not score['is_first_innings'] and score['runs'] > score['target']:
            score['result'] = f"{score['batting_team']} won by {10 - score['wickets']} wickets"
            score['is_all_out'] = True
    if 'wickets' in data:
        if score['wickets'] < 10:
            score['wickets'] += data['wickets']
            if score['wickets'] >= 10:
                score['is_all_out'] = True
                if score['is_first_innings']:
                    score['first_innings_score'] = score['runs']
                    score['target'] = score['runs'] + 1
                    score['runs'] = 0
                    score['wickets'] = 0
                    score['overs'] = 0
                    score['balls'] = 0
                    score['is_first_innings'] = False
                    score['batting_team'], score['bowling_team'] = score['bowling_team'], score['batting_team']
                else:
                    if score['runs'] < score['target']:
                        score['result'] = f"{score['bowling_team']} won by {score['target'] - score['runs']} runs"
                    elif score['runs'] == score['target']:
                        score['result'] = "Match Tied"
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
        'batting_team': score['team1'],
        'bowling_team': score['team2'],
        'is_first_innings': True,
        'first_innings_score': 0,
        'is_all_out': False,
        'target': 0,
        'result': None
    }
    return jsonify(score)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001) 