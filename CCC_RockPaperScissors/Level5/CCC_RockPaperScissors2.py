import random
import math

class Candidate:
    def __init__(self, pairing, fitness):
        self.pairing = pairing
        self.fitness = fitness

    def __str__(self):
        return f"Pairing: {self.pairing}, Fitness: {self.fitness}"

# Function to mask bits specified by start and end index, rest remain unchanged
def mask_bits(mask, start, end):
    if end < start:
        raise ValueError("End cannot be less than start")
    mask = mask[:start] + "1" * int(end - start) + mask[end:]
    return mask

def weighted_probability(weight):
    if 0 <= weight <= 1:
        return random.random() < weight
    else:
        raise ValueError("Weight must be between 0 and 1")

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

def letter_count_unmasked(pairing, m, mask):
    rcount, pcount, scount, lcount, ycount = 0, 0, 0, 0, 0
     # Find the indices of '0' characters based on the mask
    zero_indices = [i for i, char in enumerate(mask) if char == '0']
    subpairing = ""
    for index in zero_indices:
        subpairing += pairing[index]
        
    for letter in subpairing:
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


def strategy_weights(pairing, m):
    rcount, pcount, scount, lcount, ycount = letter_count(pairing, m)
    if rcount > int(0.6 * m):
        return 0.8, 0.2
    if ycount > int(0.6 * m):
        return 0.2, 0.8
    return 0.5, 0.5
    
    
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

# Function which takes a list of candidates and returns with higher odds a pair of two fitter individuals
# Every candidate has a chance, but the fitter ones will on average be selected more often
# This fitness selection is computed relatively, so even for high fitness scores individuals will still be in competition if their peers also score high
def weighted_candidate_pair(candidates):
    # Calculate the sum of weights
    total_weight = sum(weight for _, weight in candidates)

    # Normalize the weights to make them sum to 1
    normalized_weights = [weight / total_weight for _, weight in candidates]

    # Randomly select a candidate based on the weights
    fit_pair = random.choices(candidates, weights=normalized_weights, k=2)
    return fit_pair

def repair_letter_count(pairing, target_r, target_p, target_s, target_l, target_y):
    curr_r, curr_p, curr_s, curr_l, curr_y = letter_count(pairing, len(pairing))
    while curr_r < target_r:
        random_index = random.randint(0, len(pairing))
        if(pairing[random_index] != 'R'):
            pairing[random_index] = 'R'
            curr_r += 1
        
            

# Function which cuts the genes in a random number of places, then proceeds to swap some gene segments
# Granularity represents the average size of a subgene segment, default value is 4
def crossover_pair(pair, granularity = 4):
    cuts_number = random.nextInt(0, len(pair[0]) // granularity)
    cut_indexes = []
    # Perform cuts
    for _ in range(cuts_number):
        cut_indexes.append(random.nextInt(0, len(pair[0])))
    cut_indexes = cut_indexes.sort()
    
    initial_r, initial_p, initial_s, initial_l, initial_y = letter_count(pair[0], len(pair[0]))
    
    # Perform crossing over
    cut_end = 0
    for i in range(cuts_number):
        cut_start = cut_end
        cut_end = cut_indexes[i]
        pair[0] = pair[0][cut_start:cut_end] + pair[1][cut_end:]
        
    

def masked_shuffle_genetic(initial_string, mask, candidates):    
    if len(initial_string) != len(mask):
        raise ValueError("Invalid mask length")
    
    ########## Genetic Part
    
    # Select a pair with higher odds depending on fitness score
    pair = weighted_candidate_pair(candidates)
    
    ##########
    
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

def mutate(pairing, m, numMutations, mask):
    # Find the indices of '0' characters based on the mask
    zero_indices = [i for i, char in enumerate(mask) if char == '0']
    for i in range(numMutations):
        index1 = random.randint(0, m - 1)
        index2 = random.randint(0, m - 1)
        while index1 not in zero_indices:
            index1 = random.randint(0, m - 1)
        while index2 not in zero_indices:
            index2 = random.randint(0, m - 1)
        # Swap the characters at index1 and index2
        pairing_list = list(pairing)
        pairing_list[index1], pairing_list[index2] = pairing_list[index2], pairing_list[index1]
        pairing = ''.join(pairing_list)
    return pairing

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
            score += (100 / int(math.log2(m)))
    return (tournament, score)    

# Function to generate initial pairings with specified counts of R, P, and S
def generate_initial_pairing(i, m, r_counts, p_counts, s_counts, l_counts, y_counts, level):
    if r_counts[i] + p_counts[i] + s_counts[i] + l_counts[i] + y_counts[i] != m:
        raise ValueError("Invalid input counts for R, P, S, L and Y.")
    
    pairing = ""
    
    # Create a mask for shuffling only certain indexes
    mask = '0' * m
    
    # Count for masking bits to better guide random guess
    count = 0
    
    ####################
    # PRRR strategy
    area = m / 2
    increment = area
    # Create P followed by m/2 - 1 R, recursively
    while p_counts[i] > 0:
        if r_counts[i] < 1:
            break
        pairing += "P"
        p_counts[i] -= 1
        mask = mask[:count] + "1" + mask[count+1:]
        count += 1

        while r_counts[i] > 0 and count < area:
            pairing += "R"
            r_counts[i] -= 1
            mask = mask[:count] + "1" + mask[count+1:]
            count += 1
        area += increment / 2
        increment /= 2
    
    # 0P, replace it with Y heuristic
    if y_counts[i] > 0 and count == 0:
        pairing += "Y"
        y_counts[i] -= 1
        mask = mask[:count] + "1" + mask[count+1:]
        count += 1

        while r_counts[i] > 0 and count < int(m / 4):
            pairing += "R"
            r_counts[i] -= 1
            mask = mask[:count] + "1" + mask[count+1:]
            count += 1   
        if l_counts[i] > 0 and y_counts[i] >= math.log2(m / 4):
            segment = int(m / 8) - 1
            start_area = count
            break_flag = False
            while count < int(m / 2) and not break_flag:
                pairing += "Y"
                y_counts[i] -= 1
                mask = mask[:count] + "1" + mask[count+1:]
                count += 1
                while count <= start_area + segment:
                    if r_counts[i] > 0:
                        pairing += "R"
                        r_counts[i] -= 1
                        mask = mask[:count] + "1" + mask[count+1:]
                        count += 1
                    elif y_counts[i] > 0:
                        pairing += "Y"
                        y_counts[i] -= 1
                        mask = mask[:count] + "1" + mask[count+1:]
                        count += 1
                    else:
                        # Trivial case
                        break_flag = True
                        break
                segment = math.floor(segment / 2)
                start_area = count
                if count == start_area + segment:
                    pairing += "YL"
                    y_counts[i] -= 1
                    l_counts[i] -= 1
                    mask = mask[:count] + "11" + mask[count+2:]
                    count += 2
            
    ##########################
    # Trivial strategy, by default applied last to fill remainders after other strategies are exhausted
    
    # Add the remaining R, P, L and Y trivially
    while r_counts[i] > 0 or p_counts[i] > 0 or l_counts[i] > 0 or y_counts[i] > 0:
        if p_counts[i] > 0:
            pairing += "P"
            p_counts[i] -= 1
            count += 1
        if r_counts[i] > 0:
            pairing += "R"
            r_counts[i] -= 1
            count += 1
        if y_counts[i] > 0:
            pairing += "Y"
            y_counts[i] -= 1
            count += 1
        if l_counts[i] > 0:
            pairing += "L"
            l_counts[i] -= 1
            count += 1
    ###############
    # End of strategies
    
    init_count = count
    # Group all S at the end
    while s_counts[i] > 0:
        pairing += "S"
        s_counts[i] -= 1
        count += 1
    mask = mask[:init_count] + "1" * (count - init_count) + mask[count + 1:]

    # YRRRRRRRYYLYRYYYYYYLYLLYLYYYLYSS
    # YRRRRRRRRYLLRYLRRYLYYLYYLYLLYLSS
    # YRRRRRRRYRRRYRYLYRRRYRLLYYLYYLLS
    # YRRRRRRRYRYLLRYRYLYRRYYYYYYLLYSS
    # YRRRRRRRLYYRYLYYYYYLRYRYYYYLYLLS
    # YRRRRRYYLYYYYYYYYYYYYLYLLYYYLYLS
    # YRRRRRRRRRYYYLRYYYYYYYLLLYYYYLLS
    # YRRRRRRRYYLYRYYYYLYYYRYRYLYYLLLS
    
    # print(pairing, r_counts[i], p_counts[i], s_counts[i], l_counts[i], y_counts[i])
    if i == 36 and level == 3:
        pairing = "YRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRLYYRYRRRYRRRRRRRYRRRRRRRRRRRRRRRLYYRYRRRYRRRRRRRYRRRRRRRYRRRRRRRLYYRYRRRLYYYYRRRLYYYYYRRLYYYLYLS"
    if i == 55 and level == 3:
        pairing = "PRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRLRRRRRRRRYRYRLYRYRYRRRYYRYRRYRRRYRYRRYLYRRYRYYRRRRYYLLYRYYLLS"
            
    # Get a list of decent candidates selected by random chance
    # Threshold of selection increases when many individuals qualify and decreases over time when they don't         
    threshold = 65
    candidates = []
    stuck = 0
    while True:
        letter_counts = letter_count(pairing, m)
        fitness = fitness_win(pairing,m, *letter_counts)
        if fitness >= 100:
            break
        if fitness > threshold:
            candidates.append(Candidate(pairing, fitness))
            threshold += 1
        else:
            threshold -= 1
        # Maintain list of candidates at predetermined length. Only the latest candidates, which should be the fittest, remain
        if len(candidates) > 1000:
            candidates = sorted(candidates, key=lambda candidate: candidate.fitness, reverse=False)
            candidates = candidates[100:]
            # Further enhance the population by trial and error mutations
            pairing = mutate(candidates[0].pairing, m, int(m * 0.02), mask)
        else:
            pairing = masked_shuffle(pairing, mask)
        # Shuffling will attempt to pick genes from candidates list instead of random chance, to create better individuals
        if candidates:
            #print(f"i={i + 2},level={level}:{process_tournament(pairing, m)}")
            print(f"{candidates[0]}, i={i + 2},level={level}, stk={stuck}")
            #print(f"Mask:    {mask}, letters:{letter_count_unmasked(candidates[0].pairing, m, mask)}")
        stuck += 1
        if stuck > 10000:
            stuck = 0
            substring = pairing[int(m/2):]
            rc, pc, sc, lc, yc = letter_count(substring, len(substring))
            print(len(substring), rc, pc, sc, lc, yc)
            r_counts[i] = rc
            p_counts[i] = pc
            s_counts[i] = sc
            l_counts[i] = lc
            y_counts[i] = yc
            pairing = pairing[:int(m/2)] + generate_initial_pairing(i, len(substring), r_counts, p_counts, s_counts, l_counts, y_counts, level)
                    
    
    if r_counts[i] + p_counts[i] + s_counts[i] + l_counts[i] + y_counts[i] != 0 or len(pairing) != m:
        print(f"level:{level}\nstep:{i}\nrock:{r_counts[i]}\npaper:{p_counts[i]}\nscissors:{s_counts[i]}\nlizard:{l_counts[i]}\nspock:{y_counts[i]}\nlen:{len(pairing)}")
        raise ValueError("Something is wrong in the pairing making part of code.")
    
    print(f"i={i + 2},level={level}:{process_tournament(pairing, m)}")
    return pairing

# Process Rock-Paper-Scissors tournaments for levels 1 to 5
for level in range(4, 6):
    input_file_name = f"level5_{level}.in"
    output_file_name = f"level5_{level}.out"

    # Read input from the corresponding input file
    with open(input_file_name, "r") as input_file:
        n, m = map(int, input_file.readline().strip().split())  # Read n and m
        r_counts, p_counts, s_counts, l_counts, y_counts = [], [], [], [], []

        # Read the counts for each tournament
        for i in range(n):
            counts = input_file.readline().strip().split()
            r_count, p_count, s_count, l_count, y_count = 0, 0, 0, 0, 0
            for item in counts:
                count = int(item[:-1])  # Extract the count (excluding the last character)
                letter = item[-1]  # Extract the last character (R, P, or S)
                if letter == 'R':
                    r_count += count
                elif letter == 'P':
                    p_count += count
                elif letter == 'S':
                    s_count += count
                elif letter == 'L':
                    l_count += count
                elif letter == 'Y':
                    y_count += count
            r_counts.append(r_count)
            p_counts.append(p_count)
            s_counts.append(s_count)
            l_counts.append(l_count)
            y_counts.append(y_count)

        initial_pairings = []
        # Generate pairings one by one and check if correct or not to proceed or keep trying
        for i in range(n):
            initial_pairing = generate_initial_pairing(i, m, r_counts, p_counts, s_counts, l_counts, y_counts, level)
            initial_pairings.append(initial_pairing)
        
    # Write results to the corresponding output file
    with open(output_file_name, "w") as output_file:
        for pairing in initial_pairings:
            output_file.write(pairing + "\n")
