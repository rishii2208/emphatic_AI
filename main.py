import json
import sys
import click
from rich.console import Console
from rich.markdown import Markdown
from dotenv import load_dotenv

# Try to import the AI-powered reviewer, fall back to simple reviewer if not available
try:
    from reviewer import EmpathicReviewer as Reviewer
except ImportError:
    print("Using simple reviewer implementation (no AI)")
    from reviewer_simple import SimpleEmpathicReviewer as Reviewer

console = Console()

@click.command()
@click.option('--input-file', '-i', type=click.Path(exists=True), help='JSON file containing code and review comments')
@click.option('--output-file', '-o', type=click.Path(), help='Output file for the markdown report')
@click.option('--simple', is_flag=True, help='Use simple template-based reviewer instead of AI')
def main(input_file, output_file, simple):
    """Transform critical code review comments into empathetic, constructive feedback."""
    load_dotenv()
    
    # Read input from file or stdin
    if input_file:
        with open(input_file, 'r') as f:
            data = json.load(f)
    else:
        data = json.load(sys.stdin)
    
    # Validate input
    if 'code_snippet' not in data or 'review_comments' not in data:
        console.print("[bold red]Error:[/] Input must contain 'code_snippet' and 'review_comments' keys")
        sys.exit(1)
    
    # Process the review
    if simple:
        from reviewer_simple import SimpleEmpathicReviewer
        reviewer = SimpleEmpathicReviewer()
    else:
        try:
            from reviewer import EmpathicReviewer
            reviewer = EmpathicReviewer()
        except Exception as e:
            console.print(f"[bold yellow]Warning:[/] Error initializing AI reviewer: {e}")
            console.print("[bold yellow]Warning:[/] Falling back to simple template-based reviewer")
            from reviewer_simple import SimpleEmpathicReviewer
            reviewer = SimpleEmpathicReviewer()
    
    markdown_report = reviewer.process_review(data['code_snippet'], data['review_comments'])
    
    # Output the report
    if output_file:
        with open(output_file, 'w') as f:
            f.write(markdown_report)
        console.print(f"[bold green]Report saved to {output_file}[/]")
    else:
        console.print(Markdown(markdown_report))

if __name__ == '__main__':
    main()