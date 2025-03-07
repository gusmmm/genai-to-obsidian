import os
import time
import re
from pathlib import Path
import yaml
from rich.console import Console
from rich.panel import Panel

# Initialize Rich console
console = Console()

class ObsidianNote:
    """Class to represent and manipulate Obsidian notes"""
    def __init__(self, title, content, tags=None, metadata=None):
        self.title = title
        self.content = content
        self.tags = tags or []
        self.metadata = metadata or {}
        self.creation_date = time.strftime("%Y-%m-%d")
        
    def to_markdown(self):
        """Convert the note to markdown format with YAML frontmatter"""
        # Prepare frontmatter
        frontmatter = {
            "title": self.title,
            "date": self.creation_date,
            "tags": self.tags
        }
        
        # Add additional metadata
        frontmatter.update(self.metadata)
        
        # Convert frontmatter to YAML
        yaml_str = yaml.dump(frontmatter, default_flow_style=False)
        
        # Combine frontmatter and content
        return f"---\n{yaml_str}---\n\n{self.content}"

def get_obsidian_vault_path():
    """Get the path to the Obsidian vault from configuration or environment"""
    # Try environment variable first
    vault_path = os.getenv("OBSIDIAN_VAULT_PATH")
    
    # If not found, try common locations
    if not vault_path:
        home = Path.home()
        common_paths = [
            home / "Obsidian",
            home / "Documents" / "Obsidian",
            home / "Documents" / "obsidian"
        ]
        
        for path in common_paths:
            if path.exists():
                vault_path = str(path)
                break
    
    # If still not found, ask user
    if not vault_path:
        console.print("[yellow]Obsidian vault path not found.[/yellow]")
        vault_path = console.input("[bold cyan]Enter your Obsidian vault path: [/bold cyan]")
    
    # Verify path exists
    if not os.path.exists(vault_path):
        console.print(f"[bold red]Warning:[/bold red] Path {vault_path} does not exist.")
        if console.input("[bold cyan]Create directory? (y/n): [/bold cyan]").lower() == 'y':
            os.makedirs(vault_path)
        else:
            return None
    
    return vault_path

def sanitize_filename(name):
    """Convert a string to a valid filename"""
    # Remove invalid characters
    name = re.sub(r'[^\w\s-]', '', name)
    # Replace spaces with hyphens
    name = re.sub(r'\s+', '-', name)
    # Limit length
    return name[:50]

def extract_key_concepts(client, response_text, query=None, model=None, max_concepts=10):
    """Extract meaningful key concepts for linking in Obsidian using AI
    
    Args:
        client: The GenAI client
        response_text: The text to analyze for key concepts
        query: Optional original query for context
        model: Model to use (defaults to same as main query)
        max_concepts: Number of concepts to extract (default 10)
        
    Returns:
        list: Key concepts suitable for Obsidian linking
    """
    # Prepare prompt for concept extraction
    concept_prompt = f"""
    Analyze the following text and extract the {max_concepts} most significant concepts or terms.
    
    Focus on multi-word expressions, technical terms, theoretical frameworks, and meaningful phrases 
    rather than common single words. Good examples would be "extraterrestrial life", "carbon-based life forms", 
    "metabolic processes", or "self-replicating systems".
    
    Text to analyze:
    ```
    {response_text[:2000]}  # Limit to first 2000 chars to avoid token limits
    ```
    
    Return ONLY a numbered list with each concept on its own line, no explanations.
    Do not use bullet points or any other formatting, just the concepts themselves.
    Important: Make sure concepts are in a form useful for knowledge graph linking (proper nouns, technical terms, key phrases).
    """
    
    with console.status("[bold cyan]Extracting key concepts...", spinner="dots"):
        try:
            concept_response = client.models.generate_content(
                model=model,  # Use same model as main query if provided
                contents=concept_prompt,
                config={"temperature": 0.2}  # Low temperature for focused results
            )
            
            # Parse the response - first split by lines
            concept_lines = concept_response.text.strip().split('\n')
            
            # Clean up concepts - remove numbers, whitespace, etc.
            concepts = []
            for line in concept_lines:
                # Remove leading numbers, periods, and whitespace
                clean_line = re.sub(r'^\d+[\.\)]*\s*', '', line).strip()
                if clean_line and len(clean_line) > 2:  # Ensure non-empty and substantial
                    concepts.append(clean_line)
            
            # Limit to requested number
            return concepts[:max_concepts]
            
        except Exception as e:
            console.print(f"[bold red]Error extracting concepts:[/bold red] {str(e)}")
            # Fallback to simple frequency-based extraction
            return _extract_concepts_fallback(response_text, max_concepts)

def _extract_concepts_fallback(text, max_concepts=10):
    """Fallback method using simple text analysis if AI extraction fails"""
    import re
    from collections import Counter
    
    # Try to extract multi-word phrases (simple approach)
    text = text.lower()
    
    # Look for potential 2-3 word phrases
    words = re.findall(r'\b[\w-]+\b', text)
    bigrams = [f"{words[i]} {words[i+1]}" for i in range(len(words)-1)]
    trigrams = [f"{words[i]} {words[i+1]} {words[i+2]}" for i in range(len(words)-2)]
    
    # Count frequencies
    phrase_counter = Counter(bigrams + trigrams)
    
    # Filter out common phrases
    common_phrases = {"of the", "in the", "to the", "and the", "for the", "is a", "such as"}
    filtered_phrases = [phrase for phrase, count in phrase_counter.most_common(max_concepts*3) 
                       if phrase not in common_phrases and len(phrase) > 5]
    
    return filtered_phrases[:max_concepts]

def generate_follow_up_questions(client, response_text, query, model):
    """Generate follow-up questions based on the response"""
    # Using the same Gemini model to generate questions
    follow_up_prompt = f"""
    Based on the following query and response, generate 3 thoughtful follow-up questions 
    that would deepen understanding or explore related topics.
    
    Original query: {query}
    
    Response: {response_text}
    
    Return ONLY the questions as a numbered list.
    """
    
    with console.status("[bold cyan]Generating follow-up questions...", spinner="dots"):
        questions_response = client.models.generate_content(
            model=model,
            contents=follow_up_prompt,
            config={"temperature": 0.7}
        )
    
    return questions_response.text

def create_obsidian_note(response_text, query, model, temperature, 
                        key_concepts=None, follow_up_questions=None):
    """Create an Obsidian note structure from the response"""
    
    # Generate title from query
    title = query[:50] + "..."
    
    # Create content with sections
    content = f"# {title}\n\n"
    content += f"## Query\n\n{query}\n\n"
    content += f"## Response\n\n{response_text}\n\n"
    
    # Add follow-up questions if available
    if follow_up_questions:
        content += f"## Follow-up Questions\n\n{follow_up_questions}\n\n"
    
    # Add key concepts and suggestions for connections
    if key_concepts:
        content += "## Possible Connections\n\n"
        for concept in key_concepts:
            content += f"- [[{concept}]]\n"
        content += "\n"
    
    # Add notes and annotations section
    content += "## Notes and Annotations\n\n- \n\n"
    
    # Create metadata
    metadata = {
        "query": query,
        "model": model,
        "temperature": temperature,
        "date_generated": time.strftime("%Y-%m-%d"),
        "category": "AI-Generated"
    }
    
    # Generate tags
    tags = ["AI-Generated", "Gemini", "Research"]
    
    return ObsidianNote(title, content, tags, metadata)

def export_to_obsidian(response_text, query, model, temperature, 
                       follow_up_questions=None, key_concepts=None,
                       folder="AI-Generated", client=None):
    """Export response to an Obsidian-friendly markdown file"""
    
    # Get vault path
    vault_path = get_obsidian_vault_path()
    if not vault_path:
        console.print("[bold red]Failed to determine Obsidian vault path[/bold red]")
        return None
    
    # Create target folder if it doesn't exist
    target_dir = os.path.join(vault_path, folder)
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    
    # Generate timestamp
    timestamp = time.strftime("%Y-%m-%d-%H%M%S")
    
    # Create filename based on query (truncated)
    safe_query = sanitize_filename(query[:30])
    filename = f"{timestamp}-{safe_query}.md"
    filepath = os.path.join(target_dir, filename)
    
    # Extract key concepts if not provided
    if key_concepts is None and client is not None:
        key_concepts = extract_key_concepts(client, response_text, query, model)
    elif key_concepts is None:
        key_concepts = _extract_concepts_fallback(response_text)
    
    # Create note structure
    note = create_obsidian_note(
        response_text, 
        query, 
        model, 
        temperature,
        key_concepts, 
        follow_up_questions
    )
    
    # Write to file
    try:
        with open(filepath, "w") as f:
            f.write(note.to_markdown())
        console.print(Panel(
            f"[green]Exported successfully to:[/green]\n{filepath}",
            title="[bold green]Obsidian Export[/bold green]",
            border_style="green"
        ))
        return filepath
    except Exception as e:
        console.print(f"[bold red]Error exporting to Obsidian:[/bold red] {str(e)}")
        return None

def display_concepts(concepts):
    """Display extracted concepts in a panel"""
    if not concepts:
        return
    
    concepts_text = "\n".join([f"- [[{concept}]]" for concept in concepts])
    console.print(Panel(
        concepts_text,
        title="[bold yellow]Suggested Connections[/bold yellow]",
        border_style="yellow"
    ))

def display_follow_up(follow_up_text):
    """Display follow-up questions in a panel"""
    console.print(Panel(
        follow_up_text,
        title="[bold magenta]Follow-up Questions[/bold magenta]",
        border_style="magenta"
    ))