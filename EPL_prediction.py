import dash
from dash import dcc, html, Input, Output, State
from dash.dependencies import ALL
import plotly.graph_objs as go
import numpy as np
import plotly.graph_objects as go
from tensorflow.keras.models import load_model

# โหลดโมเดลที่ผ่านการเทรน
model = load_model("FP_model.h5")


def predict_match(home_team, away_team):
    # ตัวอย่างการเข้ารหัสทีม (แปลงชื่อทีมให้เป็นค่าที่โมเดลเข้าใจได้)
    team_mapping = {team: idx for idx, team in enumerate(teams.keys())}
    
    if home_team not in team_mapping or away_team not in team_mapping:
        return 0.0, 0.0, 0.0  # กรณีเกิดข้อผิดพลาด

    home_team_id = team_mapping[home_team]
    away_team_id = team_mapping[away_team]

    # เตรียมข้อมูลอินพุต (ปรับขนาดตามที่โมเดลต้องการ)
    required_timesteps = model.input_shape[1]  # จำนวนจุดข้อมูลที่โมเดลต้องการ
    padded_input = np.zeros((1, required_timesteps, 1), dtype=np.float32)  # สร้างข้อมูลอินพุตที่เติมศูนย์
    padded_input[0, :2, 0] = [home_team_id, away_team_id]  # เติม ID ของทีม home และ away

    # ทำการพยากรณ์ผลลัพธ์
    prediction = model.predict(padded_input)
    
    # คาดการณ์จะอยู่ในรูปแบบของ [home_prob, draw_prob, away_prob]
    home_prob, draw_prob, away_prob = prediction[0]

    # ตรวจสอบว่าผลลัพธ์ทั้งหมดรวมกันยังคงเป็น 1 (หรือลดความคลาดเคลื่อนเล็กน้อย)
    total = home_prob + draw_prob + away_prob
    home_prob /= total
    draw_prob /= total
    away_prob /= total

    return home_prob, draw_prob, away_prob


# Team data with logos
teams = {
    "Arsenal": "assets/arsenal.png",
    "Aston Villa": "assets/aston_villa.png", 
    "Bournemouth": "assets/bournemouth.png",
    "Brentford": "assets/brentford.png", 
    "Brighton": "assets/brighton.png", 
    "Southampton": "assets/southampton.png",
    "Chelsea": "assets/chelsea.png", 
    "Crystal Palace": "assets/crystal_palace.png", 
    "Everton": "assets/everton.png",
    "Fulham": "assets/fulham.png", 
    "Liverpool": "assets/liverpool.png", 
    "Ipswich": "assets/ipswich.png",
    "Manchester City": "assets/Manchester_city.png", 
    "Manchester United": "assets/manchester_united.png", 
    "Newcastle United": "assets/newcastle.png",
    "Nottingham Forest": "assets/nottingham_forest.png", 
    "Leicester": "assets/leicester.png", 
    "Tottenham Hotspur": "assets/Tottenham_Hotspur.png",
    "West Ham": "assets/west_ham.png", 
    "Wolverhampton": "assets/Wolverhampton.png"
}

# Create Dash app
app = dash.Dash(__name__)
app.title = 'Premier League Match Predictor 2024-2025'

# App layout
app.layout = html.Div([
    html.Div([
        html.Img(
            src="assets/banner.png",  # ระบุที่อยู่รูปภาพ
            style={
                'width': '100%',  # ให้รูปภาพเต็มความกว้างของหน้าจอ
                'height': 'auto',  # ปรับความสูงอัตโนมัติเพื่อรักษาสัดส่วน
                'display': 'block', 
                'margin': '0 auto'
            }
        )
    ]),
    
    html.H1('SEASON 2024-2025', style={'textAlign': 'center', 'color': 'white'}),
    
    html.Div([
        html.Div([
            html.H2('HOME', style={'textAlign': 'center', 'color': 'red'}),
            html.Div(id='home-selection', style={'textAlign': 'center', 'fontSize': '18px', 'marginBottom': '10px'}),
            html.Div(id='home-buttons', style={'display': 'grid', 'gridTemplateColumns': 'repeat(4, 1fr)', 'gap': '10px'})
        ], style={'flex': '1', 'padding': '20px'}),

        html.Div([
            html.H2('AWAY', style={'textAlign': 'center', 'color': 'blue'}),
            html.Div(id='away-selection', style={'textAlign': 'center', 'fontSize': '18px', 'marginBottom': '10px'}),
            html.Div(id='away-buttons', style={'display': 'grid', 'gridTemplateColumns': 'repeat(4, 1fr)', 'gap': '10px'})
        ], style={'flex': '1', 'padding': '20px'})
    ], style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center'}),

    html.Div(
    html.Button(
        'PREDICT',
        id='predict-button',
        disabled=True,
        style={
            'margin': '20px',
            'padding': '10px 20px',
            'fontSize': '20px',
            'backgroundColor': '#0fdc51',
            'border': '1px solid black',
            'borderRadius': '10px',
            'cursor': 'pointer'
        }
    ),
    style={
        'display': 'flex',
        'justifyContent': 'center',
        'alignItems': 'center'
    }
),

    dcc.Graph(id='prediction-chart')
], style={
    'backgroundColor': '#a486fe',  # ตั้งค่าสีพื้นหลัง
    'minHeight': '100vh',         # ให้ความสูงเต็มหน้าจอ
    'padding': '10px'             # เพิ่ม padding เล็กน้อยรอบเนื้อหา
    })

@app.callback(
    [Output('predict-button', 'disabled'),
     Output('home-selection', 'children'),
     Output('away-selection', 'children'),
     Output('home-buttons', 'children'),
     Output('away-buttons', 'children')],
    [Input({'type': 'home-button', 'index': ALL}, 'n_clicks'),
     Input({'type': 'away-button', 'index': ALL}, 'n_clicks')]
)

def update_team_selection(home_clicks, away_clicks):
    home_clicks = home_clicks or [0] * len(teams)
    away_clicks = away_clicks or [0] * len(teams)
    
    home_team = [team for team, n in zip(teams.keys(), home_clicks) if n % 2 == 1]
    away_team = [team for team, n in zip(teams.keys(), away_clicks) if n % 2 == 1]
    
    home_display = home_team[0] if home_team else "Select any Team"
    away_display = away_team[0] if away_team else "Select any Team"
    
    home_buttons = [
        html.Button(
            [html.Img(src=teams[team], style={'width': '70px', 'height': '70px', 'objectFit': 'contain'}), html.Br(), team],
            id={'type': 'home-button', 'index': team},
            n_clicks=home_clicks[i] if i < len(home_clicks) else 0,
            style={
                'width': '120px', 'height': '120px', 'margin': '5px',
                'borderRadius': '15px', 'backgroundColor': '#ddd' if team in home_team else 'white',
                'border': '1px solid #ddd'
            }
        ) for i, team in enumerate(teams.keys())
    ]

    away_buttons = [
        html.Button(
            [html.Img(src=teams[team], style={'width': '70px', 'height': '70px', 'objectFit': 'contain'}), html.Br(), team],
            id={'type': 'away-button', 'index': team},
            n_clicks=away_clicks[i] if i < len(away_clicks) else 0,
            style={
                'width': '120px', 'height': '120px', 'margin': '5px',
                'borderRadius': '15px', 'backgroundColor': '#ddd' if team in away_team else 'white',
                'border': '1px solid #ddd'
            }
        ) for i, team in enumerate(teams.keys())
    ]
    
    return not (len(home_team) == 1 and len(away_team) == 1 and home_team[0] != away_team[0]), home_display, away_display, home_buttons, away_buttons

@app.callback(
    Output('prediction-chart', 'figure'),
    Input('predict-button', 'n_clicks'),
    [State({'type': 'home-button', 'index': ALL}, 'n_clicks'),
     State({'type': 'away-button', 'index': ALL}, 'n_clicks')]
)
def update_prediction(n_clicks, home_clicks, away_clicks):
    if n_clicks:
        home_team = [team for team, n in zip(teams.keys(), home_clicks) if n % 2 == 1][0]
        away_team = [team for team, n in zip(teams.keys(), away_clicks) if n % 2 == 1][0]
        home_prob, draw_prob, away_prob = predict_match(home_team, away_team)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=['Match Prediction'],
            x=[home_prob * 100],
            name=home_team,
            marker_color='red',
            orientation='h',
            text=f'{home_prob*100:.1f}%',
            textposition='inside'
        ))
        fig.add_trace(go.Bar(
            y=['Match Prediction'],
            x=[draw_prob * 100],
            name='Draw',
            marker_color='gray',
            orientation='h',
            text=f'{draw_prob*100:.1f}%',
            textposition='inside'
        ))
        fig.add_trace(go.Bar(
            y=['Match Prediction'],
            x=[away_prob * 100],
            name=away_team,
            marker_color='blue',
            orientation='h',
            text=f'{away_prob*100:.1f}%',
            textposition='inside'
        ))
        
        fig.update_layout(
            barmode='stack',
            title={'text': 'RESULT', 'x': 0.5, 'xanchor': 'center'},
            xaxis={'title': 'Probability (%)', 'range': [0, 100]},
            yaxis={'title': '', 'scaleanchor': "x", 'scaleratio': 0.5},
            showlegend=True,
            height=300
        )
        
        return fig
    return go.Figure()

if __name__ == '__main__':
    app.run_server(debug=False)