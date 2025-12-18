def load_data(file_path):
    import pandas as pd
    
    # Load the dataset from the specified file path
    data = pd.read_csv(file_path)
    
    # Perform any necessary preprocessing steps here
    # For example, handling missing values or formatting columns
    
    return data

def save_data(data, file_path):
    import pandas as pd
    
    # Save the processed dataset to the specified file path
    data.to_csv(file_path, index=False)