from langchain_community.document_loaders import YoutubeLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def load_youtube_transcript(video_url):
    """Downloads the transcript text of a YouTube video safely."""
    try:
        # Corrected method initialization using the accurate class name
        loader = YoutubeLoader.from_youtube_url(
            video_url, 
            add_video_info=False
        )
        return loader.load()
    except Exception as e:
        raise Exception(f"Failed to fetch transcript: {str(e)}")
    
def split_docs(docs):
    """Splits text transcripts into smaller windows for optimal semantic matching."""
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    return splitter.split_documents(docs)