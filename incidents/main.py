import os
import subprocess
import sys
from pathlib import Path


NGROK_AUTHTOKEN = "3KaYJCzinIWOqpslSzNWppRtuwM_2jYDXjJEiebXCuGa5AjUh"


def main() -> None:
    env = os.environ.copy()
    env["NGROK_AUTHTOKEN"] = NGROK_AUTHTOKEN

    project_main = Path(__file__).resolve().parent.parent / "main.py"

    if project_main.exists() and project_main.resolve() != Path(__file__).resolve():
        subprocess.run([sys.executable, str(project_main)], env=env, check=True)


if __name__ == "__main__":
    main()

