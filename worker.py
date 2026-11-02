"""Start the Temporal worker for the CI triage agent."""
import asyncio
import os

from dotenv import load_dotenv

load_dotenv()

from temporalio.client import Client
from temporalio.contrib.google_adk_agents import GoogleAdkPlugin
from temporalio.worker import Worker

from github_tools import GITHUB_ACTIVITIES
from memory import recall, remember
from workflow import MODEL_ALIAS, TriageWorkflow

TASK_QUEUE = "ci-triage"


async def main():
    client = await Client.connect(os.environ.get("TEMPORAL_ADDRESS", "localhost:7233"),
                                  plugins=[GoogleAdkPlugin()])
    print(f"worker running on {TASK_QUEUE} with model {MODEL_ALIAS}")
    await Worker(client, task_queue=TASK_QUEUE, workflows=[TriageWorkflow],
                 activities=[recall, remember, *GITHUB_ACTIVITIES]).run()


if __name__ == "__main__":
    asyncio.run(main())
