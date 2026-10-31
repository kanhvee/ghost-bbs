# ghost-bbs

A séance with the ghosts of dead technology (GeoCities, Flash, MSN Messenger),
running offline on Gemma 3 via Ollama. Standard library only.

## Run
ollama pull gemma3:4b
python ghost_bbs.py

Commands: /switch <ghost>, /ghosts, /quit

Install Ollama from ollama.com, then run `ollama pull gemma3:4b` in a terminal.
Save `ghost_bbs.py` to a folder and run `python ghost_bbs.py`. 
Chat with a ghost or two to make sure it works. 
If it can't connect, run `ollama serve` first.
