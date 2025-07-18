"""
Groq AI Integration for Message Generation
Provides AI-powered message generation with multiple personas
"""

import os
import requests
import json
from typing import Dict, List, Optional


class GroqAI:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('GROQ_API_KEY')
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = "llama3-70b-8192"
        
        # Message generation personas
        self.personas = {
            'official': {
                'name': 'Professional Official',
                'system_prompt': """You are a professional business communicator. Generate formal, 
                respectful, and official business messages. Focus on clear communication, 
                professionalism, and proper business etiquette. Keep messages concise but complete."""
            },
            'spam': {
                'name': 'High-Converting Spam Expert',
                'system_prompt': """You are a master of high-converting direct marketing messages. 
                Create urgent, compelling messages that grab attention and drive immediate action. 
                Use psychological triggers, scarcity, urgency, and strong call-to-actions. 
                Be persuasive but not misleading."""
            },
            'marketer': {
                'name': 'Expert Marketing Professional',
                'system_prompt': """You are an expert marketing professional inspired by the best 
                marketers and copywriters. Create engaging, persuasive messages that build relationships 
                and drive results. Use storytelling, emotional triggers, and proven marketing psychology. 
                Focus on value proposition and customer benefits."""
            }
        }
    
    def set_api_key(self, api_key: str):
        """Set the Groq API key"""
        self.api_key = api_key
    
    def is_configured(self) -> bool:
        """Check if API key is configured"""
        return bool(self.api_key)
    
    def generate_message(self, persona: str, request: str, context: str = "") -> Dict[str, str]:
        """Generate message using specified persona"""
        if not self.is_configured():
            return {
                'success': False,
                'message': '',
                'error': 'Groq API key not configured. Please add your API key in Settings.'
            }
        
        if persona not in self.personas:
            return {
                'success': False,
                'message': '',
                'error': f'Invalid persona: {persona}. Available: {list(self.personas.keys())}'
            }
        
        try:
            persona_info = self.personas[persona]
            
            # Construct prompt
            system_prompt = persona_info['system_prompt']
            user_prompt = f"""
            Request: {request}
            
            Additional Context: {context if context else 'No additional context provided'}
            
            Generate a compelling message based on the request above. The message should be:
            - Ready to send (no placeholders)
            - Appropriate for WhatsApp/SMS
            - Maximum 500 characters
            - Engaging and action-oriented
            
            Return only the message text, no explanations or formatting.
            """
            
            # Prepare API request
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'model': self.model,
                'messages': [
                    {'role': 'system', 'content': system_prompt},
                    {'role': 'user', 'content': user_prompt}
                ],
                'max_tokens': 200,
                'temperature': 0.7,
                'top_p': 0.9,
                'stream': False
            }
            
            # Make API request
            response = requests.post(
                self.base_url,
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                message = result['choices'][0]['message']['content'].strip()
                
                # Clean up message
                message = message.replace('"', '').replace("'", "'")
                if message.startswith('"') and message.endswith('"'):
                    message = message[1:-1]
                
                return {
                    'success': True,
                    'message': message,
                    'error': None,
                    'persona': persona_info['name'],
                    'tokens_used': result.get('usage', {}).get('total_tokens', 0)
                }
            else:
                error_msg = f"API Error {response.status_code}: {response.text}"
                return {
                    'success': False,
                    'message': '',
                    'error': error_msg
                }
                
        except requests.exceptions.Timeout:
            return {
                'success': False,
                'message': '',
                'error': 'Request timeout. Please try again.'
            }
        except requests.exceptions.ConnectionError:
            return {
                'success': False,
                'message': '',
                'error': 'Connection error. Please check your internet connection.'
            }
        except Exception as e:
            return {
                'success': False,
                'message': '',
                'error': f'Unexpected error: {str(e)}'
            }
    
    def get_persona_names(self) -> List[str]:
        """Get list of available persona names"""
        return [info['name'] for info in self.personas.values()]
    
    def get_persona_description(self, persona: str) -> str:
        """Get description of a persona"""
        if persona in self.personas:
            return self.personas[persona]['system_prompt']
        return "Unknown persona"