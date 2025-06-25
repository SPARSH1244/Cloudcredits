def recommend_algorithm(text, purpose="personal", speed_priority=False, key_type="symmetric"):
    """
    Simple rule-based recommender for encryption algorithm.
    """

    length = len(text)

    if "demo" in purpose.lower() or "learning" in purpose.lower():
        return "Caesar Cipher"

    if length < 50 and speed_priority:
        return "Fernet"

    if key_type == "asymmetric":
        return "RSA"

    if key_type == "symmetric" and length >= 1000:
        return "AES-256 (CBC)"

    return "AES-256"
