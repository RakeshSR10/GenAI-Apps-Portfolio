import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from llm import llm
from tools import search_internet

def research_agent(topic: str) -> str:
    """Agent 1: Searches the live internet to collect deep, factual information notes."""
    raw_search_data = search_internet(topic)
    
    prompt = f"""
    You are an expert Autonomous Research Agent.
    Your job is to look at the raw internet search results for a given topic and extract all important facts, statistics, developments, and notes.
    
    Topic: {topic}
    Raw Search Results: {raw_search_data}
    
    Instructions:
    - Clean up the information and summarize it into detailed bullet points.
    - Focus heavily on accurate facts, recent dates, and names.
    - Do not invent any details. If the search results are poor, summarize exactly what is there.
    
    Output your clean research notes below:
    """
    research_notes = llm.invoke(prompt).content.strip()
    return research_notes

def writer_agent(topic: str, research_notes: str) -> str:
    """Agent 2: Takes the clean notes and writes a professional, well-formatted article."""
    prompt = f"""
    You are an elite Technology Writer and Editor Agent.
    Your job is to take raw research notes and transform them into a comprehensive, professional, well-structured article.
    
    Original Topic: {topic}
    Provided Research Notes:
    {research_notes}
    
    Instructions:
    - Write a formal, cohesive report/article.
    - Organize the text cleanly using Markdown headers (##), bold text, and neat sections.
    - Ensure there is a strong Introduction section and a clear Conclusion section.
    - Rely ONLY on the provided research notes. Do not hallucinate external details.
    
    Output your final completed article below:
    """
    final_article = llm.invoke(prompt).content.strip()
    return final_article
