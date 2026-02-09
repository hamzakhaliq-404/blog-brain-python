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
        
        The editor agent returns JSON wrapped in markdown code blocks.
        We need to extract and parse this JSON properly.
        
        Args:
            result: Output from crew.kickoff()
            
        Returns:
            Standardized dictionary with content and metadata
        """
        
        self.logger.info("Parsing crew output...")
        
        # CrewAI returns a result object with raw string output
        raw_output = str(result)
        
        self.logger.info(f"Raw output type: {type(result)}")
        
        try:
            # The editor returns JSON wrapped in ```json code blocks
            # Extract JSON from code blocks
            if "```json" in raw_output:
                self.logger.info("Extracting JSON from code block...")
                start_idx = raw_output.find("```json") + 7
                end_idx = raw_output.find("```", start_idx)
                json_str = raw_output[start_idx:end_idx].strip()
                
                # Parse the JSON
                parsed_data = json.loads(json_str)
                self.logger.info("✓ Successfully extracted and parsed JSON from code block")
                
                # The editor returns the data directly, wrap it in success response
                return {
                    "status": "success",
                    "data": {
                        "metadata": parsed_data.get("metadata", {}),
                        "content": parsed_data.get("content", {}),
                        "sources": parsed_data.get("sources", []),
                        "quality_checks": parsed_data.get("quality_checks"),
                        "editor_notes": parsed_data.get("editor_notes")
                    }
                }
            
            # Try parsing as direct JSON
            try:
                parsed_data = json.loads(raw_output)
                self.logger.info("✓ Successfully parsed direct JSON")
                
                # Check if it's already in the correct format
                if "status" in parsed_data and "data" in parsed_data:
                    return parsed_data
                
                # Wrap it in success response
                return {
                    "status": "success",
                    "data": {
                        "metadata": parsed_data.get("metadata", {}),
                        "content": parsed_data.get("content", {}),
                        "sources": parsed_data.get("sources", []),
                        "quality_checks": parsed_data.get("quality_checks"),
                        "editor_notes": parsed_data.get("editor_notes")
                    }
                }
                
            except json.JSONDecodeError:
                self.logger.warning("⚠️  Could not parse as JSON, treating as plain text")
                
                # Fallback: wrap raw text
                return {
                    "status": "success",
                    "data": {
                        "metadata": {
                            "seo_title": "Generated Content",
                            "meta_description": "AI-generated content",
                            "slug": "generated-content",
                            "focus_keyword": "content",
                            "estimated_read_time": "5 mins",
                            "word_count": len(raw_output.split())
                        },
                        "content": {
                            "markdown_body": raw_output,
                            "html_body": f"<p>{raw_output}</p>"
                        },
                        "sources": []
                    }
                }
                
        except Exception as e:
            self.logger.error(f"❌ Error parsing output: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to parse editor output: {str(e)}",
                "data": {
                    "raw_output": raw_output
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
