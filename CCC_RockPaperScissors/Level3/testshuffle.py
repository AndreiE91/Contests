import random

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

# Example usage with a mask:
initial_string = "RRRRPRPSSSSS"
mask = "101100001101"
result = fill_and_shuffle(initial_string, mask)
print(result)
