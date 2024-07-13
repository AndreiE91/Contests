def min_subarray(nums, n):
    if n > len(nums):
        return []

    min_sum = float('inf')
    min_start = 0

    window_sum = sum(nums[:n])

    for i in range(len(nums) - n + 1):
        if window_sum < min_sum:
            min_sum = window_sum
            min_start = i

        if i + n < len(nums):
            window_sum = window_sum - nums[i] + nums[i + n]

    return nums[min_start:min_start + n]

def main():
    # Process levels 1 to 5
    for level in range(1, 6):
        input_file_name = f"level2_{level}.in"
        output_file_name = f"level2_{level}.out"

        # Read input from the corresponding input file
        with open(input_file_name, "r") as input_file:
            n = int(input_file.readline().strip())
            prices = []
            for _ in range(n):
                prices.append(int(input_file.readline().strip()))
                
            m = int(input_file.readline().strip())
            task_completionTimes = []
            # create a key-value pair for each task(taskId completionTime)
            for _ in range(m):
                task_completionTimes.append(input_file.readline().strip().split(" "))

            # find minimum contiguous subarray of prices, where the length of the subarray is equal to the completion time of the task
            for task_completionTimePair in task_completionTimes:
                taskId = task_completionTimePair[0]
                completionTime = int(task_completionTimePair[1])
                min_price_index = min_subarray(prices, completionTime).index(min(min_subarray(prices, completionTime)))
                prices[min_price_index] = float('inf')
                
            

        # Write results to the corresponding output file
        with open(output_file_name, "w") as output_file:
            output_file.write(str(min_price_index) + "\n")
            
if __name__ == "__main__":
    main()
