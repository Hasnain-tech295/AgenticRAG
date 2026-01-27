
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Dict, Any, Optional
from pathlib import Path
import json
from datetime import datetime
from tavily import TavilyClient

load_dotenv()