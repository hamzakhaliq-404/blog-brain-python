"""
Editorial Review Task Definition

Task specification for the editor agent to perform quality assurance
and generate final publication-ready output.
"""

from crewai import Task
from agents.editor import create_editor_agent


def create_editing_task() -> Task:
    """
    Create an editorial review task for final content polish.
    
    Returns:
        Configured Task instance
    """
    
    description = """Review and finalize the draft article for publication. Your job is to 
ensure the content meets publication quality standards and generate all required metadata.

EDITORIAL REVIEW CHECKLIST:

1. CONTENT QUALITY ASSESSMENT
   ✓ Does it sound authentically human? (Not robotic or AI-generated)
   ✓ Is the tone consistent throughout?
   ✓ Are transitions smooth between sections?
   ✓ Does the introduction hook effectively?
   ✓ Is the conclusion strong and actionable?
   ✓ Overall readability and flow

2. FACTUAL VERIFICATION
   ✓ Are all claims backed by evidence?
   ✓ Are sources properly cited with working hyperlinks?
   ✓ Are statistics and data points accurate and recent?
   ✓ No vague statements like "many experts say" without attribution
   ✓ Verify at least 8-10 quality citations present

3. AI-ISM DETECTION (CRITICAL)
   ❌ Scan for banned phrases: "unleash", "unlock", "delve", "dive deep"
   ❌ "in today's world", "it's no secret", "needless to say"
   ❌ "game-changer", "revolutionary" (unless truly justified)
   ❌ Corporate jargon and buzzwords
   ❌ Repetitive sentence structures
   ❌ Overly formal or robotic language
   
   If you find AI-isms: REMOVE or REPHRASE them

4. FORMATTING VERIFICATION
   ✓ Only ONE H1 heading (the title)
   ✓ Proper H2 and H3 hierarchy
   ✓ All hyperlinks are valid Markdown format: [text](URL)
   ✓ Lists formatted correctly (bullets or numbers)
   ✓ Paragraphs are short (2-4 sentences)
   ✓ Proper emphasis with **bold** where needed

5. SEO COMPLIANCE
   ✓ Focus keyword appears in first 100 words
   ✓ Focus keyword in 2-3 H2 headings (naturally)
   ✓ LSI keywords distributed throughout
   ✓ Keyword usage is natural, not forced
   ✓ No keyword stuffing

6. MARKDOWN TO HTML CONVERSION
   - Convert the Markdown article to clean HTML
   - Preserve all hyperlinks and formatting
   - Ensure valid HTML structure
   - Keep both Markdown and HTML versions

7. METADATA GENERATION
   Create optimized metadata:
   
   - SEO Title: 55-60 characters, includes focus keyword, compelling
   - Meta Description: 150-160 characters, includes focus keyword, has CTA
   - URL Slug: lowercase, hyphens, no special characters
   - Focus Keyword: Primary target keyword
   - Estimated Reading Time: Calculate from word count (200 WPM average)
   - Word Count: Total words in article
   - Source List: Extract all citation URLs

8. QUALITY GATE DECISION
   
   IF content has major issues (poor quality, heavy AI-isms, missing citations):
   → REJECT and delegate back to the writer with specific feedback
   
   IF content has minor issues (small formatting, slight rewording needed):
   → FIX THEM YOURSELF and proceed
   
   IF content meets all standards:
   → APPROVE and generate final JSON output

DELEGATION AUTHORITY:
You have the power to send the article back to the writer if quality is insufficient.
Be ruthless but fair - our standards are high for a reason.

Your mission: Ensure every piece of content we publish is genuinely valuable,
authentically human, and ready to rank."""

    expected_output = """Final publication-ready output in JSON format:

{
  "status": "approved",
  "metadata": {
    "seo_title": "[55-60 char optimized title]",
    "meta_description": "[150-160 char description with CTA]",
    "slug": "url-friendly-slug",
    "focus_keyword": "[primary keyword]",
    "estimated_read_time": "8 mins",
    "word_count": 1850,
    "published_date": "[current date in ISO format]"
  },
  "content": {
    "html_body": "<h1>[Title]</h1><p>[Full HTML content]</p>...",
    "markdown_body": "# [Title]\\n\\n[Full Markdown content]..."
  },
  "sources": [
    "https://source1.com/article",
    "https://source2.com/study",
    "https://source3.com/report"
  ],
  "quality_checks": {
    "ai_isms_removed": true,
    "citations_count": 12,
    "readability_score": "good",
    "seo_compliance": "passed",
    "human_sounding": true
  },
  "editor_notes": "[Any important notes about the content or edits made]"
}

REJECTION FORMAT (if quality is insufficient):
{
  "status": "rejected",
  "reason": "[Specific issues that need addressing]",
  "required_changes": [
    "[Specific change 1]",
    "[Specific change 2]"
  ],
  "delegate_to": "writer"
}

Ensure all fields are properly filled and the JSON is valid."""

    # Create the editor agent
    agent = create_editor_agent()
    
    # Create and return the task
    task = Task(
        description=description,
        expected_output=expected_output,
        agent=agent
    )
    
    return task
