import os
import runpy

def list_algorithms():
    path = os.path.join(os.path.dirname(__file__), "algorithms")
    files = os.listdir(path)

    algorithms = [
        f[:-3] for f in files
        if f.endswith(".py") and f != "__init__.py"
    ]

    return algorithms


def main():
    algorithms = list_algorithms()

    print("Available algorithms:")
    for alg in algorithms:
        print(f" - {alg}")

    choice = input("\nWhich algorithm do you want to run? ")

    if choice not in algorithms:
        print(f"Error: '{choice}' is not a valid algorithm.")
        return

    print(f"\nRunning algorithms.{choice}...\n")

    # Run as a module so __name__ == '__main__' inside the file
    runpy.run_module(f"algorithms.{choice}", run_name="__main__")


if __name__ == "__main__":
    main()
