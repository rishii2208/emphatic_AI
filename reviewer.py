import os
import json
from typing import List, Dict, Any
import markdown
import re
import google.generativeai as genai
from google.api_core.exceptions import InvalidArgument

class EmpathicReviewer:
    def __init__(self):
        
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY issue")
        
        try:
            genai.configure(api_key=api_key)
            # Use gemini-1.0-pro-latest instead of gemini-pro
            self.model = genai.GenerativeModel('gemini-1.0-pro-latest')
        except Exception as e:
            print(f"Error initializing Gemini: {e}")
            print("Falling back to text-bison model...")
            try:
                # Try with text-bison model as fallback
                self.model = genai.GenerativeModel('text-bison')
            except Exception as e2:
                print(f"Error with fallback model: {e2}")
                raise ValueError("Could not initialize any Gemini model. Please check your API key and permissions.")
        
        # Define language-specific resources
        self.resources = {
            "python": {
                "style_guide": "https://peps.python.org/pep-0008/",
                "performance": "https://wiki.python.org/moin/TimeComplexity",
                "best_practices": "https://docs.python-guide.org/"
            },
            # Add more languages as needed
        }
    
    def detect_language(self, code_snippet: str) -> str:
        """Detect the programming language of the code snippet."""
        # Simple detection based on syntax
        if re.search(r'def\s+\w+\s*\(', code_snippet):
            return "python"
        elif re.search(r'function\s+\w+\s*\(', code_snippet):
            return "javascript"
        elif re.search(r'(public|private)\s+(static\s+)?\w+\s+\w+\s*\(', code_snippet):
            return "java"
        else:
            return "unknown"
    
    def process_review(self, code_snippet: str, review_comments: List[str]) -> str:
        """Process the code review and generate an empathetic report."""
        language = self.detect_language(code_snippet)
        
        # Generate individual responses for each comment
        sections = []
        for comment in review_comments:
            response = self._generate_empathetic_response(code_snippet, comment, language)
            sections.append(response)
        
        # Create a summary
        summary = self._generate_summary(code_snippet, review_comments, language)
        
        # Combine everything into a markdown report
        markdown_report = "# Empathetic Code Review Report\n\n"
        markdown_report += "## Code Snippet\n\n```{}\n{}\n```\n\n".format(language, code_snippet)
        markdown_report += "## Feedback Analysis\n\n"
        markdown_report += "\n\n".join(sections)
        markdown_report += "\n\n## Summary\n\n" + summary
        
        return markdown_report
    
    def _generate_empathetic_response(self, code_snippet: str, comment: str, language: str) -> str:
        """Generate an empathetic response for a single review comment."""
        prompt = f"""
        You are an empathetic senior developer providing code review feedback. 
        
        Code snippet:
        ```{language}
        {code_snippet}
        ```
        
        Original review comment: "{comment}"
        
        Please provide:
        1. A positive rephrasing of the comment that is encouraging and constructive
        2. An explanation of why this change is important (the underlying principle)
        3. A specific code example showing how to improve the code
        
        Format your response in Markdown with these three sections clearly labeled.
        Include relevant links to documentation or best practices if applicable.
        """
        
        response = self.model.generate_content(prompt)
        
        return f"### Analysis of Comment: \"{comment}\"\n\n{response.text}"
    
    def _generate_summary(self, code_snippet: str, review_comments: List[str], language: str) -> str:
        """Generate an encouraging summary of the overall feedback."""
        prompt = f"""
        You are an empathetic senior developer providing a summary of code review feedback.
        
        Code snippet:
        ```{language}
        {code_snippet}
        ```
        
        Review comments:
        {json.dumps(review_comments)}
        
        Please provide an encouraging summary paragraph that:
        1. Acknowledges the strengths in the code
        2. Frames the feedback as an opportunity for growth
        3. Ends on a positive, motivating note
        
        Keep your response concise (3-5 sentences) and encouraging.
        """
        
        response = self.model.generate_content(prompt)
        
        return response.text