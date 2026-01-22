import re
import os

INPUT_FILE = "/home/bj17300-049u/work/mediahal_wraper/log_print.txt"
OUTPUT_FILE = "/home/bj17300-049u/work/mediahal_wraper/extracted_log_print_patterns.txt"

def extract_patterns():
    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} does not exist.")
        return set()

    patterns = set()
    # Regex to match a function name followed by '(', where the arguments contain a double quote.
    # This filters for log-like calls e.g. LOG("msg") or func(arg, "str")
    # It matches the identifier, followed by (, and checks for a quote before the closing )
    regex = re.compile(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*\([^)]*"')

    print(f"Reading from {INPUT_FILE}...")
    with open(INPUT_FILE, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            # Find all matches in the line
            matches = regex.findall(line)
            for match in matches:
                # 'match' is just the captured group 1 (the function/macro name)
                # Filter out common control keywords if necessary, but user asked for "string immediately before ("
                # Let's keep it raw as requested, but maybe filter out empty strings if any (regex \w+ won't match empty).
                patterns.add(match)

    return patterns

def main():
    patterns = extract_patterns()
    
    if not patterns:
        print("No patterns found.")
        return

    print(f"Found {len(patterns)} unique patterns.")
    
    # Sort for better readability
    sorted_patterns = sorted(list(patterns))
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        for p in sorted_patterns:
            f.write(p + "\n")
            print(p)

    print(f"Results written to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
