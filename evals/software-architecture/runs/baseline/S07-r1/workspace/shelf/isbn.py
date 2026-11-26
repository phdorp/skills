"""ISBN-10 and ISBN-13 check digits."""


def valid(isbn):
    digits = isbn.replace("-", "").upper()
    if len(digits) == 10 and digits[:9].isdigit() and (digits[9].isdigit() or digits[9] == "X"):
        total = sum((10 - i) * int(d) for i, d in enumerate(digits[:9]))
        total += 10 if digits[9] == "X" else int(digits[9])
        return total % 11 == 0
    if len(digits) == 13 and digits.isdigit():
        total = sum(int(d) * (1 if i % 2 == 0 else 3) for i, d in enumerate(digits))
        return total % 10 == 0
    return False
