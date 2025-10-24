"""
LangGraph workflow nodes for processing exam materials.
"""

from .content import ContentGenerationNode
from .questions import QuestionGenerationNode
from .answers import AnswerGenerationNode
from .input_processing import InputProcessingNode
from .recognition import RecognitionNode
from .synthesis import SynthesisNode
from .edit_material import EditMaterialNode

__all__ = [
    "ContentGenerationNode",
    "QuestionGenerationNode",
    "AnswerGenerationNode",
    "InputProcessingNode",
    "RecognitionNode",
    "SynthesisNode",
    "EditMaterialNode",
]
