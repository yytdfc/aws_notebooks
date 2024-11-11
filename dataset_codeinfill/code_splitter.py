import random
from code_analyzer import analyze_code

def tokenize_with_spaces(code_snippet, language='python'):
    tokens = analyze_code(code_snippet, language)
    return tokens

def split_code_randomly(code_snippet, language='python', min_middle_length=1, max_middle_length=None, split_middle=True):
    tokens = tokenize_with_spaces(code_snippet, language)
    
    if max_middle_length is None or max_middle_length > len(code_snippet):
        max_middle_length = len(code_snippet)
    
    min_middle_length = min(min_middle_length, max_middle_length)
    
    # print(f"Attempting to split with min_length={min_middle_length}, max_length={max_middle_length}")
    
    # Check if it's possible to create a split within the given constraints
    if max_middle_length < min_middle_length or max_middle_length > len(code_snippet):
        print("Cannot create a split within the given constraints. Returning entire code as middle.")
        return {'prefix': '', 'middle': code_snippet, 'suffix': ''}
    
    # Try random splits up to 10 times
    max_attempts = 100
    for attempt in range(max_attempts):
        # Choose random start position
        start = random.randint(0, len(tokens) - 2)
        # Choose random end position after start
        max_possible_length = min(len(tokens) - start, max_middle_length)
        if max_possible_length < min_middle_length:
            continue
            
        end = random.randint(start + 1, min(start + max_possible_length, len(tokens) - 1))
        middle = ''.join(tokens[start:end])
        if middle == "":
            continue

        prefix = ''.join(tokens[:start])
        suffix = ''.join(tokens[end:])

        if split_middle and len(tokens[start]) > 2:
            split_size = random.randint(0, len(tokens[start]) - 2)
            prefix = prefix + middle[:split_size]
            middle = middle[split_size:]

        return {'prefix': prefix, 'middle': middle, 'suffix': suffix}
    
    print(f"No suitable splits found after {max_attempts} attempts. Returning entire code as middle.")
    return {'prefix': '', 'middle': code_snippet, 'suffix': ''}


def view_test(split_result):
    """
    Display the split code with different colors for each part:
    - Prefix: Blue
    - Middle: Green
    - Suffix: Yellow
    """
    # ANSI color codes
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'
    
    # Print each part with its color
    print("\nSplit code visualization:")
    print(f"{BLUE}{split_result['prefix']}{RESET}", end='')
    print(f"{GREEN}{split_result['middle']}{RESET}", end='')
    print(f"{YELLOW}{split_result['suffix']}{RESET}")
    
    # Print legend
    print("\nColor legend:")
    print(f"{BLUE}Blue: Prefix{RESET}")
    print(f"{GREEN}Green: Middle{RESET}")
    print(f"{YELLOW}Yellow: Suffix{RESET}")

# Example usage
if __name__ == "__main__":
    python_code = """
def hello(name):
    print(f"Hello, {name}!")

hello("World")
"""
    
    result = split_code_randomly(python_code, 'python', min_middle_length=1, max_middle_length=128)
    
    # Display colored visualization
    view_test(result)

