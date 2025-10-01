import logging
import warnings
from google.adk import Agent
from .config import Config
from .prompts import INSTRUCTION
from .shared_libraries.callbacks import before_agent
from .tools.tools import (
    check_product_list,
    get_product_recommendations,
    check_product_availability,
    access_cart_information,
    modify_cart,
)

warnings.filterwarnings("ignore", category=UserWarning, module=".*pydantic.*")

configs = Config()

# configure logging __name__
logger = logging.getLogger(__name__)


root_agent = Agent(
    model=configs.agent_settings.model,
    instruction=INSTRUCTION,
    name=configs.agent_settings.name,
    tools=[
        check_product_list,
        get_product_recommendations,
        check_product_availability,
        access_cart_information,
        modify_cart,
    ],
    before_agent_callback=before_agent,
)
