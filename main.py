import subprocess
import time
import os

import pandas as pd

SERVER_PATH = "reversi_server.py"
OUR_AI_PATH = "group10_player.py"
GREEDY_AI_PATH = "greedy_player.py"


def start_server():
    print("Game Starts")
    server_process = subprocess.Popen(['python3', SERVER_PATH], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2)  # Wait for the server to start properly
    return server_process

def run_game(isFirstPlayer):
    print("Playing...")
    if isFirstPlayer:
        my_ai_process = subprocess.Popen(['python3', OUR_AI_PATH])
        time.sleep(1)
        greedy_ai_process = subprocess.Popen(['python3', GREEDY_AI_PATH], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        greedy_ai_process = subprocess.Popen(['python3', GREEDY_AI_PATH], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(1)
        my_ai_process = subprocess.Popen(['python3', OUR_AI_PATH])

    my_ai_process.wait()
    greedy_ai_process.wait()

def stop_server(server_process):
    print("Press Enter to continue.")
    server_process.terminate()
    server_process.wait()

def delete_csv(filename):
    if os.path.exists(filename):
        os.remove(filename)
def read_csv(filename):
    df = pd.read_csv(filename)

    ai_score = df['Our AI'].sum()
    greedy_score = df['Greedy AI'].sum()

    diff = ai_score - greedy_score

    if diff > 0:
        print(f"Our AI Won by {diff} points")
    elif diff < 0:
        print(f"Our AI Lost by {-diff} points")
def play():
    print("Round 1: Our AI goes first")
    isFirstPlayer = True
    print("Our AI: White")
    print("Greedy AI: Black")
    server_process = start_server()
    run_game(isFirstPlayer)
    stop_server(server_process)

    print("\nRound 2: Greedy AI goes first")
    isFirstPlayer = False
    print("Greedy AI: White")
    print("Our AI: Black")
    server_process = start_server()
    run_game(isFirstPlayer)
    stop_server(server_process)

if __name__ == "__main__":
    filename = "scores.csv"
    delete_csv(filename)
    play()
    read_csv(filename)
