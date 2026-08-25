from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from agents.semantic_agent import evaluate_semantic_similarity
from agents.coverage_agent import evaluate_concept_coverage
from agents.faithfulness_agent import evaluate_faithfulness
from agents.language_coherence_agent import evaluate_language_coherence
from agents.final_evaluator_agent import evaluate_final_result

#==========
# Lets define states for the evaluation graph
#==========
class EvaluationState(TypedDict, total=False):
    # original Challenge 
    original_text:str
    key_concepts:list[str]

    # User's recall
    recall_text:str

    # Independent evaluation results
    semantic_result: dict
    concept_coverage_result: dict
    faithfulness_result: dict
    language_coherence_result: dict

    # Final Evaluation Result
    final_result: dict

    #======
    # Semantic Evaluation
    #======

def semantic_node(state: EvaluationState):
    result=evaluate_semantic_similarity(
        original_text=state["original_text"],
        recall_text= state["recall_text"]
    )
    return {
        "semantic_result": result.model_dump()
    }
##concept Coverage evaluator 
def concept_coverage_node(state: EvaluationState):
    result= evaluate_concept_coverage(
      key_concepts=state["key_concepts"],
      recall_text=state["recall_text"]  
    )
    return {
        "concept_coverage_result": result.model_dump()
    }
##faithfulness evaluator
def faithfulness_node(state: EvaluationState):
    result=evaluate_faithfulness(
        original_text=state["original_text"],
        recall_text=state["recall_text"]
    )
    return {
        "faithfulness_result": result.model_dump()
    }
##language coherence evaluator
def language_coherence_node(state: EvaluationState):
    result= evaluate_language_coherence(
        recall_text=state["recall_text"]
    )
    return{
        "language_coherence_result": result.model_dump()
    }
## Final Evaluator Node is here 
def final_evaluator_node(state: EvaluationState):
     result= evaluate_final_result(
         semantic_result=state["semantic_result"],
            concept_coverage_result=state["concept_coverage_result"],
            faithfulness_result=state["faithfulness_result"],
            language_coherence_result=state["language_coherence_result"]
     )
     return{
         "final_result": result.model_dump()
     }
## Lets Build the Evaluation Graph 
def build_evaluation_graph():
    graph = StateGraph(EvaluationState)

    graph.add_node("semantic", semantic_node)
    graph.add_node("concept_coverage", concept_coverage_node)
    graph.add_node("faithfulness", faithfulness_node)
    graph.add_node("language_coherence", language_coherence_node)
    graph.add_node("final_evaluator", final_evaluator_node)


    ## lets create the parallel architecture
    graph.add_edge(START, "semantic")
    graph.add_edge(START, "concept_coverage")
    graph.add_edge(START, "faithfulness")
    graph.add_edge(START, "language_coherence")

    ## connect these all to the final evaluator node 

    graph.add_edge("semantic", "final_evaluator")
    graph.add_edge("concept_coverage", "final_evaluator")
    graph.add_edge("faithfulness", "final_evaluator")
    graph.add_edge("language_coherence", "final_evaluator")
    graph.add_edge("final_evaluator", END)
    return graph.compile()
evaluation_graph = build_evaluation_graph()