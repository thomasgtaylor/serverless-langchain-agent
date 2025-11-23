from langgraph.graph.state import CompiledStateGraph
from langchain.agents import create_agent
from langgraph_dynamodb_checkpoint import DynamoDBSaver

TWENTY_FOUR_HOURS_IN_SECONDS = 24 * 60 * 60

def agent(table_name: str) -> CompiledStateGraph:
    return create_agent(
       model="gpt-4o-mini",
       checkpointer=DynamoDBSaver(table_name=table_name, ttl_seconds=TWENTY_FOUR_HOURS_IN_SECONDS),
   )
