"""
Writing Task Definition

Task specification for the writer agent to create engaging,
well-structured content.
"""

from crewai import Task
from agents.writer import create_writer_agent
from typing import Optional, List


def create_writing_task(
    exclude_keywords: Optional[List[str]] = None
) -> Task:
    """
    Create a writing task for content creation.
    
    Args:
        exclude_keywords: Optional list of keywords/phrases to avoid
        
    Returns:
        Configured Task instance
    """
    
    # Build exclusion note if keywords provided
    exclusion_note = ""
    if exclude_keywords:
        exclusion_note = f"\n\nIMPORTANT - DO NOT USE these words/phrases: {', '.join(exclude_keywords)}"
    
    description = f"""Using the research brief and SEO strategy outline, write a complete, 
engaging blog article in Markdown format.

STRICT REQUIREMENTS:

1. FOLLOW THE OUTLINE EXACTLY
   - Use the exact H1, H2, and H3 headings from the strategy
   - Cover each section in the specified order
   - Meet the word count targets for each section
   - Address all PAA questions as indicated

2. WRITING STYLE
   - Write in a natural, conversational yet authoritative voice
   - Imagine explaining this to a smart colleague
   - Use "you" to address the reader directly
   - Vary sentence length for better rhythm
   - Short paragraphs (2-4 sentences max)
   - Active voice whenever possible

3. CONTENT QUALITY
   - Every claim must be backed by research data
   - Cite sources using inline hyperlinks: [source text](URL)
   - Include specific examples and concrete details
   - No vague or generic statements
   - No filler content - every paragraph adds value

4. SEO INTEGRATION (Natural, Not Forced)
   - Use focus keyword in first 100 words
   - Include focus keyword in 2-3 H2 headings naturally
   - Incorporate LSI keywords throughout
   - Don't sacrifice readability for keyword density

5. STRUCTURE ELEMENTS
   - Hook in the first 2 sentences
   - Clear value proposition in introduction
   - Bullet points and numbered lists for scannability
   - Subheadings every 200-300 words
   - Smooth transitions between sections
   - Strong, actionable conclusion

6. MARKDOWN FORMATTING
   - Use # for H1, ## for H2, ### for H3
   - **Bold** for emphasis on key terms
   - *Italic* for subtle emphasis
   - Inline links: [anchor text](URL)
   - Numbered lists: 1. 2. 3.
   - Bullet lists: - item
   - Code blocks with ``` if showing code examples

7. CITATIONS
   - Cite sources naturally within the text
   - Format: [authoritative source name](URL)
   - Minimum 8-10 citations throughout the article
   - Link to the most authoritative source available

ABSOLUTELY FORBIDDEN:
❌ "unleash", "unlock", "delve", "dive deep"
❌ "in today's world", "in this day and age"
❌ "it's no secret that", "needless to say"
❌ "game-changer", "revolutionary" (unless truly justified)
❌ Corporate jargon and buzzwords
❌ Robotic or AI-sounding phrases
❌ Fluff or filler sentences{exclusion_note}

ENGAGEMENT TACTICS:
✓ Ask rhetorical questions
✓ Use analogies to explain complex concepts
✓ Include specific numbers and statistics
✓ Reference real-world examples
✓ Address common objections or concerns
✓ Provide actionable takeaways

Your article should read like it was written by a knowledgeable human who genuinely
wants to help the reader understand the topic."""

    expected_output = """A complete blog article in Markdown format:

# [H1 Title from Strategy]

[Opening hook - 1-2 compelling sentences that grab attention]

[Value proposition - what the reader will learn]

[Focus keyword naturally incorporated in first 100 words]

## [First H2 from Strategy]

[Engaging content following the outline, 200-400 words]

[Include inline citations: [Source Name](URL)]

### [H3 Subsection if applicable]

[Detailed coverage with examples and data]

## [Second H2 from Strategy]

[Continue following the outline structure]

- Bullet points for scannability
- Include specific examples
- Back claims with citations

## [Continue with all sections from outline]

### [FAQ Section]

**Question 1 from PAA?**

Direct, concise answer optimized for featured snippet. [Source](URL)

**Question 2 from PAA?**

Clear answer with supporting details.

[Continue with 5-8 FAQs]

## Conclusion

[Summarize key takeaways]

[Actionable next steps for the reader]

[Reinforce main value proposition]

---

REQUIREMENTS:
- Total word count: 1,500-2,500 words (match strategy recommendation)
- Format: Valid Markdown
- Citations: Minimum 8-10 inline hyperlinks
- Paragraphs: 2-4 sentences max
- Tone: Natural, authoritative, engaging
- SEO: Focus keyword appears naturally 3-5 times
- Quality: Every paragraph adds value, no fluff"""

    # Create the writer agent
    agent = create_writer_agent()
    
    # Create and return the task
    task = Task(
        description=description,
        expected_output=expected_output,
        agent=agent
    )
    
    return task
