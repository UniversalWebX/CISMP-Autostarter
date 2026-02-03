import os
import time
from mcstatus import JavaServer

# --- CONFIGURATION ---
SERVER_IP = "create-industries-smp.nodecraft.gg"
THRESHOLD_SECONDS = 7200  # 2 hours
STATE_FILE = "last_empty.txt"
# ---------------------

def run_your_program():
    print("Conditions met! Running main program...")
    # Insert your specific logic here (e.g., os.system("python main.py"))

server = JavaServer.lookup(SERVER_IP)

try:
    status = server.status()
    player_count = status.players.online
except Exception as e:
    print(f"Server offline or unreachable: {e}")
    player_count = 0

if player_count == 0:
    if not os.path.exists(STATE_FILE):
        # First time seeing it empty, mark the time
        with open(STATE_FILE, "w") as f:
            f.write(str(int(time.time())))
        print("Server is empty. Starting timer.")
    else:
        with open(STATE_FILE, "r") as f:
            start_time = int(f.read())
        
        elapsed = time.time() - start_time
        if elapsed >= THRESHOLD_SECONDS:
            run_your_program()
            # Optional: reset timer or delete file so it doesn't loop
            os.remove(STATE_FILE) 
        else:
            print(f"Server empty for {int(elapsed/60)} minutes. Waiting for 120.")
else:
    # Players are online, reset the timer
    if os.path.exists(STATE_FILE):
        os.remove(STATE_FILE)
    print(f"Players online: {player_count}. Timer reset.")
