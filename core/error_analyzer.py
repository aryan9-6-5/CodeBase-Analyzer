import re
import ast
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class ErrorContext:
    error_type: str
    line_number: Optional[int]
    file_name: str
    function_name: Optional[str]
    error_message: str
    pattern: str

class ErrorAnalyzer:
    def __init__(self):
        self.error_patterns = self._load_error_patterns()
    
    def _load_error_patterns(self) -> Dict:
        """Load common error patterns and their explanations"""
        return {
            'IndexError': {
                'pattern': r'list index out of range|string index out of range',
                'common_cause': 'Trying to access an element that doesn\'t exist',
                'typical_fix': 'Check list length before accessing'
            },
            'KeyError': {
                'pattern': r"KeyError: '([^']*)'",
                'common_cause': 'Dictionary key doesn\'t exist',
                'typical_fix': 'Use .get() method or check if key exists'
            },
            'AttributeError': {
                'pattern': r"'([^']*)' object has no attribute '([^']*)'",
                'common_cause': 'Method or attribute doesn\'t exist on object',
                'typical_fix': 'Check object type and available methods'
            },
            'TypeError': {
                'pattern': r'unsupported operand type|can\'t multiply sequence|unhashable type',
                'common_cause': 'Wrong data type for operation',
                'typical_fix': 'Convert to correct type or check data type'
            },
            'NameError': {
                'pattern': r"name '([^']*)' is not defined",
                'common_cause': 'Variable used before being defined',
                'typical_fix': 'Define variable before use or check spelling'
            }
        }
    
    def parse_traceback(self, traceback: str) -> ErrorContext:
        """Parse Python traceback to extract error information"""
        lines = traceback.strip().split('\n')
        
        # Extract error type and message (last line)
        error_line = lines[-1]
        error_parts = error_line.split(':', 1)
        error_type = error_parts[0].strip()
        error_message = error_parts[1].strip() if len(error_parts) > 1 else ""
        
        # Extract file and line info
        file_line_pattern = r'File "([^"]*)", line (\d+)'
        file_name = "unknown"
        line_number = None
        function_name = None
        
        for line in lines:
            match = re.search(file_line_pattern, line)
            if match:
                file_name = match.group(1)
                line_number = int(match.group(2))
            
            # Extract function name
            if 'in ' in line and not line.strip().startswith('File'):
                func_match = re.search(r'in (\w+)', line)
                if func_match:
                    function_name = func_match.group(1)
        
        # Determine error pattern
        pattern = "unknown"
        for err_type, info in self.error_patterns.items():
            if err_type == error_type:
                pattern = err_type.lower()
                break
        
        return ErrorContext(
            error_type=error_type,
            line_number=line_number,
            file_name=file_name,
            function_name=function_name,
            error_message=error_message,
            pattern=pattern
        )
    
    def analyze_error(self, code: str, traceback: str, llm_client) -> Dict:
        """Main analysis function"""
        # Parse the error
        context = self.parse_traceback(traceback)
        
        # Get context about the error
        context_dict = {
            'error_type': context.error_type,
            'line_number': context.line_number,
            'pattern': context.pattern
        }
        
        # Generate AI analysis
        raw_response = llm_client.debug_analysis(code, traceback, context_dict)
        print("DEBUG LLM RAW RESPONSE:\n", raw_response)
        
        # Parse the response into structured format
        parsed_response = self._parse_llm_response(raw_response)
        
        return parsed_response
    
    def _parse_llm_response(self, response: str) -> Dict:
        """Parse LLM response into structured format"""
        sections = {
            'root_cause': '',
            'suggested_fix': '',
            'explanation': '',
            'prevention_tips': ''
        }
        
        current_section = None
        lines = response.split('\n')
        
        for line in lines:
            line = line.strip()
            if 'ROOT_CAUSE' in line.upper():
                current_section = 'root_cause'
            elif 'SUGGESTED_FIX' in line.upper() or 'FIX' in line.upper():
                current_section = 'suggested_fix'
            elif 'EXPLANATION' in line.upper():
                current_section = 'explanation'
            elif 'PREVENTION' in line.upper() or 'TIPS' in line.upper():
                current_section = 'prevention_tips'
            elif current_section and line and not line.startswith('#'):
                sections[current_section] += line + '\n'
        
        # Clean up the sections
        for key in sections:
            sections[key] = sections[key].strip()
        
        return sections
