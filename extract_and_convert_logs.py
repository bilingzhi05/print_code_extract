import re
import os
# time rg -i -f print_regex_patterns_0114.txt '/home/amlogic/RAG/clean_log/clean_BJ-IPTV-26084-h264-花屏-resolved.log' > filterIPTV-26084_log.txt
INPUT_FILE = "/home/bj17300-049u/work/mediahal_wraper/20260122_103354_media_hal_logset/20260122_103354_media_hal_logset_suspicious_analysis.txt"
EXTRACTED_FILE = "/home/bj17300-049u/work/mediahal_wraper/20260122_103354_media_hal_logset/20260122_103354_media_hal_logset_extracted_contents.txt"
REGEX_FILE = "/home/bj17300-049u/work/mediahal_wraper/20260122_103354_media_hal_logset/20260122_103354_media_hal_logset_extracted_contents_re.txt"

PLACEHOLDER_MAP = {
    # signed integers
    "%lld": r"(-?\d+)",          # long long
    "%lli": r"(-?\d+)",          # long long
    "%ld":  r"(-?\d+)",          # long
    "%li":  r"(-?\d+)",          # long
    "%hd":  r"(-?\d+)",          # short
    "%hi":  r"(-?\d+)",          # short
    "%hhd": r"(-?\d+)",          # char/byte
    "%hhi": r"(-?\d+)",          # char/byte
    "%d":   r"(-?\d+)",          # int
    "%i":   r"-?\d+",          # int

    # unsigned integers
    "%llu": r"(\d+)",            # unsigned long long
    "%lu":  r"(\d+)",            # unsigned long
    "%hu":  r"(\d+)",            # unsigned short
    "%hhu": r"(\d+)",            # unsigned char
    "%zu":  r"(\d+)",            # size_t
    "%u":   r"(\d+)",            # unsigned int

    # hex
    "%llx": r"([0-9a-fA-F]+)",   # unsigned long long hex
    "%llX": r"([0-9a-fA-F]+)",
    "%lx":  r"([0-9a-fA-F]+)",   # unsigned long hex
    "%lX":  r"([0-9a-fA-F]+)",
    "%hx":  r"([0-9a-fA-F]+)",   # unsigned short hex
    "%hX":  r"([0-9a-fA-F]+)",
    "%hhx": r"([0-9a-fA-F]+)",   # unsigned char hex
    "%hhX": r"([0-9a-fA-F]+)",
    "%x":   r"([0-9a-fA-F]+)",   # unsigned int hex
    "%X":   r"([0-9a-fA-F]+)",

    # float / double
    "%lf":  r"(-?\d+(?:\.\d+)?)",       # double
    "%f":   r"(-?\d+(?:\.\d+)?)",       # float
    "%e":   r"-?\d+(?:\.\d+)?[eE]-?\d+",  # scientific
    "%E":   r"-?\d+(?:\.\d+)?[eE]-?\d+",  # scientific
    "%g":   r"(-?\d+(?:\.\d+)?)",       # auto format
    "%G":   r"(-?\d+(?:\.\d+)?)",

    # string / char
    "%s":   r"(.+?)",             # string (no spaces/separators)
    "%c":   r".",                       # single char
    "%p":   r"(0x[0-9a-fA-F]+|[0-9]+)",          # pointer

    # literal percent
    "%%":   r"%",                       # escaped percent
}

def extract_content():
    print(f"Extracting content from {INPUT_FILE}...")
    extracted_lines = []
    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} does not exist.")
        return []

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith("Content:"):
                # Extract text after "Content:" and strip whitespace
                content = line[len("Content:"):].strip()
                extracted_lines.append(content)
    
    # Write extracted content to file
    with open(EXTRACTED_FILE, 'w', encoding='utf-8') as f:
        for line in extracted_lines:
            f.write(line + "\n")
    
    print(f"Extracted {len(extracted_lines)} lines to {EXTRACTED_FILE}")
    return extracted_lines

def generate_regex(lines):
    print(f"Generating regex patterns to {REGEX_FILE}...")
    
    # Sort keys by length descending to handle longer placeholders first
    # e.g. %lld should be replaced before %d
    sorted_keys = sorted(PLACEHOLDER_MAP.keys(), key=len, reverse=True)
    
    regex_lines = []
    for line in lines:
        current_line = line
        
        # We need to escape special regex characters in the static parts of the string
        # BUT we must not escape the placeholders themselves before replacing them.
        # Strategy:
        # 1. Split the string by placeholders? Hard because multiple types.
        # 2. Iterate through string and replace placeholders with a unique temporary marker?
        # 3. Or just replace placeholders with the regex directly, assuming the placeholders
        #    don't contain special regex chars (they start with %).
        #    But wait, if the original string has "Error(s)", we want "Error\(s\)".
        #    If we do simple replacement, "Error(s) %d" -> "Error(s) -?\d+".
        #    This is not a valid regex for the original string if parens are meant to be literal.
        
        # However, the user simply asked to "replace %d %s with regex expression".
        # They didn't explicitly ask to escape the rest.
        # But if the goal is to make a regex that matches the log, escaping is usually implied.
        # Let's check the user request: "replace %d %s as regex expression... write to new txt file"
        # I will do direct replacement as requested, but I will ALSO escape regex special chars
        # in the non-placeholder parts to make it a valid regex pattern for the log line.
        
        # Implementation:
        # We can use re.split with a pattern that matches ANY of the placeholders.
        
        # Construct a big regex for all placeholders
        # Escape keys just in case (though % is safe)
        pattern_str = "|".join(map(re.escape, sorted_keys))
        token_pattern = re.compile(f"({pattern_str})")
        
        parts = token_pattern.split(current_line)
        # parts will be like ['Static text ', '%d', ' static text ', '%s', '']
        
        final_regex_parts = []
        for part in parts:
            if part in PLACEHOLDER_MAP:
                # It's a placeholder, replace with regex
                final_regex_parts.append(PLACEHOLDER_MAP[part])
            else:
                # It's static text, escape it
                final_regex_parts.append(re.escape(part))
        
        regex_line = "".join(final_regex_parts)
        # Add start/end anchors if appropriate, or just the pattern?
        # User didn't specify, but usually full line match is good.
        # For now just the pattern content as requested.
        regex_lines.append(regex_line)

    with open(REGEX_FILE, 'w', encoding='utf-8') as f:
        for line in regex_lines:
            f.write(line + "\n")
            
    print(f"Generated {len(regex_lines)} regex patterns to {REGEX_FILE}")

def main():
    lines = extract_content()
    if lines:
        generate_regex(lines)

if __name__ == "__main__":
    main()
