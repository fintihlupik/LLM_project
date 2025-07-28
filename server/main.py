from unittest import result
from fastapi import FastAPI, HTTPException
from marshmallow import pprint
from pydantic import BaseModel # Import BaseModel for request and response validation
from server.groq_wrapper import generate_response
from typing import Literal, Optional
#from server.agents import marketing_agent, finance_agent
from server.agents.marketing_agent import marketing_agent
from server.agents.finance_agent import run_agent
from server.tools.get_market_news import get_market_news
from server.tools.get_market_yahoo import get_market_yahoo
import json
from server.tools.generate_image import generate_image  #generate image




app = FastAPI(title="Groq LangChain API", version="1.0.0")

class ResponseOutput(BaseModel):
    output: str

class ContentRequest(BaseModel):
    prompt: str                 
    audience: Optional[str] = None
    platform: Optional[str] = None
    region: Optional[str] = None
    model: Optional[Literal["llama", "turbo"]] = "llama"  # Por defecto llama

@app.post("/generate", response_model=ResponseOutput)
async def generate(data: ContentRequest):
    try:
        result = await generate_response(data)
        return ResponseOutput(output=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"message": "Groq LangChain API está funcionando"}

@app.post("/agent/marketing", response_model=ResponseOutput)
async def agent_generate(data: ContentRequest):
    try:
        input_data = data.model_dump() # Convert Pydantic model to dict
        print(f"[DEBUG] INPUT MODEL DUMP: {input_data}")
        json_string = json.dumps(input_data)  # Convert dict to JSON string
        print(f"[DEBUG] JSON STRING: {json_string}")
        result = marketing_agent.invoke({"input": json.dumps(input_data)}) # LangChain requiere strings, así que después se convierte a JSON
        
        if isinstance(result, dict) and "output" in result:
            content = result["output"]
        elif isinstance(result, dict) and "input" in result:
            content = result["input"]
        else:
            content = str(result)
            
        return ResponseOutput(output=content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
from langchain.agents import AgentExecutor

@app.post("/agent/finance", response_model=ResponseOutput)
async def finance_agent_generate(data: ContentRequest):
    try:
        input_data = data.model_dump()  # Convert Pydantic model to dict
        
        print(f"[DEBUG] INPUT MODEL DUMP: {input_data}")
        json_string = json.dumps(input_data)  # Convert dict to JSON string
        print(f"[DEBUG] JSON STRING: {json_string}")
        #result = finance_agent.invoke({"input": json_string})  # LangChain requiere strings, así que después se convierte a JSON
        result = run_agent(json_string)
        
    
        if isinstance(result, dict) and "output" in result:
            content = result["output"]
        elif isinstance(result, dict) and "input" in result:
            content = result["input"]
        else:
            content = str(result)
            
        return ResponseOutput(output=content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




class MarketNewsRequest(BaseModel):
    ticker: str

@app.post("/market-news", response_model=ResponseOutput)
async def get_yahoo_market_news(data: MarketNewsRequest):
    """
    Endpoint para obtener noticias financieras de Yahoo Finance directamente.
    
    Acepta un ticker directo como 'AAPL', 'TSLA', 'BTC-USD', '^GSPC' (S&P 500), '^DJI' (Dow Jones), etc.
    """
    try:
        # Llamamos directamente a la función get_market_news con el ticker
        result = get_market_yahoo(data.ticker)
        return ResponseOutput(output=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# crear imagen
class ImageRequest(BaseModel):
    prompt: str

@app.post("/generate-image", response_model=ResponseOutput)
async def generate_image_endpoint(data: ImageRequest):
    try:
        image_b64 = generate_image(data.prompt)
        return ResponseOutput(output=image_b64)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
