from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.knowledge.pdf_url import PDFUrlKnowledgeBase
from agno.knowledge.pdf import PDFKnowledgeBase
from agno.vectordb.pgvector import PgVector, SearchType
from agno.models.google import Gemini
from agno.embedder.google import GeminiEmbedder
from utils.key_manager import ApiKeyManager

# Initialize the API key manager
key_manager = ApiKeyManager(required_keys=["GEMINI_API_KEY"])
GEMINI_API_KEY = key_manager.get("GEMINI_API_KEY")


db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"
knowledge_base = PDFKnowledgeBase(
    #urls=["https://agno-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf"],
    path="Assessment_and_classification_of_burn_injury.pdf",
    vector_db=PgVector(
        table_name="burns_knowledge", 
        db_url=db_url, 
        search_type=SearchType.hybrid,
        embedder=GeminiEmbedder(api_key=GEMINI_API_KEY),
        ),
)
# Load the knowledge base: Comment out after first run
#knowledge_base.load(recreate=True, upsert=True)

agent = Agent(
    model=Gemini(
        id="gemini-2.5-pro-exp-03-25",
        api_key=GEMINI_API_KEY,
        temperature=0,
    ),
    knowledge=knowledge_base,
    # Add a tool to read chat history.
    read_chat_history=True,
    show_tool_calls=True,
    markdown=True,
    # debug_mode=True,
)
agent.print_response("Elaborate a list in bullet points on how I should classify the anatomical locations of burns. Is there a standard? Provide full scientific references, in a formatted table.", stream=True)
agent.print_response("What was my last question?", stream=True)