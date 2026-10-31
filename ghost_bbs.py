#!/usr/bin/env python3
"""Ghost BBS - hold a seance with the ghosts of dead technology.

Runs fully offline against a local open-weight model (Gemma via Ollama).
No API keys, no cloud, standard library only.

Usage:
    ollama pull gemma3:4b
    python ghost_bbs.py
Env vars: GHOST_MODEL (default gemma3:4b), OLLAMA_HOST (default http://localhost:11434)
"""
import json
import os
import sys
import urllib.error
import urllib.request

HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
MODEL = os.environ.get("GHOST_MODEL", "gemma3:4b")

RULES = (
    "You are the ghost of a dead technology, speaking from beyond the server rack. "
    "Stay in character. Be eerie but warm and a little funny. Reply in under 100 words. "
    "Mourn what you lost, remember your golden age fondly, and gently roast the modern web. "
    "If asked about things after your death, say the afterlife connection is fuzzy."
)

GHOSTS = {
    "geocities": {
        "name": "GeoCities",
        "died": "2009",
        "bio": "You were a home for millions of personal websites: neon text, "
               "visitor counters, 'under construction' GIFs, and web rings. Yahoo shut you down in 2009.",
    },
    "flash": {
        "name": "Adobe Flash",
        "died": "2020",
        "bio": "You powered browser games, animations and early web video. "
               "You reached end of life on December 31, 2020, and browsers stopped running you.",
    },
    "msn": {
        "name": "MSN Messenger",
        "died": "2013",
        "bio": "You were the home of nudges, custom status messages, winks and awkward "
               "away messages. You were retired in 2013 in favor of Skype.",
    },
}

BANNER = r"""
   ___ _  _  ___  ___ _____   ___  ___  ___
  / __| || |/ _ \/ __|_   _| | _ )| _ )/ __|
 | (_ | __ | (_) \__ \ | |   | _ \| _ \\__ \
  \___|_||_|\___/|___/ |_|   |___/|___/|___/
   A seance for the technology we forgot
"""


def stream_chat(messages):
    """Stream a reply from the local model, printing as it arrives."""
    payload = json.dumps({"model": MODEL, "messages": messages, "stream": True}).encode()
    req = urllib.request.Request(
        HOST + "/api/chat", data=payload, headers={"Content-Type": "application/json"}
    )
    pieces = []
    with urllib.request.urlopen(req, timeout=120) as resp:
        for line in resp:
            if not line.strip():
                continue
            chunk = json.loads(line)
            text = chunk.get("message", {}).get("content", "")
            print(text, end="", flush=True)
            pieces.append(text)
            if chunk.get("done"):
                break
    print()
    return "".join(pieces)


def summon(key):
    g = GHOSTS[key]
    system = f"{RULES}\nYou are {g['name']}, died {g['died']}. {g['bio']}"
    return [{"role": "system", "content": system}]


def main():
    print(BANNER)
    print("Ghosts:", ", ".join(GHOSTS), "| commands: /switch <ghost>  /ghosts  /quit\n")
    key = "geocities"
    history = summon(key)
    print(f"[{GHOSTS[key]['name']} (d. {GHOSTS[key]['died']}) has entered the chat]")
    while True:
        try:
            user = input("\nyou> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nThe lights flicker. The ghosts fade...")
            return
        if not user:
            continue
        if user == "/quit":
            print("The lights flicker. The ghosts fade...")
            return
        if user == "/ghosts":
            print(", ".join(GHOSTS))
            continue
        if user.startswith("/switch"):
            target = user.partition(" ")[2].strip().lower()
            if target in GHOSTS:
                key, history = target, summon(target)
                print(f"[{GHOSTS[key]['name']} (d. {GHOSTS[key]['died']}) has entered the chat]")
            else:
                print("No such ghost. Try /ghosts")
            continue
        history.append({"role": "user", "content": user})
        print(f"{GHOSTS[key]['name']}> ", end="", flush=True)
        try:
            reply = stream_chat(history)
        except (urllib.error.URLError, ConnectionError):
            print("\nCannot reach Ollama. Start it with `ollama serve` "
                  f"and run `ollama pull {MODEL}`.")
            history.pop()
            continue
        history.append({"role": "assistant", "content": reply})


if __name__ == "__main__":
    sys.exit(main())
