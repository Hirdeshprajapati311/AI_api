import os
from dotenv import load_dotenv
from google import genai

load_dotenv()



class GeminiServices:
  def __init__(self):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
      raise ValueError("GEMINI_API_KEY is not set in the environment variables.")
    self.client = genai.Client()

  def generate_text(self,prompt:str,model:str="gemini-2.5-flash")->str:
    """Gemini Response for one question"""
    try:
      response = self.client.models.generate_content(
        model=model,
        contents=prompt,
      )
      return response.text
    except Exception as e:
      raise RuntimeError(f"An error occured while calling Gemini API: {str(e)}") from e

  async def genearate_text_async(self,prompt:str,model:str="gemini-2.5-flash")->str:
      """Gemini Response for multiple questions""" 
      try:
        response = await self.client.aio.models.generate_content(model=model,contents=prompt,)
        return response.text
      except Exception as e:
        raise RuntimeError(f"An error occured while calling Gemini API: {str(e)}") from e