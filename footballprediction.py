from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
import tensorflow as tf
import numpy as np
import joblib
import requests
from io import BytesIO

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Banner Section (30%)
        self.banner = Image(source='banner.png', size_hint=(1, 0.3))
        layout.add_widget(self.banner)
        
        # Team Logos Section (30%)
        self.team_layout = GridLayout(cols=2, size_hint=(1, 0.3))
        self.home_logo = Image(size_hint=(None, None), height=Window.height * 0.3)  # Maintain aspect ratio
        self.away_logo = Image(size_hint=(None, None), height=Window.height * 0.3)  # Maintain aspect ratio
        self.team_layout.add_widget(self.home_logo)
        self.team_layout.add_widget(self.away_logo)
        layout.add_widget(self.team_layout)
        
        # Team Names Section (15%)
        self.team_name_layout = GridLayout(cols=2, size_hint=(1, 0.15))
        self.home_team_input = TextInput(hint_text='Enter Home Team')
        self.away_team_input = TextInput(hint_text='Enter Away Team')
        self.home_team_input.bind(on_text_validate=self.update_home_logo)
        self.away_team_input.bind(on_text_validate=self.update_away_logo)
        self.team_name_layout.add_widget(self.home_team_input)
        self.team_name_layout.add_widget(self.away_team_input)
        layout.add_widget(self.team_name_layout)
        
        # Last 5 Matches Section (10%)
        self.matches_layout = GridLayout(cols=2, size_hint=(1, 0.1), spacing=30)  # Increased spacing
        self.home_matches = GridLayout(cols=5, spacing=10)  # Spacing between inputs
        self.away_matches = GridLayout(cols=5, spacing=10)  # Spacing between inputs
        
        self.home_last_5_inputs = []
        self.away_last_5_inputs = []
        
        for i in range(5):
            home_input = TextInput(multiline=False, size_hint_x=None, width=40)
            away_input = TextInput(multiline=False, size_hint_x=None, width=40)
            
            home_input.bind(text=self.auto_tab_home)
            away_input.bind(text=self.auto_tab_away)
            
            self.home_last_5_inputs.append(home_input)
            self.away_last_5_inputs.append(away_input)
            
            self.home_matches.add_widget(home_input)
            self.away_matches.add_widget(away_input)
        
        self.matches_layout.add_widget(self.home_matches)
        self.matches_layout.add_widget(self.away_matches)
        layout.add_widget(self.matches_layout)
        
        # Predict Button (15%)
        self.predict_button = Button(text='Predict', background_color=(0, 1, 0, 1), size_hint=(1, 0.15))
        self.predict_button.bind(on_press=self.predict_result)
        layout.add_widget(self.predict_button)
        
        self.add_widget(layout)

    def update_home_logo(self, instance):
        self.home_logo.source = self.get_team_logo(instance.text)
    
    def update_away_logo(self, instance):
        self.away_logo.source = self.get_team_logo(instance.text)
    
    def auto_tab_home(self, instance, value):
        if len(value) == 1:
            index = self.home_last_5_inputs.index(instance)
            if index < 4:
                self.home_last_5_inputs[index + 1].focus = True
    
    def auto_tab_away(self, instance, value):
        if len(value) == 1:
            index = self.away_last_5_inputs.index(instance)
            if index < 4:
                self.away_last_5_inputs[index + 1].focus = True
    
    def get_team_logo(self, team_name):
        # Simulated: Replace with real API call to fetch first image from Google
        return f'teamlogo/{team_name.lower().replace(" ", "_")}.png'
    
    def predict_result(self, instance):
        self.manager.get_screen('result_screen').set_winner(self.home_logo.source)  # Example winner
        self.manager.current = 'result_screen'

class ResultScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.winner_logo = Image(size_hint=(1, 0.4))
        layout.add_widget(self.winner_logo)
        self.result_label = Label(text='WIN', color=(0, 1, 0, 1), font_size=50, size_hint=(1, 0.2))
        layout.add_widget(self.result_label)
        self.add_widget(layout)
    
    def set_winner(self, team_logo):
        self.winner_logo.source = team_logo

class FootballPredictionApp(App):
    def build(self):
        sm = ScreenManager()
        self.main_screen = MainScreen(name='main_screen')
        self.result_screen = ResultScreen(name='result_screen')
        sm.add_widget(self.main_screen)
        sm.add_widget(self.result_screen)
        return sm
    
if __name__ == '__main__':
    FootballPredictionApp().run()
