import random
import math
import copy

class Candidate:
    def __init__(self, pairing, fitness):
        self.pairing = pairing
        self.fitness = fitness

    def __str__(self):
        return f"Pairing: {self.pairing}, Fitness: {self.fitness}"
    
class z_character:
    def __init__(self, index):
        self.index = index
        self.met_p = False
        self.met_l = False
        self.met_y = False
    def __str__(self):
        return f"Z: {self.index}, {self.met_p}, {self.met_l}, {self.met_y}"
    
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
        if char_list[index] not in "RPSLY":
            raise ValueError("Invalid character outside of RPSLY in random shuffle")
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

def mutate(pairing, m, numMutations, x_indexes, z_characters, fitness):
    z_indexes = []
    for character in z_characters:
        z_indexes.append(character.index)
    # Find the indices of '0' characters based on the mask
    for i in range(numMutations):
        index1 = random.randint(0, len(x_indexes) - 1)
        index2 = random.randint(0, len(x_indexes) - 1)
        index1 = x_indexes[index1]
        index2 = x_indexes[index2]
        # Swap the characters at index1 and index2
        pairing_list = list(pairing)
        # The bigger the fitness, the less chance of random mutations
        if random.random() < (1 / fitness):
            pairing_list[index1], pairing_list[index2] = pairing_list[index2], pairing_list[index1]
        else:
            pairing_list[index1] = random.choice(("R", "P", "S", "L", "Y"))
        pairing = ''.join(pairing_list)
    return pairing

def mutate_unsafe(pairing, m, numMutations, x_indexes, z_characters):
    z_indexes = []
    for character in z_characters:
        z_indexes.append(character.index)
    # Find the indices of '0' characters based on the mask
    for i in range(numMutations):
        index1 = random.randint(0, len(x_indexes))
        index1 = x_indexes[index1]
        # Swap the characters at index1 and index2
        pairing_list = list(pairing)
        pairing_list[index1] = random.choice("R", "P", "S", "L", "Y")
        pairing = ''.join(pairing_list)
    return pairing

# Function to search for a z_character by index
def find_z_character_by_index(z_characters, target_index):
    for z_char in z_characters:
        if z_char.index == target_index:
            return z_char
    return None  # Return None if the index is not found in the list

# Function to determine the winner of a Rock-Paper-Scissors-Lizard-Spock tournament
def rock_paper_scissors(player1, player2, index, z_characters):
    if player1 not in "RPSLYZ" or player2 not in "RPSLYZ":
        raise ValueError("Invalid input.")
        
    if player1 == "Z" and player2 == "P":
        target_z = find_z_character_by_index(z_characters, index)
        target_z.met_p = True
        if target_z.met_p == True and target_z.met_l == True and target_z.met_y == True:
            z_characters.remove(target_z)
            return player2
        else:
            return player1
    
    if player1 == "Z" and player2 == "L":
        target_z = find_z_character_by_index(z_characters, index)
        target_z.met_l = True
        if target_z.met_p == True and target_z.met_l == True and target_z.met_y == True:
            z_characters.remove(target_z)
            return player2
        else:
            return player1
        
    if player1 == "Z" and player2 == "Y":
        target_z = find_z_character_by_index(z_characters, index)
        target_z.met_y = True
        if target_z.met_p == True and target_z.met_l == True and target_z.met_y == True:
            z_characters.remove(target_z)
            return player2
        else:
            return player1
        
    if player2 == "Z" and player1 == "P":
        target_z = find_z_character_by_index(z_characters, index + 1)
        target_z.met_p = True
        if target_z.met_p == True and target_z.met_l == True and target_z.met_y == True:
            z_characters.remove(target_z)
            return player1
        else:
            return player2
        
    if player2 == "Z" and player1 == "L":
        target_z = find_z_character_by_index(z_characters, index + 1)
        target_z.met_l = True
        if target_z.met_p == True and target_z.met_l == True and target_z.met_y == True:
            z_characters.remove(target_z)
            return player1
        else:
            return player2
        
    if player2 == "Z" and player1 == "Y":
        target_z = find_z_character_by_index(z_characters, index + 1)
        target_z.met_y = True
        if target_z.met_p == True and target_z.met_l == True and target_z.met_y == True:
            z_characters.remove(target_z)
            return player1
        else:
            return player2
        
    if player1 == "Z" and player2 == "Z":
        target_z1 = find_z_character_by_index(z_characters, index)
        target_z2 = find_z_character_by_index(z_characters, index + 1)
        target_z1.met_p = target_z1.met_p and target_z2.met_p
        target_z1.met_l = target_z1.met_l and target_z2.met_l
        target_z1.met_y = target_z1.met_y and target_z2.met_y
        z_characters.remove(target_z2)
        return player1
    
    if (
        (player1 == "R" and (player2 == "L" or player2 == "S")) or
        (player1 == "P" and (player2 == "R" or player2 == "Y")) or
        (player1 == "S" and (player2 == "P" or player2 == "L")) or
        (player1 == "L" and (player2 == "Y" or player2 == "P")) or
        (player1 == "Y" and (player2 == "R" or player2 == "S")) or
        (player1 == "Z" and (player2 == "S" or player2 == "R"))
    ):
        return player1
    else:
        return player2
    
# Function to process and simulate the Rock-Paper-Scissors tournament rounds
def process_tournament(tournament, m, z_characters):
    while len(tournament) > 1:
        new_round = ""
        for i in range(0, len(tournament), 2):
            winner = rock_paper_scissors(tournament[i], tournament[i + 1], i, z_characters)
            new_round += winner
        tournament = new_round
    return tournament
    
# Fitness function based on win condition
def fitness_win(pairing, m, z_characters):
    processed_pairing, score = fitness_helper(pairing, m, z_characters)
    if processed_pairing == "S":
        return 100
    else:
        return score

# Function to help fitness function determine score
def fitness_helper(tournament, m, z_characters):
    score = 0
    """ z_list_str = [str(z) for z in z_characters]
    print(z_list_str)
    print(tournament) """
    while len(tournament) > 1:
        new_round = ""
        for i in range(0, len(tournament), 2):
            # Use a list comprehension to convert objects to strings and join them
            
            #print(f"fitnesshelper:{tournament[i]}, {tournament[i + 1]}, {i}")
            winner = rock_paper_scissors(tournament[i], tournament[i + 1], i, z_characters)
            new_round += winner
        tournament = new_round
        for z_character in z_characters:
            z_character.index //= 2
        """ z_list_str = [str(z) for z in z_characters]
        print(z_list_str)
        print(tournament) """
            
        if "S" in tournament:
            score += (100 / int(math.log2(m)))
            
    return (tournament, score)

def replace_character(original_string, index, new_character):
    if 0 <= index < len(original_string):
        # Create a new string with the character replaced
        new_string = original_string[:index] + new_character + original_string[index + 1:]
        return new_string
    else:
        # Handle the case where the index is out of range
        return original_string  # or raise an error, return None, etc.

def x_shuffle(pairing, m, x_indexes):
    for i in range(m):
        if i in x_indexes:
            pairing = replace_character(pairing, i, random.choice(('P', 'S', 'R', 'L', 'Y')))
            
    return pairing

def process_initial_pairing(i, m, pairing, level):
    x_indexes = []
    z_characters = []
    for i in range(m):
        if pairing[i] == 'X':
            pairing = replace_character(pairing, i, random.choice(('P', 'S', 'R', 'L', 'Y')))
            x_indexes.append(i)
        if pairing[i] == 'Z':
            z_characters.append(z_character(i))
    pairing = pairing[:-1]
    
    initial_z = copy.deepcopy(z_characters)
    """ print("First initial z copy: ", end = "")
    for zobj in initial_z:
        print(zobj, end = "")
    print() """
    
    # Get a list of decent candidates selected by random chance
    # Threshold of selection increases when many individuals qualify and decreases over time when they don't         
    threshold = 65
    candidates = []
    while True:
        z_characters = copy.deepcopy(initial_z)
        """ print("Subsequent initial z copy: ", end = "")
        for zobj in z_characters:
            print(zobj, end = "")
        print() """
        
        fitness = fitness_win(pairing,m, z_characters)
        if fitness >= 100:
            break
        if fitness > threshold:
            candidates.append(Candidate(pairing, fitness))
            threshold += 1
        else:
            threshold -= 1
        # Maintain list of candidates at predetermined length. Only the latest candidates, which should be the fittest, remain
        if len(candidates) <= 1000 and len(candidates) >= 100:
            if len(candidates) > 1000:
                candidates = sorted(candidates, key=lambda candidate: candidate.fitness, reverse=False)
                candidates = candidates[100:]
            # Further enhance the population by trial and error mutations
            pairing = mutate(candidates[0].pairing, m, int( math.ceil(len(x_indexes)* 0.02)), x_indexes, z_characters, fitness)
        else:
            # Randomly choose individuals initially
            if len(candidates) < 100:
                pairing = x_shuffle(pairing, m, x_indexes)
        # Shuffling will attempt to pick genes from candidates list instead of random chance, to create better individuals
        if candidates:
            print(f"{candidates[0]}, i={i + 2},level={level}")
    
    print(f"i={i + 2},level={level}")
    return pairing

# Process Rock-Paper-Scissors tournaments for levels 1 to 5
for level in range(1, 6):
    input_file_name = f"level7_{level}.in"
    output_file_name = f"level7_{level}.out"

    # Read input from the corresponding input file
    with open(input_file_name, "r") as input_file:
        n, m = map(int, input_file.readline().strip().split())  # Read n and m

        processed_pairings = []
        pairings = []

        # Read the counts for each tournament
        for i in range(n):
            pairings.append(input_file.readline())

        # Process pairings one by one and check if correct or not to proceed or keep trying
        for i in range(n):
            print(f"ii:{i}")
            pairings[i] = process_initial_pairing(i, m, pairings[i], level)
            processed_pairings.append(pairings[i])
        
    # Write results to the corresponding output file
    with open(output_file_name, "w") as output_file:
        for pairing in processed_pairings:
            output_file.write(pairing + "\n")
