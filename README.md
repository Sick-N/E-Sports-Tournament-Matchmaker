# E-Sports-Tournament-Matchmaker
Allows the user to take well known competitive e-sports games and create tournaments with them using a random amount of players. 

All games use an ELO system in the background, with the lowest ELO (0) being assigned to the lowest rank (such as unranked, or iron 1). Every rank above that increases its elo by 100 (e.g iron 3 would be 200 elo, so on and so forth).

Choosing a game simply allows you to use the ingame rank instead of manually assigning an elo value to the player.
  If you picked Valorant as the chosen game, you could input "Jim, Gold 3" instead of "Jim, 1100". 
  When a player is adamant they deserve the 50 extra rr they have, then you'll have to manually add it to the elo value: "Jim, 1150".

if your game is not listed, pick any game (it won't matter) and simply use elo to calculate the skill gap between players.


When picking a drafting mode, Balanced/Greedy is recommended for the best draft possible, with snake being a close second. You cannot currently manually add teams after
the teams have been generate, or edit existing teams. 

The Bracket Generator takes in the output of the Team Creation script and will create an initial tournament bracket based off the teams made from the Team Creation script. You can then easily put those teams into a separate tournament website: [https://scoreleader.com/bracket/](url)

Enjoy!
