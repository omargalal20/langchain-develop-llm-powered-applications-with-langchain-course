from langgraph.prebuilt import create_react_agent
from loguru import logger

from business.clients.langsmith_client import LangSmithClient
from business.clients.llm_client import LLMClient
from business.tools.tavily import get_research_gate_profile_urls
from config.settings import get_settings

settings = get_settings()


class ResearchGateLookupAgent:
    """
    ResearchGateLookupAgent
    """

    def __init__(
            self,
            llm_client: LLMClient,
            langsmith_client: LangSmithClient,
    ):
        """
        Initialize ResearchGateLookupAgent configuration.
        """

        self.agent_name = "ResearchGateLookupAgent"
        self.llm = llm_client.get_llm()
        self.react_prompt = langsmith_client.get_prompt("hwchase17/react")

    def lookup(self, researcher_name: str) -> str:
        """
        Lookup for ResearchGate profile
        """
        logger.info(f"{self.agent_name} attempting to lookup ResearchGate profile for: {researcher_name}")

        tools_for_agent = [get_research_gate_profile_urls]

        system_message = "You are a precise and efficient assistant for retrieving the correct ResearchGate profile URL based on researcher name."
        query = f"Given the full name {researcher_name} I want you to get it me a link to their ResearchGate profile page. Your answer should contain only a URL"

        agent = create_react_agent(name=self.agent_name, model=self.llm, prompt=system_message, tools=tools_for_agent)

        # for step in langgraph_agent_executor.stream(
        #         {"messages": query},
        #         stream_mode="values",
        # ):
        #     step["messages"][-1].pretty_print()

        result = agent.invoke(
            {"messages": query}
        )

        return result["messages"][-1].content
