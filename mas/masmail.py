import os
from dotenv import load_dotenv
from datetime import datetime
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from langchain_community.agent_toolkits import GmailToolkit
from langchain.agents import initialize_agent, AgentType
from crewai import Agent, Task, Crew
import imaplib
import email
from email.header import decode_header

# Load environment variables
load_dotenv()
api_key = os.getenv('OLLAMA_API_KEY')

# Initialize the Groq model
llm = ChatGroq(api_key=api_key, model_name='llama3-70b-8192')
parser = StrOutputParser()

# IMAP email retrieval with date filtering
def fetch_emails_by_date(username, password, date):
    # Connect to the server
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(username, password)
    mail.select("inbox")

    date_str = date.strftime("%d-%b-%Y")
    status, messages = mail.search(None, f'ON {date_str}')
    email_ids = messages[0].split()

    emails = []
    for email_id in email_ids:
        status, msg_data = mail.fetch(email_id, "(RFC822)")
        msg = email.message_from_bytes(msg_data[0][1])
        subject, encoding = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding if encoding else "utf-8")
        from_ = msg.get("From")
        date_ = msg.get("Date")
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                try:
                    body = part.get_payload(decode=True).decode()
                except:
                    pass
                if content_type == "text/plain" and "attachment" not in content_disposition:
                    break
        else:
            body = msg.get_payload(decode=True).decode()

        emails.append((subject, from_, date_, body))

    mail.close()
    mail.logout()

    return emails

# Sentiment Analysis Agent
sentiment_agent = Agent(
    llm=llm,
    role="Sentiment Analyst",
    goal="Analyze the sentiment of the email content.",
    backstory="You analyze the email content to determine the overall sentiment.",
    allow_delegation=False,
    verbose=True
)

# Spam Classification Agent
classification_agent = Agent(
    llm=llm,
    role="Spam Classifier",
    goal="Classify the email as spam or non-spam based on the content and header.",
    backstory="You classify the email based on its content and header analysis.",
    allow_delegation=False,
    verbose=True
)

# Report Generation Agent
report_agent = Agent(
    llm=llm,
    role="Report Generator",
    goal="Generate a comprehensive report based on the classification and sentiment analysis.",
    backstory="You create a detailed report that includes the sentiment analysis and classification results.",
    allow_delegation=False,
    verbose=True
)

# Tasks for each agent
sentiment_task = Task(
    description="Analyze the sentiment of the email content.",
    expected_output="Sentiment analysis result (e.g., Positive, Negative, Neutral).",
    agent=sentiment_agent,
)

classification_task = Task(
    description="Classify the email as spam or non-spam based on content and header analysis.",
    expected_output="Classification result (Spam or Non-Spam).",
    agent=classification_agent,
)

report_task = Task(
    description="Generate a comprehensive report based on the classification and sentiment analysis.",
    expected_output="A detailed report including sentiment and classification results.",
    agent=report_agent
)

# Crew object for multi-agent system
crew = Crew(agents=[sentiment_agent, classification_agent, report_agent],
            tasks=[sentiment_task, classification_task, report_task],
            verbose=True)

# Fetch emails by date
username = "sundharess@gmail.com"
password = "jgobfatrsnrhrfwo"  # Replace with your app password
date_to_fetch = datetime(2024, 7, 4)  # Replace with the desired date

emails = fetch_emails_by_date(username, password, date_to_fetch)
print("Emails received on", date_to_fetch.strftime("%Y-%m-%d"))
for i, (subject, from_, date_, body) in enumerate(emails):
    print(f"{i + 1}. From: {from_} - Subject: {subject}")

# Select an email for processing
selected_email_index = int(input("Select which email to process (enter the number): ")) - 1
if 0 <= selected_email_index < len(emails):
    selected_email = emails[selected_email_index]
    subject, from_, date_, body = selected_email

    # Process the selected email through the multi-agent system
    result = crew.kickoff(inputs={"email_content": body})
    print(result)
else:
    print("Invalid selection")
