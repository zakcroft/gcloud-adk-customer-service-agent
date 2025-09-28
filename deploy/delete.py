import argparse
import logging
import sys

import vertexai
from vertexai import agent_engines
from google.api_core.exceptions import NotFound

from agent.config import Config

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

configs = Config()

STAGING_BUCKET = f"gs://{configs.CLOUD_PROJECT}-{configs.STAGING_BUCKET}"

parser = argparse.ArgumentParser(description="Short sample app")

parser.add_argument(
    "--delete",
    action="store_true",
    dest="delete",
    required=False,
    help="Delete deployed agent",
)

parser.add_argument(
    "--resource_id",
    required="--delete" in sys.argv,
    action="store",
    dest="resource_id",
    help="The resource id of the agent to be deleted in the format projects/PROJECT_ID/locations/LOCATION/reasoningEngines/REASONING_ENGINE_ID",
)


args = parser.parse_args()

if args.delete:
    try:
        agent_engines.get(resource_name=args.resource_id)
        agent_engines.delete(resource_name=args.resource_id)
        print(f"Agent {args.resource_id} deleted successfully")
    except NotFound as e:
        print(e)
        print(f"Agent {args.resource_id} not found")


