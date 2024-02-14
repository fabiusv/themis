import openai
from dotenv import load_dotenv
import os

load_dotenv()
print("key: \n \n \n \n")
print(os.getenv("openai_api_key"))
api_key = os.getenv("openai_api_key")

client = openai.OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=api_key
)


assistant = client.beta.assistants.create(
    name="Math Tutor",
    instructions="You are a personal math tutor. Write and run code to answer math questions.",
    tools=[{"type": "code_interpreter"}],
    model="gpt-4-1106-preview"
)

thread = client.beta.threads.create()

message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="I need to solve the equation `3x + 11 = 14`. Can you help me?"
)

run = client.beta.threads.runs.create(
  thread_id=thread.id,
  assistant_id=assistant.id,
  instructions="Please address the user as Jane Doe. The user has a premium account."
)
print(type(run.status))

while run.status != "completed":
    run = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
    )
    

messages = client.beta.threads.messages.list(thread_id=thread.id)
print(messages)





import os

os.environ["GOOGLE_CSE_ID"] = "c4415157c33794318"
os.environ["GOOGLE_API_KEY"] = os.getenv("gcloud_api_key")

from langchain.tools import Tool
from langchain_community.utilities import GoogleSearchAPIWrapper

search = GoogleSearchAPIWrapper()

tool = Tool(
    name="Google Search",
    description="Search Google for recent results.",
    func=search.run,
)

print(tool.run("Obama's first name?"))