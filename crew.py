"""
CrewAI Orchestration - Content Generation Crew

This module orchestrates the multi-agent content generation workflow,
connecting all agents and tasks in a sequential process.
"""

from crewai import Crew, Process
from tasks.research_task import create_research_task
from tasks.strategy_task import create_strategy_task
from tasks.writing_task import create_writing_task
from tasks.editing_task import create_editing_task
from utils.logger import setup_logger
from config import settings
from typing import Dict, Any, Optional, List
import json
import time

logger = setup_logger(__name__)


class ContentGenerationCrew:
    """
    Orchestrates the multi-agent content generation workflow.
    
    The crew executes 4 sequential tasks:
    1. Research - Gather comprehensive information
    2. Strategy - Create SEO-optimized outline
    3. Writing - Generate engaging article
    4. Editing - Quality assurance and finalization
    """
    
    def __init__(self):
        """Initialize the content generation crew."""
        self.logger = logger
        self.logger.info("Content Generation Crew initialized")
    
    def generate_content(
        self,
        topic: str,
        target_audience: Optional[str] = None,
        tone: str = "professional",
        exclude_keywords: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Execute the full content generation workflow.
        
        This method orchestrates all 4 agents to produce a complete,
        publication-ready blog article with metadata.
        
        Args:
            topic: The blog topic to write about (required)
            target_audience: Optional target audience specification
            tone: Writing tone (professional, casual, technical, conversational)
            exclude_keywords: Optional list of keywords/phrases to avoid
            
        Returns:
            Dictionary with generated content, metadata, and sources
            
        Example:
            >>> crew = ContentGenerationCrew()
            >>> result = crew.generate_content(
            ...     topic="The Future of AI in Healthcare",
            ...     target_audience="Healthcare professionals",
            ...     tone="professional"
            ... )
            >>> print(result['status'])
            'success'
        """
        
        start_time = time.time()
        
        try:
            self.logger.info("=" * 60)
            self.logger.info(f"Starting content generation for topic: '{topic}'")
            self.logger.info(f"Target audience: {target_audience or 'General'}")
            self.logger.info(f"Tone: {tone}")
            self.logger.info("=" * 60)
            
            # Create all tasks
            self.logger.info("Creating tasks...")
            
            research_task = create_research_task(topic, target_audience)
            self.logger.info("✓ Research task created")
            
            strategy_task = create_strategy_task(topic, tone)
            self.logger.info("✓ Strategy task created")
            
            writing_task = create_writing_task(exclude_keywords)
            self.logger.info("✓ Writing task created")
            
            editing_task = create_editing_task()
            self.logger.info("✓ Editing task created")
            
            # Link tasks with context flow
            # Each task receives output from previous tasks as context
            self.logger.info("Linking task contexts...")
            strategy_task.context = [research_task]
            writing_task.context = [research_task, strategy_task]
            editing_task.context = [research_task, strategy_task, writing_task]
            self.logger.info("✓ Task context chain established")
            
            # Create the crew
            self.logger.info("Assembling the crew...")
            crew = Crew(
                agents=[
                    research_task.agent,
                    strategy_task.agent,
                    writing_task.agent,
                    editing_task.agent
                ],
                tasks=[
                    research_task,
                    strategy_task,
                    writing_task,
                    editing_task
                ],
                process=Process.sequential,  # Tasks execute in order
                verbose=True,                 # Show detailed execution logs
                memory=settings.enable_memory,  # Agents remember context
                max_rpm=30  # Rate limiting: max 30 requests per minute
            )
            
            self.logger.info("✓ Crew assembled with 4 agents")
            self.logger.info(f"  - Memory enabled: {settings.enable_memory}")
            self.logger.info(f"  - Max iterations: {settings.max_iterations}")
            self.logger.info("")
            
            # Execute the crew workflow
            self.logger.info("🚀 Executing crew workflow...")
            self.logger.info("-" * 60)
            
            result = crew.kickoff()
            
            self.logger.info("-" * 60)
            self.logger.info("✓ Crew workflow completed")
            
            # Parse the final output from the editor
            output = self._parse_output(result)
            
            # Calculate execution time
            execution_time = time.time() - start_time
            self.logger.info(f"⏱️  Total execution time: {execution_time:.2f} seconds")
            
            # Add execution metadata
            output['execution_metadata'] = {
                'execution_time_seconds': round(execution_time, 2),
                'topic': topic,
                'target_audience': target_audience,
                'tone': tone,
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
            self.logger.info("=" * 60)
            self.logger.info("✅ Content generation completed successfully!")
            self.logger.info("=" * 60)
            
            return output
            
        except Exception as e:
            execution_time = time.time() - start_time
            error_message = str(e)
            
            self.logger.error("=" * 60)
            self.logger.error(f"❌ Content generation failed: {error_message}")
            self.logger.error(f"⏱️  Failed after: {execution_time:.2f} seconds")
            self.logger.error("=" * 60)
            
            return {
                "status": "error",
                "message": error_message,
                "execution_metadata": {
                    'execution_time_seconds': round(execution_time, 2),
                    'topic': topic,
                    'error': error_message,
                    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
                }
            }
    
    def _parse_output(self, result: Any) -> Dict[str, Any]:
        """
        Parse the crew output into a standardized format.
        
        The editor agent should return a JSON object, but we handle
        both JSON and string outputs gracefully.
        
        Args:
            result: Output from crew.kickoff()
            
        Returns:
            Standardized dictionary with content and metadata
        """
        
        # If result is already a dict, return it
        if isinstance(result, dict):
            self.logger.info("✓ Output is already in JSON format")
            return result
        
        # If result is a string, try to parse as JSON
        if isinstance(result, str):
            self.logger.info("Parsing string output...")
            
            try:
                output = json.loads(result)
                self.logger.info("✓ Successfully parsed JSON from string")
                return output
            except json.JSONDecodeError:
                self.logger.warning("⚠️  Output is not valid JSON, wrapping in standard format")
                # Wrap raw text in a basic structure
                return {
                    "status": "success",
                    "data": {
                        "content": {
                            "markdown_body": result
                        }
                    },
                    "note": "Output was plain text, not structured JSON"
                }
        
        # Fallback for other types
        self.logger.warning(f"⚠️  Unexpected output type: {type(result)}")
        return {
            "status": "success",
            "data": {
                "raw_output": str(result)
            }
        }
    
    def validate_output(self, output: Dict[str, Any]) -> bool:
        """
        Validate that the output has all required fields.
        
        Args:
            output: The generated content output
            
        Returns:
            True if valid, False otherwise
        """
        
        required_fields = ['status']
        
        for field in required_fields:
            if field not in output:
                self.logger.error(f"❌ Missing required field: {field}")
                return False
        
        if output['status'] == 'success':
            # Check for data field
            if 'data' not in output:
                self.logger.error("❌ Success status but no 'data' field")
                return False
        
        self.logger.info("✓ Output validation passed")
        return True


def create_crew() -> ContentGenerationCrew:
    """
    Factory function to create a new ContentGenerationCrew instance.
    
    Returns:
        ContentGenerationCrew instance
    """
    return ContentGenerationCrew()


# Example usage
if __name__ == "__main__":
    """
    Example of how to use the ContentGenerationCrew.
    
    This requires:
    - GEMINI_API_KEY in .env
    - SERPER_API_KEY in .env
    - All dependencies installed
    """
    
    print("\n" + "=" * 60)
    print("Content Generation Crew - Example Usage")
    print("=" * 60 + "\n")
    
    # Create crew instance
    crew = ContentGenerationCrew()
    
    # Example topic
    example_topic = "How AI is Transforming Customer Service in 2026"
    
    print(f"Topic: {example_topic}")
    print("\nTo run this example, ensure you have:")
    print("  1. GEMINI_API_KEY configured in .env")
    print("  2. SERPER_API_KEY configured in .env")
    print("  3. All dependencies installed (pip install -r requirements.txt)")
    print("\nThen uncomment and run:")
    print()
    print("# result = crew.generate_content(")
    print(f"#     topic='{example_topic}',")
    print("#     target_audience='Business owners',")
    print("#     tone='professional'")
    print("# )")
    print("# print(json.dumps(result, indent=2))")
    print()
    print("=" * 60)
