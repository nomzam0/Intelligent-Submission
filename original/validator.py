
def validateFormat(data):
    """
    Validates that the input data is not empty.
    
    Args:
        data: Input data to validate (string, list, dict, etc.)
    
    Returns:
        bool: True if data length > 0, False otherwise
    """
    if len(data) > 0:
        return True
    return False