# YRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR LYYYYYYYYYYYYYYY YRRRRRRRRRRRRRRR YRRRRRRRRRRRRRRR YRRRRRRRRRRRRRRR
import math, random
# Function to determine the winner of a Rock-Paper-Scissors-Lizard-Spock tournament
def rock_paper_scissors(player1, player2):
    if player1 not in "RPSLY" or player2 not in "RPSLY":
        raise ValueError("Invalid input.")
    if (
        (player1 == "R" and (player2 == "L" or player2 == "S")) or
        (player1 == "P" and (player2 == "R" or player2 == "Y")) or
        (player1 == "S" and (player2 == "P" or player2 == "L")) or
        (player1 == "L" and (player2 == "Y" or player2 == "P")) or
        (player1 == "Y" and (player2 == "R" or player2 == "S"))
    ):
        return player1
    else:
        return player2
    
# Function to process and simulate the Rock-Paper-Scissors tournament rounds
def process_tournament(tournament, m):
    while len(tournament) > 1:
        new_round = ""
        for i in range(0, len(tournament), 2):
            winner = rock_paper_scissors(tournament[i], tournament[i + 1])
            new_round += winner
        tournament = new_round
    return tournament

# Function to check whether win condition is met or not
def check_win_condition(pairing, m, character):
    processed_pairing = process_tournament(pairing, m)
    if processed_pairing in character:
        return True
    else:
        return False
    
def letter_count(pairing, m):
    rcount, pcount, scount, lcount, ycount = 0, 0, 0, 0, 0
    """ if len(pairing) != m:
        print(len(pairing), m)
        raise ValueError("Invalid pairing length.") """
    for letter in pairing:
        if letter == "R":
            rcount += 1
        if letter == "P":
            pcount += 1
        if letter == "S":
            scount += 1
        if letter == "L":
            lcount += 1
        if letter == "Y":
            ycount += 1
    return (rcount, pcount, scount, lcount, ycount)

# Fitness function based on win condition
def fitness_win(pairing, m, rcount, pcount, scount, lcount, ycount):
    if letter_count(pairing, m) != (rcount, pcount, scount, lcount, ycount):
        return 0
    processed_pairing, score = fitness_helper(pairing, m)
    if processed_pairing == "S":
        return 100
    else:
        return score

# Function to help fitness function determine score
def fitness_helper(tournament, m):
    score = 0
    while len(tournament) > 1:
        new_round = ""
        for i in range(0, len(tournament), 2):
            winner = rock_paper_scissors(tournament[i], tournament[i + 1])
            new_round += winner
        tournament = new_round
        if "S" in tournament:
            score += (100 / int(math.log2(m))) + random.randint(1, 5)
    return (tournament, score)

def shuffle_string(input_string):
    # Convert the string to a list of characters
    char_list = list(input_string)
    
    # Shuffle the list of characters
    random.shuffle(char_list)
    
    # Join the shuffled characters back into a string
    shuffled_string = ''.join(char_list)
    
    return shuffled_string

# 91R 0P 1S 8L 28Y

m = 64
pairing = "RYRRRYLRYYRYRYRRRYRRRRRRLRRYRYYRLYRYYRRRLRYRLRRRRRRYYYYRRYYYLYLS" 
pairing = pairing.replace(" ", "")   
    
letter_counts = letter_count(pairing, m)    
    
print(letter_counts)
print(len(pairing))
print(pairing)
print(f"fitness={fitness_win(pairing,m, *letter_counts)}")    
    
if check_win_condition(pairing, m, "S"):
    print("S wins")
else:
    print("S loses")
    
""" for _ in range(1000):
    pairing = shuffle_string(pairing)
    fitness = fitness_win(pairing,m, *letter_counts)
    if fitness > 10:
        print(f"fitness={fitness}")
        print(pairing) """