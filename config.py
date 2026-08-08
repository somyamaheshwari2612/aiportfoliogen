import os

class Config:
    # Output Directory
    OUTPUT_FOLDER = os.path.join(os.getcwd(), 'output')
    
    # File Restrictions
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx'}
    MAX_FILE_SIZE_MB = 5
    MAX_CONTENT_LENGTH = MAX_FILE_SIZE_MB * 1024 * 1024
    
    # AI Configuration
    GEMINI_MODEL_NAME = "gemini-2.5-pro"
    
    # Themes
    THEMES = ['modern', 'minimal', 'glass', 'dark']
