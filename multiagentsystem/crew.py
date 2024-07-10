# Developing crew with meshing up agents and tasks

from crewai import Crew,Process
from agents import researcher,writer
from tasks import researchtask,writertask

crew = Crew(
    agents=[researcher,writer],
    tasks=[researchtask,writertask],
    process=Process.sequential, # After the research agent finishes it's work it will collaborate to news writer
)

# Kicking off the crew

outcome = crew.kickoff(inputs={'topic':'Section 498A'})
print(outcome)