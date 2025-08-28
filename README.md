# Empathetic Code Reviewer

Note: I have deliberately pushed .env file, so that evaluators dont have to waste time in generating .env file and API key. I will delete API keys once evaluation gets completed.Also, the keys are from free account just for evaluation purpose. SO PLEASE DON'T JUDGE ME.

## Overview

This tool takes code review comments that might be perceived as harsh or blunt and transforms them into empathetic, constructive feedback that helps developers learn and grow.

## Features

- Transforms critical code review comments into empathetic feedback
- Explains the reasoning behind each suggestion
- Provides concrete code examples for improvement
- Includes relevant documentation links
- Generates an encouraging summary

## Installation

1. Clone this repository `git clone url`
2. Install dependencies: `pip install -r requirements.txt`
3. I have setted up a sample_input.json file for testing purpose, if you want you can change it accordingly.
4. Run the tool: `python main.py --input-file sample_input.json`

## Working of this Tool

1. Input Processing : The system takes a JSON input containing:

   - A code snippet that needs review
   - A list of critical review comments

2. Language Detection : The system automatically detects the programming language of the code snippet.
3. Feedback Transformation : For each critical comment, the system:

   - Rephrases it in a positive, encouraging way
   - Explains the underlying principle or reason for the suggestion
   - Provides a concrete code example showing how to implement the improvement

4. Summary Generation : The system creates an encouraging summary that acknowledges strengths and frames feedback as growth opportunities.
5. Output : The system produces a well-formatted Markdown report containing all the transformed feedback.

## Technologies Used

1. Python : The core programming language used for the project.
2. Google Generative AI (Gemini) : Used for transforming critical feedback into empathetic suggestions. The system is designed to fall back to a template-based approach if API access is unavailable.
3. Rich : A Python library for rich text and beautiful formatting in the terminal, used to display the Markdown output.
4. Click : A Python package for creating command-line interfaces, used to handle command-line arguments.
5. Markdown : Used for formatting the output report in a readable, structured way.
6. Regular Expressions : Used for language detection and text processing.
7. Environment Variables : Used to securely store API keys.
8. JSON : Used for input/output data formatting.
   The project has a fallback mechanism that uses predefined templates when the AI API is unavailable, ensuring it can still function without external dependencies.

## Execution Flow

1. User provides a JSON input with code and review comments
2. The system processes this input through the main.py script
3. The EmpathicReviewer class transforms each comment
4. A formatted Markdown report is generated

## Why 2 reviewers files?

I have used two reviewer files for different implementation approaches:

1. reviewer.py : This file contains the EmpathicReviewer class that uses the Google Generative AI (Gemini) API to transform code review comments. This is the primary implementation that leverages AI to generate personalized, context-aware responses for each review comment.
2. reviewer_simple.py : This file contains the SimpleEmpathicReviewer class that uses predefined templates instead of AI. It serves as a fallback mechanism when:

- The Gemini API key is not available or invalid
- The user doesn't have access to the required Gemini models
- The user explicitly chooses to use the simple implementation with the --simple flag
