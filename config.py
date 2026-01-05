"""
Configuration - reads from .env file
"""
import os
from dotenv import load_dotenv

load_dotenv()

# WordPress
WORDPRESS_URL = os.getenv("WORDPRESS_URL", "https://lookizm.com")
WORDPRESS_USERNAME = os.getenv("WORDPRESS_USERNAME", "")
WORDPRESS_APP_PASSWORD = os.getenv("WORDPRESS_APP_PASSWORD", "")

# Ollama (Local)
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "unclemusclez/thedrummer-smegmma-v1:8b")  # 8B model - better quality

# Blog Settings
BLOG_CATEGORY_ID = int(os.getenv("BLOG_CATEGORY_ID", "1"))
AUTHOR_ID = int(os.getenv("AUTHOR_ID", "1"))
POST_STATUS = os.getenv("POST_STATUS", "publish")

# Content Generation
MIN_WORD_COUNT = int(os.getenv("MIN_WORD_COUNT", "2500"))
MAX_WORD_COUNT = int(os.getenv("MAX_WORD_COUNT", "3000"))
POSTS_PER_DAY = int(os.getenv("POSTS_PER_DAY", "1"))
POST_TIME = os.getenv("POST_TIME", "10:00")

# Image Services
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY", "N6yGErTimuX5C78O77AiC6SQTT01d6bDmRD1gnAFYbAD1DZOR377HNeI")
