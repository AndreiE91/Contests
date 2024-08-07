import random
import math
import numpy as np
import networkx as nx

class CoordinatePair:
    def __init__(self, col1, row1, col2, row2):
        self.col1 = col1
        self.row1 = row1
        self.col2 = col2
        self.row2 = row2

    def __str__(self):
        return f"Coord: {self.col1}, {self.row1}, {self.col2}, {self.row2}"

def process_sameland(n, coordinates, map_matrix, level):
    # Create a mapping from coordinates to nodes
    coord_to_node = {(r, c): (r, c) for r in range(n) for c in range(n)}
    responses = []

    # Create a graph
    graph = nx.Graph()

    # Add nodes to the graph with 'position' attribute
    for r in range(n):
        for c in range(n):
            graph.add_node((r, c), position=(r, c))  # Add nodes with 'position' attribute

    # Add edges based on adjacency (up, down, left, right) and the content of the map_matrix
    for r in range(n):
        for c in range(n):
            if map_matrix[r][c] == "L":
                neighbors = [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]
                for neighbor in neighbors:
                    if (
                        0 <= neighbor[0] < n
                        and 0 <= neighbor[1] < n
                        and map_matrix[neighbor[0]][neighbor[1]] == "L"
                    ):
                        graph.add_edge((r, c), neighbor)

    for j, coordinate in enumerate(coordinates):
        source_coord = (coordinate.col1, coordinate.row1)
        target_coord = (coordinate.col2, coordinate.row2)

        source_node = coord_to_node.get(source_coord)
        target_node = coord_to_node.get(target_coord)

        if source_node is None or target_node is None:
            print("Node is none")

        response = "DIFFERENT"  # Assume different until proven otherwise
        # Check for a path using DFS
        if nx.has_path(graph, source_node, target_node):
            response = "SAME"

        responses.append(response)
        print(f"i={j + 2}, level={level}: {response}")
    return responses

def main():
    # Process Islands for levels 1 to 5
    for level in range(1, 6):  # Adjust the range to match the desired levels
        input_file_name = f"level2_{level}.in"
        output_file_name = f"level2_{level}.out"

        # Read input from the corresponding input file
        with open(input_file_name, "r") as input_file:
            n = int(input_file.readline())  # Read n

            results = []
            coordinates = []

            mapp = []
            # Read the lines of the map
            for _ in range(n):
                line = input_file.readline().strip()  # Remove leading/trailing whitespace
                mapp.append(list(line))  # Convert the string to a list of characters

            # Read the number of coordinates
            m = int(input_file.readline())  # Read m

            # Read the lines of the coordinates
            for _ in range(m):
                read_str = input_file.readline()
                split_values = read_str.split(' ')
                coord1 = split_values[0]
                coord2 = split_values[1]
                col1, row1 = coord1.split(',')
                col2, row2 = coord2.split(',')
                coordinate = CoordinatePair(int(row1), int(col1), int(row2), int(col2))
                coordinates.append(coordinate)

        # Process coordinates one by one
        responses = process_sameland(n, coordinates, mapp, level)

        # Write results to the corresponding output file
        with open(output_file_name, "w") as output_file:
            for response in responses:
                output_file.write(response + "\n")

if __name__ == "__main__":
    main()
