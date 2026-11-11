# SRN: PES2UG24CS061
# Student: Andey Hemanth
# Lab 7: Fuzzing for Input Validation Bugs - Fixed Parser

def clean_pan(pan):
    """
    Removes spaces from a PAN and upper-cases it.
    Safely handles None, empty string, and non-string inputs.
    """
    if not isinstance(pan, str):
        return ""
    return pan.strip().replace(" ", "").upper()


def parse_amount(text):
    """
    Converts an amount such as 'Rs 12,50,000' into an int.
    Safely handles None, malformed strings, and non-numeric inputs.
    """
    if not isinstance(text, str):
        return 0
    cleaned = text.replace("Rs", "").replace("rs", "").replace(",", "").strip()
    try:
        return int(cleaned)
    except ValueError:
        return 0


def parse_tax_slab(line):
    """
    Parses 'LOW-HIGH:RATE' into a (low, high, rate) tuple.
    Safely handles None, missing delimiters, non-numeric values, and malformed inputs.
    """
    if not isinstance(line, str):
        return (0, 0, 0)
    try:
        if ":" not in line:
            return (0, 0, 0)
        limits, rate_str = line.split(":", 1)
        if "-" not in limits:
            return (0, 0, 0)
        low_str, high_str = limits.split("-", 1)
        return int(low_str.strip()), int(high_str.strip()), int(rate_str.strip())
    except Exception:
        return (0, 0, 0)


def main():
    print("==== Running clean_pan ====")
    value = input("Enter a PAN (e.g. abcde 1234f): ")
    print("Cleaned PAN:", clean_pan(value))

    print("\n==== Running parse_amount ====")
    value = input("Enter an amount (e.g. Rs 12,50,000): ")
    print("Amount in rupees:", parse_amount(value))

    print("\n==== Running parse_tax_slab ====")
    value = input("Enter a tax slab as LOW-HIGH:RATE (e.g. 250000-500000:5): ")
    print("Tax slab (low, high, rate):", parse_tax_slab(value))


if __name__ == "__main__":
    main()
