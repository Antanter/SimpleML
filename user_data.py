import pickle
from collections import defaultdict
import atexit
import os

STATE_FILE = "user_state.pkl"

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "rb") as f:
            data = pickle.load(f)
            return defaultdict(list, data)
    return defaultdict(list)

def save_state():
    with open(STATE_FILE, "wb") as f:
        pickle.dump(dict(user_state), f)

user_state = load_state()

atexit.register(save_state)
