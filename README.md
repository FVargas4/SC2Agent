# SC2Agent

This is a hand-in project on the Agent topic.

On this folder you will find the agent file (*terranAgent.py*), which if run correctly (with the proper libraries and with the game Starcraft 2 installed) will run an agent that plays such game. 

The agent will use the race Terran for playing and it's strategy at the beggining of this project is the following:
- Gatheruing minerals to be able to make two Barracks (*Marine* (soldier) *spawner*)
- Wait until it has created 10 marines and goes to attack the enemy. (This is a process that is repeated as many times as needed to either win or lose the game.)

These steps are good for defeating a very easy mode bot, but upping that difficulty the agent's loss time was getting smaller and smaller. So I decided to add some new features to the agent including:
- Making more barracks so more marines are being created (total of three)
- Creating a refinery so the Terrans can gather vespene gas on the Command Center.
- Create a Engineering Bay so updates can be made on the go. (But the framework does not seems to make this possible)

