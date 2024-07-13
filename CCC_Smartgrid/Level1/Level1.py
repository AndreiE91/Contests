def main():
    # Process levels 1 to 5
    for level in range(1, 6):
        input_file_name = f"level1_{level}.in"
        output_file_name = f"level1_{level}.out"

        # Read input from the corresponding input file
        with open(input_file_name, "r") as input_file:
            n = int(input_file.readline().strip())
            prices = []
            for _ in range(n):
                prices.append(int(input_file.readline().strip()))

        # get the index of the minimum price
        min_price_index = prices.index(min(prices))

        # Write results to the corresponding output file
        with open(output_file_name, "w") as output_file:
            output_file.write(str(min_price_index) + "\n")
            
if __name__ == "__main__":
    main()
