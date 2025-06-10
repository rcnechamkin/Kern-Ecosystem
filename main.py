#Enforces AIRIK
from core.airik_enforcer import enforce_airik
enforce_airik()

#Launches API
from api.start_api import start_api

app = start_api()

#Fun readout
GREEN = "\033[92m"
BOLD = "\033[1m"
RESET = "\033[0m"

print(f"{GREEN}{BOLD}Avrana is online.{RESET}")
print(f"{GREEN}Kern Prime is awake.{RESET}")
print(f"{GREEN}AIRIK is enforced.{RESET}")
print(f"{BOLD}Listening at http://127.0.0.1:8000{RESET}")

