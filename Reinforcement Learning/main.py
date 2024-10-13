# Reinforcement Learning CIA 1

# Scenario - A company is using four different advertising strategies across various online platforms. Each strategy has an unknown probability of success (click-through rate), and the company wants to maximize the total number of clicks over time. You have access to real-time feedback, showing how many clicks each strategy generates. The cumulative rewards for each strategy are tracked and updated after every campaign.

# At any given point, you must decide which strategy to use next, knowing that some strategies have performed better than others, but there is still uncertainty about their true potential.Based on the scenario described, choose any multi-armed bandit algorithm you have studied (such as Upper Confidence Bound (UCB1), ε-greedy, or Thompson Sampling) to optimize the company's advertising strategies over time. Explain how your chosen algorithm balances exploration and exploitation, and write a Python function to implement it. Describe how you would decide which strategy to choose at the next time point based on the data provided in the scenario.

# Using Thompson Sampling Algorithm plus Agentic Approach to optimize the Advertising Strategies

# LLM's are utilized for efficient data retrieval but here mock data is utilized

# Loading necessary libraries

from crewai import Agent, Task, Crew
from langchain_groq import ChatGroq
import numpy as np
from scipy.stats import beta
import asyncio
import os
import random

os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')

class AdStrategy:
    def __init__(self, name):
        self.name = name
        self.successes = 0
        self.failures = 0
        self.impressions = 0
        self.clicks = 0

    async def update(self):
        # API calls
        new_impressions = random.randint(100, 1000)
        new_clicks = random.randint(0, new_impressions)
        
        self.successes += new_clicks
        self.failures += (new_impressions - new_clicks)
        self.impressions += new_impressions
        self.clicks += new_clicks

    def sample(self):
        return beta.rvs(self.successes + 1, self.failures + 1)

    @property
    def ctr(self):
        return self.clicks / self.impressions if self.impressions > 0 else 0

class RealTimeAdvertisingEnvironment:
    def __init__(self, strategies):
        self.strategies = {s.name: s for s in strategies}

    async def update_all(self):
        await asyncio.gather(*(strategy.update() for strategy in self.strategies.values()))

# Developing Agents

data_analyst = Agent(
    name="Data Analyst",
    role="Analyzes real-time performance data of advertising strategies",
    goal="Provide accurate analysis of each strategy's performance",
    backstory="Expert in data analysis with focus on advertising metrics",
    llm=ChatGroq(model='llama3-70b-8192',temperature=0.7)
)

strategy_selector = Agent(
    name="Strategy Selector",
    role="Selects the best advertising strategy based on current data",
    goal="Maximize overall click-through rate",
    backstory="Experienced in decision making for advertising campaigns",
    llm=ChatGroq(model='llama3-70b-8192',temperature=0.7)
)

feedback_processor = Agent(
    name="Feedback Processor",
    role="Processes real-time feedback from advertising platforms",
    goal="Accurately update strategy performance based on feedback",
    backstory="Specialist in real-time data processing and updates",
    llm=ChatGroq(model='llama3-70b-8192',temperature=0.7)
)

report_generator = Agent(
    name="Report Generator",
    role="Compiles all analysis and decisions into a comprehensive markdown report",
    goal="Create a clear, informative report on the ad optimization process",
    backstory="Experienced technical writer with expertise in reporting",
    llm=ChatGroq(model='llama3-70b-8192',temperature=0.7)
)

# Developing Tasks

analyze_data = Task(
    description="Analyze the current real-time performance data of all advertising strategies",
    expected_output="A detailed analysis of each strategy's performance, including CTR, total impressions, and clicks.",
    agent=data_analyst
)

select_strategy = Task(
    description="Select the best strategy for the next campaign using Thompson Sampling",
    expected_output="The name of the selected strategy and a brief explanation of why it was chosen.",
    agent=strategy_selector
)

process_feedback = Task(
    description="Process the real-time feedback from all campaigns and update strategy data",
    expected_output="A summary of the updates made to each strategy based on the latest feedback.",
    agent=feedback_processor
)

generate_report = Task(
    description="Compile all the analysis, decisions, and feedback into a comprehensive markdown report on the ad optimization process.",
    expected_output="A complete markdown-formatted report detailing the entire optimization process, including data analysis, strategy selections, and performance trends.",
    agent=report_generator,
    output_file = 'report.md'
)

advertising_crew = Crew(
    agents=[data_analyst, strategy_selector, feedback_processor, report_generator],
    tasks=[analyze_data, select_strategy, process_feedback, generate_report],
    verbose=True
)

# Main function 

async def run_realtime_advertising_optimization(duration_seconds=3600):
    strategies = [AdStrategy(f"Strategy_{i}") for i in range(4)]
    env = RealTimeAdvertisingEnvironment(strategies)
    
    start_time = asyncio.get_event_loop().time()
    while asyncio.get_event_loop().time() - start_time < duration_seconds:
        # Updating all strategies with mock real-time data
        await env.update_all()
        
        result = advertising_crew.kickoff()
        
        selected_strategy = result['select_strategy']
        
        print(f"Selected strategy: {selected_strategy}")
        
        feedback_processor.execute_task(f"Process real-time feedback for all strategies")

        await asyncio.sleep(60)  
        
    final_analysis = data_analyst.execute_task("Provide a final analysis of all strategies' performance based on real-time data")
    return final_analysis

asyncio.run(run_realtime_advertising_optimization())
