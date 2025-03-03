# agentSimple.py
import os
from dotenv import load_dotenv
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI

load_dotenv()  # Load environment variables (like OPENAI_API_KEY)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
print("[DEBUG agentSimple] OPENAI_API_KEY:",
      OPENAI_API_KEY[:6] + "..." if OPENAI_API_KEY else None)

# Define the schema for the transaction data we want
schemas = [
    ResponseSchema(name="amount", description="Amount of crypto to transfer."),
    ResponseSchema(name="currency",
                   description="Crypto symbol (e.g. BTC, mUSD)."),
    ResponseSchema(name="recipient", description="Recipient wallet address."),
]

output_parser = StructuredOutputParser.from_response_schemas(schemas)

# Create an LLM with your OpenAI API key
llm = ChatOpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)

# Build the parse prompt
prompt_tmpl = PromptTemplate(
    template=("Extract transaction details from this request:\n"
              "{input}\n"
              "{format_instructions}"),
    input_variables=["input"],
    partial_variables={
        "format_instructions": output_parser.get_format_instructions()
    },
)


def parse_transaction_prompt(prompt: str):
    """
    Use ChatOpenAI to parse the user's prompt into {amount, currency, recipient}.
    Returns either a dict or an error string.
    """
    try:
        formatted = prompt_tmpl.format(input=prompt)
        response_text = llm.predict(formatted)
        parsed = output_parser.parse(response_text)
        return parsed  # e.g. {"amount":"0.000001","currency":"BTC","recipient":"0x1234"}
    except Exception as e:
        return f"❌ Failed to parse prompt: {str(e)}"
