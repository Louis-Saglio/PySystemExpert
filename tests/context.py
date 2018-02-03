import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from system_expert import Fact, Rule, Engine
import system_expert.helpers as helpers
import system_expert.restful_api as api_rest