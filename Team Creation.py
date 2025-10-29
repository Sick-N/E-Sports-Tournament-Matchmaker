'''
Author: Nicolas Sigler
Date: 10/29/2025
Version: 1.0
Purpose: Makes teams for E-sports tournaments based off an elo system where the
lowest rank is set to 0 elo. Optional modes of draft are available such as Snake/Captain.
If manual teams are created then it will display the expected elo level of that team based
off their ranks.
'''
import itertools
import random

# Valorant rank to ELO mapping (Iron 1 = 0, each division = 100 ELO)
VALORANT_RANKS = {
    'iron 1': 0, 'iron 2': 100, 'iron 3': 200,
    'bronze 1': 300, 'bronze 2': 400, 'bronze 3': 500,
    'silver 1': 600, 'silver 2': 700, 'silver 3': 800,
    'gold 1': 900, 'gold 2': 1000, 'gold 3': 1100,
    'platinum 1': 1200, 'platinum 2': 1300, 'platinum 3': 1400,
    'diamond 1': 1500, 'diamond 2': 1600, 'diamond 3': 1700,
    'ascendant 1': 1800, 'ascendant 2': 1900, 'ascendant 3': 2000,
    'immortal 1': 2100, 'immortal 2': 2200, 'immortal 3': 2300,
    'radiant': 2400
}

# Rocket League rank to ELO mapping
ROCKET_LEAGUE_RANKS = {
    'unranked': 0,
    'bronze 1': 100, 'bronze 2': 200, 'bronze 3': 300,
    'silver 1': 400, 'silver 2': 500, 'silver 3': 600,
    'gold 1': 700, 'gold 2': 800, 'gold 3': 900,
    'platinum 1': 1000, 'platinum 2': 1100, 'platinum 3': 1200,
    'diamond 1': 1300, 'diamond 2': 1400, 'diamond 3': 1500,
    'champion 1': 1600, 'champion 2': 1700, 'champion 3': 1800,
    'grand champion 1': 1900, 'grand champion 2': 2000, 'grand champion 3': 2100,
    'supersonic legend': 2200
}

# Marvel Rivals rank to ELO mapping
MARVEL_RIVALS_RANKS = {
    'bronze 3': 0, 'bronze 2': 100, 'bronze 1': 200,
    'silver 3': 300, 'silver 2': 400, 'silver 1': 500,
    'gold 3': 600, 'gold 2': 700, 'gold 1': 800,
    'platinum 3': 900, 'platinum 2': 1000, 'platinum 1': 1100,
    'diamond 3': 1200, 'diamond 2': 1300, 'diamond 1': 1400,
    'grandmaster 3': 1500, 'grandmaster 2': 1600, 'grandmaster 1': 1700,
    'eternity': 1800, 'one above all': 1900
}

# Super Smash Bros Ultimate (using common competitive skill tiers)
SMASH_RANKS = {
    'beginner': 0,
    'casual': 200,
    'intermediate': 400,
    'advanced': 600,
    'expert': 800,
    'competitive': 1000,
    'tournament': 1200,
    'professional': 1400,
    'top player': 1600,
    'elite': 1800
}

GAME_SYSTEMS = {
    '1': {'name': 'Valorant', 'ranks': VALORANT_RANKS},
    '2': {'name': 'Rocket League', 'ranks': ROCKET_LEAGUE_RANKS},
    '3': {'name': 'Marvel Rivals', 'ranks': MARVEL_RIVALS_RANKS},
    '4': {'name': 'Super Smash Bros Ultimate', 'ranks': SMASH_RANKS}
}


def select_game():
    """Let user select which game's ranking system to use."""
    print("\nSelect game:")
    print("  1. Valorant")
    print("  2. Rocket League")
    print("  3. Marvel Rivals")
    print("  4. Super Smash Bros Ultimate")

    while True:
        choice = input("Choose game (1-4): ").strip()
        if choice in GAME_SYSTEMS:
            return GAME_SYSTEMS[choice]
        print("Please enter a number between 1 and 4.")


def select_algorithm():
    """Let user select team creation algorithm."""
    print("\nTeam creation algorithm:")
    print("  1. Balanced/Greedy (assigns to lowest ELO team, usually the best.)")
    print("  2. Snake Draft (alternating picks for balance)")
    print("  3. Random Assignment")
    print("  4. Captains Draft (captains pick players)")
    print("  5. Manual Selection")

    while True:
        choice = input("Choose algorithm (1-5): ").strip()
        if choice in ['1', '2', '3', '4', '5']:
            return choice
        print("Please enter a number between 1 and 5.")


def parse_rank_or_elo(rank_str, rank_system):
    """Parse either a game rank or raw ELO number."""
    rank_str = rank_str.strip().lower()

    # Try to parse as number first
    try:
        return int(rank_str)
    except ValueError:
        pass

    # Try to parse as game rank
    if rank_str in rank_system:
        return rank_system[rank_str]

    # Handle alternative formats (e.g., "iron1", "iron-1")
    rank_str = rank_str.replace('-', ' ').replace('_', ' ')
    if rank_str in rank_system:
        return rank_system[rank_str]

    raise ValueError(f"Invalid rank or ELO: {rank_str}")


def get_players(game_info):
    """Get player information from user input."""
    players = []
    game_name = game_info['name']
    rank_system = game_info['ranks']

    print(f"\nEnter players for {game_name} (format: 'Player Name, Rank/ELO')")
    print(f"Examples: 'Alice, {list(rank_system.keys())[5]}' or 'Bob, 1500'")
    print("Press Enter with empty input when done.\n")

    while True:
        player_input = input("Player: ").strip()
        if not player_input:
            break

        try:
            name, rank_or_elo = player_input.rsplit(',', 1)
            name = name.strip()
            elo = parse_rank_or_elo(rank_or_elo, rank_system)
            players.append({'name': name, 'elo': elo, 'input': rank_or_elo.strip()})
        except ValueError as e:
            print(f"Invalid format. {e}")
            continue

    return players


def calculate_team_average(team):
    """Calculate average ELO for a team."""
    if not team:
        return 0
    return sum(player['elo'] for player in team) / len(team)


def elo_to_rank(elo, rank_system):
    """Convert ELO back to game rank for display."""
    for rank, rank_elo in sorted(rank_system.items(), key=lambda x: x[1], reverse=True):
        if elo >= rank_elo:
            return rank.title()
    return list(rank_system.keys())[0].title()


def create_snake_draft_teams(players, team_size):
    """Create balanced teams using snake draft algorithm."""
    sorted_players = sorted(players, key=lambda x: x['elo'], reverse=True)

    num_teams = len(players) // team_size
    teams = [[] for _ in range(num_teams)]

    for i, player in enumerate(sorted_players[:num_teams * team_size]):
        round_num = i // num_teams
        if round_num % 2 == 0:
            team_idx = i % num_teams
        else:
            team_idx = num_teams - 1 - (i % num_teams)

        teams[team_idx].append(player)

    remaining = sorted_players[num_teams * team_size:]
    return teams, remaining


def create_balanced_greedy_teams(players, team_size):
    """Create balanced teams using greedy algorithm (assign to lowest ELO team)."""
    sorted_players = sorted(players, key=lambda x: x['elo'], reverse=True)

    num_teams = len(players) // team_size
    teams = [[] for _ in range(num_teams)]
    team_totals = [0] * num_teams

    for player in sorted_players[:num_teams * team_size]:
        # Find team with lowest total ELO
        min_team_idx = team_totals.index(min(team_totals))
        teams[min_team_idx].append(player)
        team_totals[min_team_idx] += player['elo']

    remaining = sorted_players[num_teams * team_size:]
    return teams, remaining


def create_random_teams(players, team_size):
    """Create teams using random assignment."""
    shuffled = players.copy()
    random.shuffle(shuffled)

    num_teams = len(players) // team_size
    teams = [[] for _ in range(num_teams)]

    for i, player in enumerate(shuffled[:num_teams * team_size]):
        team_idx = i % num_teams
        teams[team_idx].append(player)

    remaining = shuffled[num_teams * team_size:]
    return teams, remaining


def create_captains_draft_teams(players, team_size):
    """Create teams using captains draft (captains pick players)."""
    if len(players) < 2:
        print("Need at least 2 players for captains draft.")
        return [], players

    num_teams = len(players) // team_size

    if num_teams < 2:
        print("Not enough players to form multiple teams.")
        return [], players

    print("\n" + "=" * 60)
    print("CAPTAINS DRAFT")
    print("=" * 60)

    # Select captains
    print(f"\nSelect {num_teams} captains:")
    for i, player in enumerate(players, 1):
        print(f"  {i}. {player['name']} ({player['input']}, ELO: {player['elo']})")

    captains = []
    captain_indices = []

    while len(captains) < num_teams:
        try:
            choice = input(f"Select captain #{len(captains) + 1}: ").strip()
            idx = int(choice) - 1

            if idx < 0 or idx >= len(players):
                print("Invalid player number.")
                continue

            if idx in captain_indices:
                print("Player already selected as captain.")
                continue

            captains.append(players[idx])
            captain_indices.append(idx)
            print(f"✓ {players[idx]['name']} is captain of Team {len(captains)}")
        except ValueError:
            print("Please enter a valid number.")

    # Initialize teams with captains
    teams = [[captain] for captain in captains]

    # Remove captains from available players
    available_players = [p for i, p in enumerate(players) if i not in captain_indices]

    # Draft rounds
    pick_order = list(range(num_teams))
    round_num = 0

    while available_players and all(len(team) < team_size for team in teams):
        # Snake draft order
        if round_num % 2 == 1:
            pick_order.reverse()

        for team_idx in pick_order:
            if not available_players or len(teams[team_idx]) >= team_size:
                continue

            print(f"\n--- Team {team_idx + 1}'s pick (Captain: {captains[team_idx]['name']}) ---")
            print("Available players:")
            for i, player in enumerate(available_players, 1):
                print(f"  {i}. {player['name']} ({player['input']}, ELO: {player['elo']})")

            while True:
                try:
                    choice = input(f"Team {team_idx + 1} picks player: ").strip()
                    pick_idx = int(choice) - 1

                    if pick_idx < 0 or pick_idx >= len(available_players):
                        print("Invalid player number.")
                        continue

                    picked_player = available_players.pop(pick_idx)
                    teams[team_idx].append(picked_player)
                    print(f"✓ {picked_player['name']} joins Team {team_idx + 1}")
                    break
                except ValueError:
                    print("Please enter a valid number.")

        round_num += 1

    return teams, available_players


def create_manual_teams(players, team_size, game_info):
    """Manually create teams by selecting players."""
    teams = []
    remaining_players = players.copy()
    team_num = 1
    rank_system = game_info['ranks']

    print("\n" + "=" * 60)
    print("MANUAL TEAM CREATION")
    print("=" * 60)

    while len(remaining_players) >= team_size:
        print(f"\n--- Creating Team {team_num} ---")
        print("\nAvailable players:")
        for i, player in enumerate(remaining_players, 1):
            print(f"  {i}. {player['name']} ({player['input']}, ELO: {player['elo']})")

        team = []
        print(f"\nSelect {team_size} players for Team {team_num}")
        print("Enter player numbers separated by spaces (e.g., '1 3 5')")

        while True:
            try:
                selection = input(f"Select {team_size} players: ").strip()
                indices = [int(x) - 1 for x in selection.split()]

                if len(indices) != team_size:
                    print(f"Please select exactly {team_size} players.")
                    continue

                if any(i < 0 or i >= len(remaining_players) for i in indices):
                    print("Invalid player number(s).")
                    continue

                if len(set(indices)) != len(indices):
                    print("Cannot select the same player twice.")
                    continue

                selected = [remaining_players[i] for i in sorted(indices, reverse=True)]
                team.extend(selected)

                for i in sorted(indices, reverse=True):
                    remaining_players.pop(i)

                break
            except (ValueError, IndexError):
                print("Invalid input. Please enter valid player numbers.")

        teams.append(team)

        avg_elo = calculate_team_average(team)
        avg_rank = elo_to_rank(avg_elo, rank_system)
        player_names = ", ".join(p['name'] for p in team)
        print(f"\n✓ Team {team_num} created: {player_names}")
        print(f"  Average: {avg_elo:.1f} ELO (~{avg_rank})")

        team_num += 1

        if remaining_players:
            continue_choice = input("\nCreate another team? (y/n): ").strip().lower()
            if continue_choice != 'y':
                break

    return teams, remaining_players


def display_teams(teams, game_info):
    """Display teams with their players and average ELO."""
    rank_system = game_info['ranks']

    print("\n" + "=" * 60)
    print("TEAMS")
    print("=" * 60)

    for i, team in enumerate(teams, 1):
        if not team:
            continue

        player_list = []
        for player in team:
            player_list.append(f"{player['name']} ({player['input']})")

        player_names = ", ".join(player_list)
        avg_elo = calculate_team_average(team)
        avg_rank = elo_to_rank(avg_elo, rank_system)

        print(f"\nTeam {i}: {player_names}")
        print(f"Average ELO: {avg_elo:.1f} (~{avg_rank})")

    print("\n" + "=" * 60)


def main():
    print("=" * 60)
    print("MULTI-GAME TEAM GENERATOR")
    print("=" * 60)

    # Select game
    game_info = select_game()
    print(f"\nSelected: {game_info['name']}")

    # Select algorithm
    algorithm = select_algorithm()

    # Get team size
    while True:
        try:
            team_size = int(input("\nEnter number of players per team: "))
            if team_size < 1:
                print("Team size must be at least 1.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")

    # Get players
    players = get_players(game_info)

    if len(players) < team_size:
        print(f"\nNot enough players! Need at least {team_size} players.")
        return

    # Create teams based on selected algorithm
    if algorithm == '1':
        teams, remaining = create_snake_draft_teams(players, team_size)
    elif algorithm == '2':
        teams, remaining = create_balanced_greedy_teams(players, team_size)
    elif algorithm == '3':
        teams, remaining = create_random_teams(players, team_size)
    elif algorithm == '4':
        teams, remaining = create_captains_draft_teams(players, team_size)
    else:  # algorithm == '5'
        teams, remaining = create_manual_teams(players, team_size, game_info)

    # Display results
    display_teams(teams, game_info)

    if remaining:
        print("\nPlayers not assigned to teams:")
        for player in remaining:
            print(f"  - {player['name']} ({player['input']}, ELO: {player['elo']})")


if __name__ == "__main__":
    main()