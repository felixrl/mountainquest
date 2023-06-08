# SORTING MODULE
# MountainQuest
# Felix Liu

# VERSION HISTORY
# 6.6.2023 - created, added generic merge sort implementation

def merge_sort(val_list, comparison_strategy):
    if len(val_list) < 2: # Termination condition: lists of size one or less get returned for sorting
        return val_list
    else: # Recursively sort right and left half before merging together
        middle = len(val_list) // 2
        right_half = merge_sort(val_list[middle:len(val_list)], comparison_strategy) # Sort right half
        left_half = merge_sort(val_list[0:middle], comparison_strategy) # Sort left half
        return merge(left_half, right_half, comparison_strategy) # Merge lists and return result using the designated strategy function
def merge(left, right, comparison_strategy):
        result = []
        # While both lists have elements, perform sort comparisons and append to result 
        while len(left) > 0 and len(right) > 0:
            if comparison_strategy(left[0], right[0]): # Left is smaller or equal (first or redundant in sorted order) COMPARE WITH STRATEGY
                result.append(left[0])
                left.pop(0) # Remove appended element from left list
            else: # Right is smaller in sorted order
                result.append(right[0])
                right.pop(0) # Remove appended element from right list
        # Leftover elements, simply append all remaining elements into the result
        while len(left) > 0:
            result.append(left[0])
            left.pop(0)
        while len(right) > 0:
            result.append(right[0])
            right.pop(0) 
        return result # Return merged result

def compare_alphabetically(left, right):
    if left <= right:
        return True
    return False
