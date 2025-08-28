import os
import json
from typing import List, Dict, Any
import re

class SimpleEmpathicReviewer:
    def __init__(self):
        # Define language-specific resources
        self.resources = {
            "python": {
                "style_guide": "https://peps.python.org/pep-0008/",
                "performance": "https://wiki.python.org/moin/TimeComplexity",
                "best_practices": "https://docs.python-guide.org/"
            },
            # Add more languages as needed
        }
        
        # Define templates for common code review comments
        self.templates = {
            "inefficient": {
                "rephrasing": "I see an opportunity to make this code more efficient!",
                "why": "Efficient code runs faster, uses less memory, and is often more readable.",
                "improvement": "Consider using list comprehensions or built-in functions that are optimized for performance."
            },
            "naming": {
                "rephrasing": "Using descriptive variable names can make your code even clearer!",
                "why": "Good variable names make code self-documenting and easier to understand for others (and your future self).",
                "improvement": "Try to use names that describe what the variable represents or its purpose."
            },
            "redundant": {
                "rephrasing": "There's a chance to make this code more concise!",
                "why": "Removing redundant code makes your program cleaner and easier to maintain.",
                "improvement": "In Python, certain patterns can be simplified for better readability."
            }
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
        # Determine which template to use based on keywords in the comment
        template_key = "redundant"  # default
        
        if any(word in comment.lower() for word in ["inefficient", "slow", "performance", "loop"]):
            template_key = "inefficient"
        elif any(word in comment.lower() for word in ["name", "variable", "identifier"]):
            template_key = "naming"
        elif any(word in comment.lower() for word in ["redundant", "unnecessary", "duplicate"]):
            template_key = "redundant"
        
        template = self.templates[template_key]
        
        # Generate specific improvements based on the comment and code
        specific_improvement = self._generate_specific_improvement(code_snippet, comment, language, template_key)
        
        # Format the response
        response = f"""
### Analysis of Comment: "{comment}"

* **Positive Rephrasing:** {template["rephrasing"]}

* **The 'Why':** {template["why"]}

* **Suggested Improvement:** {specific_improvement}
"""
        
        return response
    
    def _generate_specific_improvement(self, code_snippet: str, comment: str, language: str, template_key: str) -> str:
        """Generate specific improvement suggestions based on the comment and code."""
        if language == "python":
            if template_key == "inefficient" and "loop" in comment.lower():
                return """```python
# Instead of:
results = []
for u in users:
    if u.is_active and u.profile_complete:
        results.append(u)
return results

# Consider using a list comprehension:
return [user for user in users if user.is_active and user.profile_complete]
```"""
            elif template_key == "naming" and "u" in comment.lower():
                return """```python
# Instead of:
for u in users:
    if u.is_active and u.profile_complete:
        results.append(u)

# Use a more descriptive name:
for user in users:
    if user.is_active and user.profile_complete:
        results.append(user)
```"""
            elif template_key == "redundant" and "== True" in comment:
                return """```python
# Instead of:
if u.is_active == True and u.profile_complete == True:
    results.append(u)

# Boolean variables don't need comparison with True:
if u.is_active and u.profile_complete:
    results.append(u)
```"""
        
        # Default improvement suggestion
        return f"""```{language}
# Consider reviewing the code based on the principles mentioned above
# and applying best practices from {self.resources.get(language, {}).get('best_practices', 'relevant documentation')}
```"""
    
    def _generate_summary(self, code_snippet: str, review_comments: List[str], language: str) -> str:
        """Generate an encouraging summary of the overall feedback."""
        return """Your code has a solid foundation! The suggestions above are opportunities to make your code even more elegant and maintainable. Remember that code review is a collaborative process aimed at continuous improvement. Keep up the great work, and these small refinements will help you develop even stronger coding practices!"""