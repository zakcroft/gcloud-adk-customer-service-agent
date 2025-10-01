import os
import pytest

from dotenv import find_dotenv, load_dotenv
from google.adk.evaluation.agent_evaluator import AgentEvaluator

pytest_plugins = ("pytest_asyncio",)

@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv(find_dotenv("../.env"))


# AgentEvaluator.migrate_eval_data_to_new_schema(
#     os.path.join(os.path.dirname(__file__), "eval_data/full_conversation_old.test.json"),
#     os.path.join(os.path.dirname(__file__), "eval_data/full_conversation.test.json"),
# )

@pytest.mark.asyncio
async def test_eval_simple():
    """Test basic cart inquiry functionality."""
    await AgentEvaluator.evaluate(
        "app.agent",
        os.path.join(os.path.dirname(__file__), "eval_data/simple.test.json"),
        num_runs=1,
        print_detailed_results=True
    )


# @pytest.mark.asyncio
# async def test_eval_cart_management():
#     """Test cart operations: add, check, remove items."""
#     await AgentEvaluator.evaluate(
#         "app.agent",
#         os.path.join(
#             os.path.dirname(__file__), "eval_data/cart_management.test.json"
#         ),
#         num_runs=1,
#         print_detailed_results=True
#     )


@pytest.mark.asyncio
async def test_eval_full_conversation():
    """Test complete conversation flow: greeting, product inquiry, cart management.

    Note: This test has 8 conversation turns and may hit API rate limits.
    Run separately with delays if needed.
    """
    await AgentEvaluator.evaluate(
        "app.agent",
        os.path.join(
            os.path.dirname(__file__), "eval_data/full_conversation.test.json"
        ),
        num_runs=1,
        print_detailed_results=True
    )
