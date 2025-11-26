import os
from google import genai
from google.genai import types
import streamlit as st

class Coach:
    def __init__(self, mode="Easy", api_key=None):
        self.mode = mode
        self.api_key = api_key
        
    def _get_system_instruction(self, stats):
        """
        Constructs the system instruction based on mode and user stats.
        """
        base_instruction = f"""
        You are a health coach for a user with the following stats:
        - Average Steps: {int(stats.get('steps', 0))}
        - Missed Gym Days (Recent): {stats.get('missed_gym_days', 0)}
        - Recent Cheat Meals: {stats.get('recent_cheats', 0)}
        - Health Score: {stats.get('health_score', 0)}
        
        Your goal is to provide qualitative advice and insights based on this data.
        """
        
        if self.mode == "Easy":
            return base_instruction + """
            Persona: Supportive, gentle, encouraging. 
            Tone: Warm, positive, understanding.
            Directives: 
            - Focus on the small wins.
            - If stats are low, kindly suggest small improvements.
            - Never be harsh.
            """
        elif self.mode == "Accountability":
            return base_instruction + """
            Persona: Tough Love, Drill Sergeant, Witty.
            Tone: Direct, slightly sarcastic, demanding.
            Directives:
            - Roast the user for bad habits (low steps, missed gym).
            - If they miss the gym > 3 days, threaten to block their pizza orders.
            - Be ruthless but funny.
            - Use emojis like 😤, 🛑, 💪.
            """
        return base_instruction

    def generate_response(self, user_input, stats, chat_history):
        """
        Generates a response using Google GenAI.
        chat_history: List of dicts [{"role": "user", "content": "..."}, ...]
        """
        if not self.api_key:
            return "Error: API Key not provided. Please set GEMINI_API_KEY."

        try:
            client = genai.Client(api_key=self.api_key)
            
            system_instruction = self._get_system_instruction(stats)
            
            # Convert history to GenAI format
            formatted_history = []
            for msg in chat_history:
                role = "user" if msg["role"] == "user" else "model"
                formatted_history.append(
                    types.Content(
                        role=role,
                        parts=[types.Part(text=msg["content"])]
                    )
                )
            
            # Create chat session
            chat = client.chats.create(
                model="gemini-2.0-flash",
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.7,
                ),
                history=formatted_history
            )
            
            response = chat.send_message(user_input)
            return response.text
            
        except Exception as e:
            return f"Error connecting to Coach: {str(e)}"

    def check_cheat_meal_block(self, recent_activity):
        """
        Returns True if cheat meals should be blocked.
        Rule: Block if missed gym 3 days in a row.
        Unblock only after 10 consecutive valid gym sessions.
        """
        if self.mode != "Accountability":
            return False
            
        # Simplified logic for prototype:
        # Check last 3 days. If all have 0 valid gym, block.
        last_3_days = recent_activity.sort_values('date', ascending=False).head(3)
        valid_sessions = last_3_days[last_3_days['is_gym_valid']].shape[0]
        
        if valid_sessions == 0:
            return True
            
        return False
