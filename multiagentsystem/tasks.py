# Defining tasks for all the agents

from crewai import Task # For defining task
from tools import tool
from agents import researcher,writer

researchtask = Task(
    description = (
        "Identify the next big trend in {topic}."
        "Focus on identifying pros and cons and the overall narrative."
        "Your final report should clearly articulate the key points,"
        "its market opportunities, and potential risks."),
    expected_output = 'A collection of recent news articles, with a summary of each article highlighting the main points and publication dates.',
    tools = [tool],
    agent = researcher # Defining agent
)

writertask = Task(
    description = (
        "Compose an insightful article on {topic}."
        "Focus on the latest trends and how it's impacting the industry."
        "This article should be easy to understand, engaging, and positive."),
    expected_output = 'A polished final draft of the article, free of grammatical errors and inconsistencies, ready for publication.',
    tools = [tool],
    agent = writer, # Defining agent
    async_execution = False,
    output_file = 'article1.md' # Output file as markdown
    
)