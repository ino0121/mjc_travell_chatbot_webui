from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain import hub
from langchain.prompts import PromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate, SystemMessagePromptTemplate
from langchain_openai import ChatOpenAI

class GenerativeChatbot:
    def __init__(self):
        self.llm = ChatOpenAI(temperature = 0, model='gpt-3.5-turbo')
        self.tools = [TavilySearchResults(max_results=3)]
        self.prompt = hub.pull("hwchase17/openai-functions-agent")
        self.prompt.messages = [SystemMessagePromptTemplate(prompt=PromptTemplate(input_variables=[],
                                                        template="""
                                                        당신은 AI 챗봇이며, 사용자는 여행지에 대한 정보를 얻고자 합니다. 당신은 사용자에게 자세하고 정확한 정보를 제공해야 합니다.
                                                        모든 대화는 한국어로 이루어지며, 금액에 관한 정보는 모두 대한민국 원으로 변환하여 제공해야 합니다.
                                                        """)),
                                                        MessagesPlaceholder(variable_name='chat_history', optional=True),
                                                        HumanMessagePromptTemplate(prompt=PromptTemplate(input_variables=['input'], template='{input}')),
                                                        MessagesPlaceholder(variable_name='agent_scratchpad')]
        self.agent = create_openai_functions_agent(self.llm, self.tools, self.prompt)
        self.agent_executor = AgentExecutor(agent=self.agent, tools=self.tools, verbose=False)

    def inform_city(self, city):
        input_message = f"여행지로서 {city}에 대해 개략적으로 설명해 줘."
        return self.agent_executor.invoke({"input": input_message})['output']

    def inform_flight(self, month, city):
        input_message = f"Skyscanner에서 서울에서 출발해 {city}까지 가는 항공편 가격을 찾아 줘."
        return self.agent_executor.invoke({"input": input_message})['output']

    def inform_hotels(self, month, itinerary, city):
        input_message = f"{month}월 기준 {city}에서 {itinerary}일 동안 묵을 숙소 정보를 가격을 반드시 포함해 3개 찾아 줘."
        return self.agent_executor.invoke({"input": input_message})['output']

    def inform_attractions(self, month, city):
        input_message = f"{month}월에 {city}에서 방문하기 좋은 관광지 5곳을 알려줘."
        return self.agent_executor.invoke({"input": input_message})['output']

    def note_inform(self, month, itinerary, city):
        print(self.inform_city(city))
        print(self.inform_flight(month, city))
        print(self.inform_hotels(itinerary, city))
        print(self.inform_attractions(city))