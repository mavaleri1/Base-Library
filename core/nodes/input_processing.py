"""
Node for processing user input.
Analyzes incoming data and determines the presence of images.
"""

import logging
from typing import Literal
from langgraph.types import Command
from pathlib import Path

from ..core.state import GeneralState
from ..services.file_utils import ImageFileManager
from .base import BaseWorkflowNode


logger = logging.getLogger(__name__)


class InputProcessingNode(BaseWorkflowNode):
    """
    Node for processing user input.
    Analyzes message and image_paths, sets the correct state values.
    Simple node without HITL logic.
    """

    def __init__(self):
        super().__init__(logger=logger)
        self.file_manager = ImageFileManager()

    def get_node_name(self) -> str:
        """Returns the name of the node for configuration search"""
        return "input_processing"

    async def __call__(
        self, state: GeneralState, config
    ) -> Command[Literal["generating_content"]]:
        """
        Processes user input and validates images.

        Args:
            state: Current state with input_content and potentially image_paths
            config: LangGraph configuration

        Returns:
            Command with transition to content generation and updated state
        """
        thread_id = config["configurable"]["thread_id"]
        logger.info(f"Starting input processing for thread {thread_id}")

        # Get input_content from state
        input_content = state.input_content

        # Validate input_content at system entry
        logger.debug(f"Security guard status: {self.security_guard is not None}")
        if self.security_guard:
            logger.info("Validating exam question for security threats")
            input_content = await self.validate_input(input_content)
        else:
            logger.warning("Security guard not initialized - skipping validation")

        # Generate a short name for the session
        display_name = None
        try:
            model = self.create_model()
            display_name_prompt = f"""Create a brief title (3-5 words) for the following exam question:
"{input_content}"

Requirements:
- Maximum 5 words
- Reflects the essence of the question
- No special characters or punctuation
- On the same language as the question

Answer only the name, without explanations."""

            response = await model.ainvoke(display_name_prompt)
            display_name = response.content.strip()
            logger.info(f"Generated display_name: {display_name}")
        except Exception as e:
            logger.warning(f"Failed to generate display_name: {e}")
            # Fallback: use first words of question
            words = input_content.split()[:5]
            display_name = " ".join(words)
            if len(words) > 5:
                display_name += "..."

        # Validate and process images
        validated_image_paths = []
        if state.image_paths:
            logger.info(f"Found {len(state.image_paths)} image paths to validate")

            for image_path in state.image_paths:
                path_obj = Path(image_path)
                if path_obj.exists() and self.file_manager.validate_image_file(
                    path_obj
                ):
                    validated_image_paths.append(image_path)
                    logger.info(f"Validated image: {image_path}")
                else:
                    logger.warning(f"Invalid or missing image: {image_path}")

        # Update state
        update_data = {
            "input_content": input_content,
            "image_paths": validated_image_paths,
            "display_name": display_name,  # Add display_name to state
        }

        logger.info(
            f"Input processing completed for thread {thread_id}. "
            f"Question: '{input_content[:100]}...', Images: {len(validated_image_paths)}"
        )

        return Command(goto="generating_content", update=update_data)
