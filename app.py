from dotenv import load_dotenv
from graph_model import build_graph

load_dotenv()

def main():
    graph = build_graph()
    question = "What is the main idea of this PDF document?"

    result = graph.invoke({
        "messages": [
            {"role": "user", "content": question}
        ]
    })

    answer = result["messages"][-1].content
    print("Answer:")
    print(answer)

if __name__ == "__main__":
    main()
