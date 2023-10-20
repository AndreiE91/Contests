import random
import math
    
class Coordinate:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __str__(self):
        return f"Coord: {self.row}, Fitness: {self.col}"

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

def replace_character(original_string, index, new_character):
    if 0 <= index < len(original_string):
        # Create a new string with the character replaced
        new_string = original_string[:index] + new_character + original_string[index + 1:]
        return new_string
    else:
        # Handle the case where the index is out of range
        return original_string  # or raise an error, return None, etc.

def process_coordinates(i, n, m, coordinates, mapp, level):
    letters = []
    for i in range(m):
        letter = mapp[coordinates[i].col][coordinates[i].row]
        letters.append(letter)
    
    print(f"i={i + 2},level={level}:{letters}")
    return letters

# Process Rock-Paper-Scissors tournaments for levels 1 to 5
for level in range(1, 6):
    input_file_name = f"level1_{level}.in"
    output_file_name = f"level1_{level}.out"

    # Read input from the corresponding input file
    with open(input_file_name, "r") as input_file:
        n = int(input_file.readline())  # Read n 

        results = []
        mapp = []
        coordinates = []

        # Read the lines of the map
        for i in range(n):
            mapp.append(input_file.readline())

        # Read the number of coordinates
        m = int(input_file.readline())  # Read m

         # Read the lines of the coordinates
        for i in range(m):
            read_str = input_file.readline()
            split_values = read_str.split(',')
            row = int(split_values[0])
            col = int(split_values[1])
            coordinates.append(Coordinate(row, col))

        # Process coordinates one by one
        letters = process_coordinates(i, n, m, coordinates, mapp, level)
        results.append(letters)
        
    # Write results to the corresponding output file
    with open(output_file_name, "w") as output_file:
        for letter in letters:
            output_file.write(letter + "\n")
