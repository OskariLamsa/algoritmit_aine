from invoke import task
import subprocess
import sys

@task
def main(c):
    #c.run("poetry run python main.py")
    def main(c):
        cmd = ["poetry", "run", "python", "main.py"]
        subprocess.run(cmd, check=False)