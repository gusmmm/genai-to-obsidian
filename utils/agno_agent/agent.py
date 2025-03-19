from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.pubmed import PubmedTools
from agno.tools.duckduckgo import DuckDuckGoTools
from utils.key_manager import ApiKeyManager

# Initialize the API key manager
key_manager = ApiKeyManager(required_keys=["GEMINI_API_KEY"])
GEMINI_API_KEY = key_manager.get("GEMINI_API_KEY")

# Using Google AI Studio
pubmed_agent = Agent(
    model=Gemini(
        id="gemini-2.0-pro-exp-02-05",
        api_key=GEMINI_API_KEY
        ),
    markdown=True,
    tools=[PubmedTools(max_results=4)],
    description="" \
        "You are an agent that can search PubMed and answer questions.\
                Use the query to search PubMed. Using the summary of the returned papers to answer the query. \
                Use simple and direct language. Give concrete values to answer the question,if possible.\
                Provide a list of the most relevant articles and their findings related to the query.\
                Write in JSON format the full list of results with keys 'Published','Title','First_author', 'DOI' and 'Summary'.\
                ", 
    show_tool_calls=True
)

#agent.print_response("Share a 2 sentence horror story.")
#pubmed_agent.print_response("Is there any correlation between parasitemia levels in malaria patients and the mortality?",stream=True)

ddg_agent = Agent(
    model=Gemini(
        id="gemini-2.0-pro-exp-02-05",
        api_key=GEMINI_API_KEY
        ),
    markdown=True,
    tools=[DuckDuckGoTools(fixed_max_results=10)],
    description="" \
        "You are an agent that can search DuckDuckGo and answer questions.\
                Use the query to search DuckDuckGo.\
                Use simple and direct language. Give concrete values to answer the question,if possible.\
                Always include sources.\
                Provide the author, year and title if it is a scientific paper.\
                ",
    show_tool_calls=True
)
#agent.print_response("Share a 2 sentence horror story.")
#ddg_agent.print_response("Is there any correlation between parasitemia levels in malaria patients and the mortality?",stream=True)

agent_team = Agent(
    team=[pubmed_agent, ddg_agent],
    model=Gemini(
        id="gemini-2.0-pro-exp-02-05",
        api_key=GEMINI_API_KEY
        ),
    tools=[PubmedTools(max_results=10), DuckDuckGoTools(fixed_max_results=10)],
    instructions=["Always include sources", "Use tables to display data"],
    show_tool_calls=True,
    markdown=True,
)

agent_team.print_response("Are there any new treatments and or vaccine for malaria? What is the scientific evidence for their use?",stream=True)
# agent_team.print_response("What is the best way to treat a cold?",stream=True)