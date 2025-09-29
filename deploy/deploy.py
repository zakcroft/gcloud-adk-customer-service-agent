import argparse
import asyncio
import logging
import sys
import time

import vertexai
from vertexai import agent_engines
from google.api_core.exceptions import NotFound, GoogleAPIError

from agent.config import Config
from agent.root_agent import root_agent

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

configs = Config()
STAGING_BUCKET = f"gs://{configs.STAGING_BUCKET}"


def init_vertexai():
    """Initialize Vertex AI with project configuration."""
    vertexai.init(
        project=configs.CLOUD_PROJECT,
        location=configs.CLOUD_LOCATION,
        staging_bucket=STAGING_BUCKET,
    )
    logger.info(f"Initialized Vertex AI for project: {configs.CLOUD_PROJECT}")


def deploy_agent() -> str:
    """Deploy the agent and return the resource name."""
    logger.info("Starting agent deployment...")

    try:
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

        logger.info("Deployment finished successfully!")
        logger.info(f"Resource Name: {remote_app.resource_name}")
        print(f"\n✅ Deployment successful!")
        print(f"📋 Resource Name: {remote_app.resource_name}")
        print(f"🔗 Project: {configs.CLOUD_PROJECT}")
        print(f"📍 Location: {configs.CLOUD_LOCATION}")

        return remote_app.resource_name

    except Exception as e:
        logger.error(f"Deployment failed: {e}")
        print(f"\n❌ Deployment failed: {e}")
        sys.exit(1)


def delete_agent(resource_name: str) -> bool:
    """Delete a deployed agent."""
    logger.info(f"Attempting to delete agent: {resource_name}")

    try:
        # First check if the agent exists
        agent_engines.get(resource_name=resource_name)

        # Delete the agent
        agent_engines.delete(resource_name=resource_name, force=True)

        logger.info(f"Agent {resource_name} deleted successfully")
        print(f"\n✅ Agent deleted successfully!")
        print(f"📋 Resource Name: {resource_name}")
        return True

    except NotFound:
        logger.warning(f"Agent {resource_name} not found")
        print(f"\n⚠️  Agent not found: {resource_name}")
        return False

    except Exception as e:
        logger.error(f"Failed to delete agent: {e}")
        print(f"\n❌ Failed to delete agent: {e}")
        return False


async def test_agent(resource_name: str) -> bool:
    """Test a deployed agent with sample queries."""
    logger.info(f"Testing agent: {resource_name}")

    try:
        # Get the agent instance
        remote_agent = agent_engines.get(resource_name=resource_name)


        remote_session = await remote_agent.async_create_session(user_id="u_456")
        print(remote_session)

        print(f"\n🧪 Testing agent: {resource_name}")
        print("=" * 60)

        test_queries = [
            "Do you sell seeds?",
            "What do you have in the vegetable seeds department?",
            "Can you add 2 packets of tomato seeds to my cart?",
            "Actually, remove 1 packet from my cart",
            "What's in my cart now?",
        ]

        success_count = 0
        for i, query in enumerate(test_queries, 1):
            print(f"\n🔍 Test {i}: {query}")
            print("-" * 40)

            try:
                response_received = False
                async for event in remote_agent.async_stream_query(
                    user_id="u_456",
                    session_id=remote_session["id"],
                    message=query,  # Fixed: Use the actual query instead of hardcoded message
                ):
                    print(event)
                    response_received = True

                if response_received:
                    print("✅ Query completed successfully")
                    success_count += 1
                else:
                    print("⚠️  No response received")

            except Exception as e:
                print(f"❌ Query failed: {e}")

            time.sleep(3)  # Pause between queries to allow conversation flow

        print(f"\n📊 Test Results: {success_count}/{len(test_queries)} queries successful")

        if success_count == len(test_queries):
            print("🎉 All tests passed!")
            return True
        else:
            print("⚠️  Some tests failed")
            return False

    except NotFound:
        logger.error(f"Agent {resource_name} not found")
        print(f"\n❌ Agent not found: {resource_name}")
        return False

    except Exception as e:
        logger.error(f"Failed to test agent: {e}")
        print(f"\n❌ Failed to test agent: {e}")
        return False


def list_agents():
    """List all deployed agents in the project."""
    logger.info("Listing deployed agents...")

    try:
        # List all agent engines in the project
        agents = agent_engines.list()

        print(f"\n📋 Deployed Agents in Project: {configs.CLOUD_PROJECT}")
        print("=" * 60)

        agent_list = list(agents)

        if not agent_list:
            print("No agents found in this project.")
            print("💡 Deploy an agent using: python deploy/deploy.py --deploy")
            return

        print(f"Found {len(agent_list)} agent(s):")
        print()

        for i, agent in enumerate(agent_list, 1):
            print(f"{i}. {agent.display_name}")
            print(f"   📋 Resource Name: {agent.resource_name}")
            print(f"   📅 Created: {agent.create_time}")
            print(f"   🔄 Updated: {agent.update_time}")

            # Show description if available
            if hasattr(agent, 'description') and agent.description:
                print(f"   📝 Description: {agent.description}")

            print()

        print("💡 Test an agent using: python deploy/deploy.py --test <resource_name>")
        print("💡 Delete an agent using: python deploy/deploy.py --delete <resource_name>")

    except Exception as e:
        logger.error(f"Failed to list agents: {e}")
        print(f"\n❌ Failed to list agents: {e}")
        print("💡 Make sure you have the correct permissions and project configuration.")


def main():
    parser = argparse.ArgumentParser(
        description="Customer Service Agent Deployment Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python deploy/deploy.py --deploy                    # Deploy the agent
  python deploy/deploy.py --delete <resource_name>    # Delete a deployed agent
  python deploy/deploy.py --test <resource_name>      # Test a deployed agent
  python deploy/deploy.py --list                      # List deployed agents
        """
    )

    # Create mutually exclusive group for main actions
    action_group = parser.add_mutually_exclusive_group(required=True)

    action_group.add_argument(
        "--deploy",
        action="store_true",
        help="Deploy the customer service agent"
    )

    action_group.add_argument(
        "--delete",
        metavar="RESOURCE_NAME",
        help="Delete a deployed agent (provide resource name)"
    )

    action_group.add_argument(
        "--test",
        metavar="RESOURCE_NAME",
        help="Test a deployed agent (provide resource name)"
    )

    action_group.add_argument(
        "--list",
        action="store_true",
        help="List all deployed agents"
    )

    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )

    args = parser.parse_args()

    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Verbose logging enabled")

    # Initialize Vertex AI
    init_vertexai()

    # Execute the requested action
    try:
        if args.deploy:
            deploy_agent()

        elif args.delete:
            delete_agent(args.delete)

        elif args.test:
           asyncio.run(test_agent(args.test))

        elif args.list:
            list_agents()

    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
