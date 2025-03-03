# apisimple.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Union, Dict
from agentSimple import parse_transaction_prompt

app = FastAPI()


class PromptRequest(BaseModel):
    prompt: str


class ParseResponse(BaseModel):
    done: bool
    messages: list
    parsed: Union[Dict[str, str], str, None]


@app.post("/agent", response_model=ParseResponse)
def parse_agent(req: PromptRequest):
    """
    POST /agent
    Body: { "prompt": "Please send 0.000001 BTC to 0x1234..." }

    Returns:
    {
      "done": true,
      "messages": [...],
      "parsed": { "amount": "...", "currency":"BTC", "recipient":"..." }
    }
    """
    prompt = req.prompt
    messages = [prompt]

    result = parse_transaction_prompt(prompt)
    if isinstance(result, str):
        # It's an error
        messages.append(result)
        return {"done": True, "messages": messages, "parsed": None}

    # success
    messages.append(f"Parsed => {result}")
    return {"done": True, "messages": messages, "parsed": result}
