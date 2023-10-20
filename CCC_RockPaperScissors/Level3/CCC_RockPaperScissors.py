import random

def shuffle_string(input_string):
    # Convert the string to a list of characters
    char_list = list(input_string)
    
    # Shuffle the list of characters
    random.shuffle(char_list)
    
    # Join the shuffled characters back into a string
    shuffled_string = ''.join(char_list)
    
    return shuffled_string

def masked_shuffle(initial_string, mask):    
    if len(initial_string) != len(mask):
        raise ValueError("Invalid mask length")
    
    # Convert the combined string to a list of characters
    char_list = list(initial_string)

    # Find the indices of '0' characters based on the mask
    zero_indices = [i for i, char in enumerate(mask) if char == '0']

    substring_list = []

    # Create substring only of masked indexes
    for index in zero_indices:
        if char_list[index] not in "RPS":
            raise ValueError("Invalid character outside of RPS in random shuffle")
        substring_list.append(char_list[index])
            
    # Shuffle only the substring
    random.shuffle(substring_list)
    
    # Join back shuffled substring into initial stirng
    count = 0
    for index in zero_indices:
        char_list[index] = substring_list[count]
        count += 1

    # Join the characters back into the initial string_list
    shuffled_string = ''.join(char_list)

    return shuffled_string

# Function to determine the winner of a Rock-Paper-Scissors tournament
def rock_paper_scissors(player1, player2):
    if player1 not in "RPS" or player2 not in "RPS":
        raise ValueError("Invalid input.")
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

# Function to check whether win condition is met or not
def check_win_condition(pairing, m):
    processed_pairing = process_tournament(pairing, m)
    if "S" not in processed_pairing:
        return False
    if "R" in processed_pairing:
        return False
    return True

# Function to generate initial pairings with specified counts of R, P, and S
def generate_initial_pairing(i, m, r_counts, p_counts, s_counts, level):
    if r_counts[i] + p_counts[i] + s_counts[i] != m:
        raise ValueError("Invalid input counts for R, P, and S.")
    
    pairing = ""
    
    # Create a mask for shuffling only certain indexes
    mask = '0' * m
    
    count = 0
    # Create as many PRRR groups as possible
    while r_counts[i] >= 3 and p_counts[i] >= 1:
        pairing += "PRRR"
        r_counts[i] -= 3
        p_counts[i] -= 1
        mask = mask[:count * 4] + "1" * 4 + mask[(count+1)*4:]
        count += 1
    count *= 4
    # Add the remaining R and P trivially
    while r_counts[i] > 0 or p_counts[i] > 0:
        if p_counts[i] > 0:
            pairing += "P"
            p_counts[i] -= 1
        if r_counts[i] > 0:
            pairing += "R"
            r_counts[i] -= 1
        count += 1
    
    init_count = count
    # Group all S at the end
    while s_counts[i] > 0:
        pairing += "S"
        s_counts[i] -= 1
        count += 1
    mask = mask[:init_count] + "1" * (count - init_count) + mask[count + 1:]   
    
    while not check_win_condition(pairing, m):
        pairing = masked_shuffle(pairing, mask)
    
    if r_counts[i] + p_counts[i] + s_counts[i] != 0 or len(pairing) != m:
        print(f"level:{level}\nstep:{i}\nrock:{r_counts[i]}\npaper:{p_counts[i]}\nscissors:{s_counts[i]}\nlen:{len(pairing)}")
        raise ValueError("Something is wrong in the pairing making part of code.")
    
    print(f"i={i}:{process_tournament(pairing, m)}")
    print(mask)
    return pairing

# Process Rock-Paper-Scissors tournaments for levels 1 to 5
for level in range(1, 6):
    input_file_name = f"level3_{level}.in"
    output_file_name = f"level3_{level}.out"

    # Read input from the corresponding input file
    with open(input_file_name, "r") as input_file:
        n, m = map(int, input_file.readline().strip().split())  # Read n and m
        r_counts, p_counts, s_counts = [], [], []

        # Read the counts for each tournament
        for i in range(n):
            counts = input_file.readline().strip().split()
            r_count, p_count, s_count = 0, 0, 0
            for item in counts:
                count = int(item[:-1])  # Extract the count (excluding the last character)
                letter = item[-1]  # Extract the last character (R, P, or S)
                if letter == 'R':
                    r_count += count
                elif letter == 'P':
                    p_count += count
                elif letter == 'S':
                    s_count += count
            r_counts.append(r_count)
            p_counts.append(p_count)
            s_counts.append(s_count)

        initial_pairings = []
        # Generate pairings one by one and check if correct or not to proceed or keep trying
        for i in range(n):
            initial_pairing = initial_pairing = generate_initial_pairing(i, m, r_counts, p_counts, s_counts, level)
            initial_pairings.append(initial_pairing)
        
    # Write results to the corresponding output file
    with open(output_file_name, "w") as output_file:
        for pairing in initial_pairings:
            output_file.write(pairing + "\n")
