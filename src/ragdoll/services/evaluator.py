from datasets import Dataset

from ragas import evaluate
from ragas.metrics import Fai
from ragas.llms import InstructorBaseRagasLLM


class RagEvaluator:
    def __init__(self, evaluator_llm: InstructorBaseRagasLLM):
        self.eval_llm = evaluator_llm
    