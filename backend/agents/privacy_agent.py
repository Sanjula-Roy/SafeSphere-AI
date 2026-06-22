import re


def mask_sensitive_data(text):
    masked_text = text
    detected_items = []

    patterns = {
        "Aadhaar Number": r"\b\d{4}\s?\d{4}\s?\d{4}\b",
        "PAN Number": r"\b[A-Z]{5}[0-9]{4}[A-Z]\b",
        "Phone Number": r"\b\d{10}\b",
        "Email Address": r"\b[\w\.-]+@[\w\.-]+\.\w+\b",
        "UPI ID": r"\b[\w\.-]+@[\w]+\b"
    }

    for label, pattern in patterns.items():
        matches = re.findall(pattern, masked_text)

        for match in matches:
            detected_items.append({
                "type": label,
                "original": match,
                "masked": create_mask(match)
            })
            masked_text = masked_text.replace(match, create_mask(match))

    return {
        "agent": "Privacy & Security Agent",
        "detected_count": len(detected_items),
        "detected_items": detected_items,
        "masked_text": masked_text
    }


def create_mask(value):
    clean_value = str(value)

    if len(clean_value) <= 4:
        return "*" * len(clean_value)

    return clean_value[:3] + "*" * (len(clean_value) - 6) + clean_value[-3:]