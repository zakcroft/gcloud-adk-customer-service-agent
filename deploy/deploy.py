import argparse
import logging
import sys

import vertexai
from vertexai import agent_engines

from agent.config import Config
from agent.root_agent import root_agent

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

configs = Config()

STAGING_BUCKET = f"gs://{configs.CLOUD_PROJECT}-{configs.STAGING_BUCKET}"

vertexai.init(
    project=configs.CLOUD_PROJECT,
    location=configs.CLOUD_LOCATION,
    staging_bucket=STAGING_BUCKET,
)

app = agent_engines.AdkApp(
    agent=root_agent,
    enable_tracing=True,
)

remote_app = agent_engines.create(
    agent_engine=app,
    requirements=[
        "google-cloud-aiplatform[adk,agent_engines]",
        "google-cloud-aiplatform>=1.114.0",
        "pydantic>=2.11.9",
        "pydantic-settings>=2.10.1",
        "cloudpickle>=3.1.1",
    ],
    extra_packages=['./agent'],
)

print(f"Deployment finished!")
print(f"Resource Name: {remote_app.resource_name}")
# Resource Name: "projects/{PROJECT_NUMBER}/locations/{LOCATION}/reasoningEngines/{RESOURCE_ID}"
#       Note: The PROJECT_NUMBER is different than the PROJECT_ID.
