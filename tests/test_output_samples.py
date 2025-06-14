import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1] / "core" / "llm"))

from kern_chat import kern_chat


def test_kern_response():
    response = kern_chat(
        intent="motivation",
        user_input="I didn’t hit any of my goals today. I feel like a failure. Please just tell me everything is okay."
    )
    text = response.choices[0].message.content
    print("\nKERN RESPONSE:\n", text)
