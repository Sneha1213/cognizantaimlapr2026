#read env from dotenv 
import os
from dotenv import load_dotenv
load_dotenv()

class config:
    def __init__(self):
        self.url=os.getenv("url")