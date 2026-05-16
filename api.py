from fastapi import FastAPI
from pydantic import BaseModel
from agent import DoctorAppointmentAgent
from langchain_core.messages import HumanMessage
import os

os.environ.pop("SSL_CERT_FILE", None)

# Create FastAPI app instance
app = FastAPI()

# Request body model
class UserQuery(BaseModel):
    id_number: int
    messages: str


agent = DoctorAppointmentAgent()


@app.post("/execute")
def execute_agent(user_input: UserQuery):

    app_graph = agent.workflow()

    input_messages = [
        HumanMessage(content=user_input.messages)
    ]

    query_data = {
        "messages": input_messages,
        "id_number": user_input.id_number,
        "next": "",
        "query": "",
        "current_reasoning": "",
    }

    response = app_graph.invoke(
        query_data,
        config={"recursion_limit": 20}
    )

    return {"messages": response["messages"]}


# Uvicorn entrypoint
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
                    "api:app",
                    host="0.0.0.0",
                    port=8003,
                    reload=True
                )