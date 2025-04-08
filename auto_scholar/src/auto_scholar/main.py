#!/usr/bin/env python
import sys
import warnings
from datetime import datetime
from crew import AutoScholar
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")
import os
import dotenv
dotenv.load_dotenv()

def run():
    inputs = {
        'topic': 'Vision Transformers',
        'current_year': str(datetime.now().year)
    }
    
    try:
        result = AutoScholar().crew().kickoff(inputs=inputs)
        
        # Save the final report
        with open("research_report.md", "w") as f:
            f.write(result)
        
        print(f"✅ Research completed! Report saved to research_report.md")
        print(f"✅ ChromaDB vector store persisted to 'chroma_db' directory")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        AutoScholar().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        AutoScholar().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs",
        "current_year": str(datetime.now().year)
    }
    try:
        AutoScholar().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")


if __name__ == "__main__":
    run()