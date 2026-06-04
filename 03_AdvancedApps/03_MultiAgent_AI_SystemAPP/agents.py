import warnings
# Suppress terminal developer alerts right away
warnings.filterwarnings("ignore", category=DeprecationWarning)

from llm import llm
from tools import search_internet

def research_agent(topic: str) -> str:
    """Agent 1: Crawls the live internet to pull concrete factual reference data."""
    raw_search_data = search_internet(topic)
    
    prompt = f"""
    You are an expert Autonomous Research Specialist.
    Extract all critical facts, statistics, breakthroughs, and timeline events for the given topic based on these raw web results.
    
    Topic: {topic}
    Raw Search Data: {raw_search_data}
    
    Instructions:
    - Synthesize the data into heavily detailed, descriptive bullet points.
    - Focus strictly on facts, metrics, figures, and recent dates.
    - Do not invent information. If web results are poor, extract exactly what is visible.
    
    Output your comprehensive research notes below:
    """
    return llm.invoke(prompt).content.strip()

def writer_agent(topic: str, research_notes: str, critic_feedback: str = "") -> str:
    """Agent 2: Crafts a formal article draft and revises it based on Critic feedback."""
    feedback_clause = ""
    if critic_feedback:
        feedback_clause = f"""
        This is a REVISED DRAFT. You MUST fix the document by addressing these strict correction notes from your Manager/Critic:
        {critic_feedback}
        """

    prompt = f"""
    You are an elite Technical Writer and Content Architect Agent.
    Transform the raw research notes into a formal, comprehensive, professional report.
    
    Original Topic: {topic}
    Research Notes Provided:
    {research_notes}
    {feedback_clause}
    
    Instructions:
    - Create a clean, formal layout using clear Markdown headers (##), bold terms, and neat paragraphs.
    - Ensure there is a robust Introduction section and a distinct, actionable Conclusion section.
    - Do not hallucinate fields. Rely only on the notes and requested feedback modifications.
    
    Output your completed report draft below:
    """
    return llm.invoke(prompt).content.strip()

def critic_agent(topic: str, article_draft: str) -> str:
    """Agent 3: Evaluates the draft. Returns 'APPROVE' or a list of specific text corrections."""
    prompt = f"""
    You are a strict Managing Editor and Quality Assurance Critic Agent.
    Your single task is to audit the provided report against the target topic to determine if it meets professional standards.
    
    Target Topic: {topic}
    Report Draft under Review:
    {article_draft}
    
    Evaluation Guidelines:
    - Check if the article draft is deeply detailed, clear, and comprehensive.
    - Ensure it has proper structural headings, an Introduction, and a Conclusion.
    - If the report is brief, lacks technical depth, or misses clean structure, you MUST reject it.
    
    Your Output Response Format Rule (STRICT):
    - If the article is ready for publishing, output ONLY the single word: APPROVE
    - If the article needs improvement, output your critical evaluation notes detailing exactly what the writer must fix, add, or expand. (Do NOT include the word APPROVE anywhere in your feedback if you reject it).
    
    Your Evaluation Review Below:
    """
    return llm.invoke(prompt).content.strip()
