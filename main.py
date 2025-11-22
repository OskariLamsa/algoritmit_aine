import os
import runpy
import sys

def list_algorithms():
    path = os.path.join(os.path.dirname(__file__), "algorithms")
    files = os.listdir(path)

    algorithms = [
        f[:-3] for f in files
        if f.endswith(".py") and f != "__init__.py"
    ]

    return algorithms

def list_maps():
    path = os.path.join(os.path.dirname(__file__), "maps_data")
    files = os.listdir(path)
    maps = [
        f[:-4] for f in files
        if f.endswith(".csv")
    ]
    return maps


def main():
    algorithms = list_algorithms()
    maps = list_maps()
    print("Available algorithms:")
    for i in algorithms:
        print(f" - {i}")

    algo_choice = input("\nWhich algorithm do you want to run? ")

    if algo_choice not in algorithms:
        print(f"Error: '{algo_choice}' is not a valid algorithm.")
        return

    print("\nAvailable maps are:")
    for i in maps:
        print(f" - {i}")

    map_choice = input("Which map do you want to choose? ")

    if map_choice not in maps:
        print(f"Error. {map_choice} is not a valid map name.")
        return
    sys.argv = ["", map_choice + ".csv"]
    runpy.run_module(f"algorithms.{algo_choice}", run_name="__main__")


if __name__ == "__main__":
    main()
