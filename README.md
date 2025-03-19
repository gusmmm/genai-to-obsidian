# Gemini to Obsidian
A powerful tool to interact with Google's Gemini AI and automatically export responses to your Obsidian vault as structured markdown notes with knowledge graph integration.

# Features
🤖 Query Google Gemini AI models directly from the command line
📝 Export AI-generated content to your Obsidian vault with proper formatting
🔗 Automatically extract key concepts and create knowledge graph links
❓ Generate thoughtful follow-up questions related to your query
📊 View detailed information about token usage and response metrics
🎨 Beautiful terminal interface with rich formatting

# Installation
## Prerequisites
- Python 3.12 or later
- An Obsidian vault
- Google Gemini API key

# Setup

1. Clone the repository:
git clone https://github.com/yourusername/genai-to-obsidian.git
cd genai-to-obsidian
2. Set up a virtual environment and install dependencies:
### Using uv (recommended)
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .

### Alternatively using pip
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e .

3. Create a .env file with your Gemini API key:
echo "GEMINI_API_KEY=your_api_key_here" > .env

4. (Optional) Set your Obsidian vault path:
echo "OBSIDIAN_VAULT_PATH=/path/to/your/obsidian/vault" >> .env

# Usage
Run the application:
python main.py

The default behavior will:
- Connect to the Gemini API
- Send a pre-configured query
- Display the response with rich formatting
- Extract key concepts for knowledge graph linking
- Generate follow-up questions
- Prompt to export results to your Obsidian vault

## Customizing Queries
To modify the query or model parameters, edit the main.py file:

model = 'gemini-2.0-flash-thinking-exp-01-21'  # Choose your preferred model
query = "Your question here"  # Replace with your own query
temperature = 0.2  # Adjust temperature as needed (0.0-1.0)

# Obsidian Integration
The tool will:

- Create a folder named "AI-Generated" in your Obsidian vault (configurable)
- Export responses as markdown files with YAML frontmatter
- Include automatically extracted key concepts as wiki-links
- Add metadata like model used, temperature setting, and generation date

If your Obsidian vault path isn't specified in the .env file, the tool will:
- Check common locations
- Ask for the path if not found
- Offer to create the directory if it doesn't exist

# Project Structure
genai-to-obsidian/
├── main.py              # Main entry point
├── utils/
│   ├── api.py           # Google GenAI API handling
│   ├── display.py       # Terminal UI components
│   └── obsidian.py      # Obsidian export functionality
├── pyproject.toml       # Project configuration
├── requirements.txt     # Dependencies
└── README.md            # Project documentation

# License
This project is licensed under the MIT License - see the LICENSE file for details.

# Contributing
Contributions are welcome! Please feel free to submit a Pull Request.
