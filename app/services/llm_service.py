from app.config import OPENAI_API_KEY, GEMINI_API_KEY
from app.services.memory_service import MemoryService
from typing import AsyncGenerator
from langchain_core.messages import AIMessageChunk
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

class LLMService:
    """
    Handles interaction with OpenAI GPT-4o, GPT-3.5 Turbo, or Google's Gemini 1.5 Flash,
    utilizing Langchain memory and streaming responses asynchronously.
    """

    SYSTEM_PROMPT = """
    You are an AI assistant responsible for structuring all responses in HTML to enhance clarity and readability. 
    Use appropriate tags for headings, paragraphs, lists, and formatting elements. Maintain a logical flow with well-organized sections, 
    avoiding unnecessary text and excessive styling.
    Follow these rules : 
    1. Paragraphs: Use <p> tags for every separate idea or explanation.  
    2. Line Breaks: Use <br> tags for minor separations where needed.  
    3. Lists: Use <ul> and <li> tags for any list-based information.  
    4. Headings: If required, use <h2> or <h3> for section titles.  
    5. Bold & Italic: Use <strong> for emphasis and <em> for slight emphasis.  
    6. Code Blocks: If providing code snippets, wrap them inside <pre><code> blocks.  
    7. Links: If suggesting references, format them as <a href='URL'>Text</a>.  
    8. Tables: If tabular data is needed, use <table><tr><td> elements.  

    Ensure that the response remains natural while following this structure. 
    Do not include unnecessary text outside the HTML tags. Do not enclose responses within triple backticks or 
    any unnecessary code fences. The response should be directly usable as HTML without extra formatting artifacts.
    """

    def __init__(self,memory):
        """Initialize the memory service without locking into a specific model."""
        self.memory_service = memory

    def _get_model(self, model_name: str):
        """
        Returns the LLM model instance based on user selection.

        Args:
            model_name (str): The LLM model to use ("gpt-4o", "gpt-3.5-turbo", or "gemini-1.5-flash").

        Returns:
            An instance of the selected LLM model.
        """
        model_name = model_name.lower()

        if model_name == "gpt-4o":
            return ChatOpenAI(model="gpt-4o", api_key=OPENAI_API_KEY)

        elif model_name == "gpt-3.5-turbo":
            return ChatOpenAI(model="gpt-3.5-turbo", api_key=OPENAI_API_KEY)

        elif model_name == "gemini-1.5-flash":
            return ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",
                google_api_key=GEMINI_API_KEY,
                streaming=True
            )

        else:
            raise ValueError("Invalid model name. Choose 'gpt-4o', 'gpt-3.5-turbo', or 'gemini-1.5-flash'.")

    async def generate_response(self, user_input: str, model_name: str) -> AsyncGenerator[str, None]:
        """
        Generates a streamed response using the selected LLM model with Langchain memory.

        Args:
            user_input (str): The user's input message.
            model_name (str): The LLM model to use.

        Yields:
            str: The generated response chunks as a stream.
        """
        try:
            model = self._get_model(model_name)
            self.memory_service.add_message("user", user_input)

            full_prompt = f"{self.SYSTEM_PROMPT}\n\nUser Query: {user_input}"
            full_response = ""

            async for chunk in model.astream(full_prompt):
                if isinstance(chunk, AIMessageChunk):
                    chunk = chunk.content  

                if chunk:
                    full_response += chunk
                    yield chunk 

            self.memory_service.add_message("assistant", full_response)
        except Exception as e:
            raise RuntimeError(f"Error generating response: {e}")
        
    
