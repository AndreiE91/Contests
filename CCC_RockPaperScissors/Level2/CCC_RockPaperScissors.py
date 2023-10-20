# Function to determine the winner of a Rock-Paper-Scissors tournament
def rock_paper_scissors(player1, player2):
    if player1 not in "RPS" or player2 not in "RPS":
        return "Invalid input"
    if (player1 == "R" and player2 == "S") or (player1 == "S" and player2 == "P") or (player1 == "P" and player2 == "R"):
        return player1
    else:
        return player2
    
# Function to process and simulate the Rock-Paper-Scissors tournament rounds
def process_tournament(tournament, m):
    while len(tournament) > m / 4:
        new_round = ""
        for i in range(0, len(tournament), 2):
            winner = rock_paper_scissors(tournament[i], tournament[i + 1])
            new_round += winner
        tournament = new_round
    return tournament

# Process Rock-Paper-Scissors tournaments for levels 1 to 5
for level in range(1, 6):
    input_file_name = f"level2_{level}.in"
    output_file_name = f"level2_{level}.out"

    # Read input from the corresponding input file
    with open(input_file_name, "r") as input_file:
        n, m = map(int, input_file.readline().strip().split())  # Read n and m
        tournaments = [line.strip() for line in input_file]

    # Process the tournaments and store the results
    results = []
    for i in range(n):
        tournament = tournaments[i]
        winner = process_tournament(tournament, m)
        results.append(winner)

    # Write results to the corresponding output file
    with open(output_file_name, "w") as output_file:
        for winner in results:
            output_file.write(winner + "\n")
