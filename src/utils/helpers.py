def calculate_accuracy(y_true, y_pred):
    correct_predictions = sum(y_t == y_p for y_t, y_p in zip(y_true, y_pred))
    return correct_predictions / len(y_true) if len(y_true) > 0 else 0.0

def calculate_confusion_matrix(y_true, y_pred):
    classes = set(y_true) | set(y_pred)
    matrix = {cls: {cls2: 0 for cls2 in classes} for cls in classes}
    
    for t, p in zip(y_true, y_pred):
        matrix[t][p] += 1
    
    return matrix

def handle_ambiguous_description(description):
    # Placeholder for handling ambiguous transaction descriptions
    return description.strip()  # Example: just stripping whitespace for now