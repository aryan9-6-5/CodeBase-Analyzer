import google.generativeai as genai
import os
from typing import List, Dict
from dotenv import load_dotenv
load_dotenv()
class GeminiClient:
    def __init__(self):
        genai.configure(api_key=os.environ.get('GOOGLE_API_KEY'))
        self.model = genai.GenerativeModel('models/gemini-2.0-flash')
    
    def generate_response(self, prompt: str, max_tokens: int = 1000) -> str:
        """Generate response using Gemini Pro"""
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=max_tokens,
                    temperature=0.2,
                )
            )
            return response.text
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def debug_analysis(self, code: str, error: str, context: Dict) -> str:
        """Generate debugging analysis"""
        prompt = f"""
        You are an expert Python debugging assistant. Analyze this error and provide educational explanations.
        
        CODE:
        ```python
        {code}
        ```
        
        ERROR:
        ```
        {error}
        ```
        
        CONTEXT:
        Error Type: {context.get('error_type', 'Unknown')}
        Line Number: {context.get('line_number', 'Unknown')}
        Error Pattern: {context.get('pattern', 'Unknown')}
        
        Please provide:
        1. ROOT_CAUSE: What exactly went wrong (1-2 sentences)
        2. SUGGESTED_FIX: Corrected code snippet
        3. EXPLANATION: Why this error happens (educational, 2-3 sentences)
        4. PREVENTION_TIPS: How to avoid this in the future (1-2 practical tips)
        
        Format your response with clear headers for each section.
        Be educational and encouraging - this is for learning.
        """
        
        return self.generate_response(prompt)