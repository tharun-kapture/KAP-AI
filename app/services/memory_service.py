from langchain.memory import ConversationBufferMemory

class MemoryService:
    """
    Manages conversational memory by storing and retrieving user-assistant interactions.
    This service maintains a buffer of past messages to provide context for future exchanges.
    """

    def __init__(self):
        """
        Initializes the memory service with a conversation buffer.
        """
        self.memory_buffer = ConversationBufferMemory(memory_key="conversation_history")

    def add_message(self, role: str, message: str):
        """
        Stores a message in memory under the specified role.
        
        Args:
            role (str): Either "user" or "assistant" indicating who sent the message.
            message (str): The content of the message.
        
        Raises:
            ValueError: If the role is not "user" or "assistant".
        """
        try:
            if role not in ["user", "assistant"]:
                raise ValueError("Invalid role: Must be either 'user' or 'assistant'")
            
            print(f"Storing message - Role: {role}, Content: {message}") 
            
            if role == "user":
                self.memory_buffer.save_context({"input": message}, {"output": ""})
            else:  
                self.memory_buffer.save_context({"input": ""}, {"output": message})
        
        except Exception as e:
            print(f"Error storing message: {str(e)}")

    def get_conversation_history(self):
        """
        Retrieves the stored conversation history.
        
        Returns:
            dict: A dictionary containing the conversation history.
        """
        try:
            return self.memory_buffer.load_memory_variables({})
        except Exception as e:
            print(f"Error retrieving memory: {str(e)}")
            return {}

    def clear_conversation_history(self):
        """
        Clears all stored conversation history.
        """
        try:
            self.memory_buffer.clear()
            print("Conversation history cleared.")
        except Exception as e:
            print(f"Error clearing memory: {str(e)}")