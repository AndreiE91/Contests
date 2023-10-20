import random

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

def combine_individuals(individual1, individual2, desired_counts):
    # Check if the individuals are of the same length
    if len(individual1) != len(individual2):
        raise ValueError("Individuals must have the same length.")

    offspring = []

    # Choose crossover point
    crossover_point = random.randint(0, len(individual1))

    # Copy substrings from parents
    offspring.extend(individual1[:crossover_point])
    offspring.extend(individual2[crossover_point:])

    # Count the letters in the offspring
    offspring_counts = {}
    for letter in offspring:
        if letter not in offspring_counts:
            offspring_counts[letter] = 0
        offspring_counts[letter] += 1

    # Ensure counts match the desired counts
    for letter, count in desired_counts.items():
        while offspring_counts.get(letter, 0) < count:
            # If a letter is underrepresented, randomly insert it
            index = random.randint(0, len(offspring))
            offspring.insert(index, letter)
            if letter not in offspring_counts:
                offspring_counts[letter] = 1
            else:
                offspring_counts[letter] += 1

    return "".join(offspring)

# Example usage:
individual1 = "RPSLYR"
individual2 = "YSLRPP"
desired_counts = {'R': 2, 'P': 2, 'S': 2, 'L': 2, 'Y': 2}

offspring = combine_individuals(individual1, individual2, desired_counts)
print(offspring)
print(letter_count(offspring, 6))