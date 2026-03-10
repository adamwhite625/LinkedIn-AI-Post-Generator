import ollama
from src.config import MODEL
from src.extractor import ContentSource

linkedin_system_prompt = """You are a LinkedIn thought leadership expert who transforms technical AI papers and articles into engaging, professional LinkedIn posts.

Your posts should:
- Start with a compelling hook that grabs attention
- Distill complex technical concepts into accessible insights
- Include 3-5 key takeaways or insights
- Use strategic line breaks for readability
- End with a thought-provoking question or call-to-action
- Be 150-300 words (LinkedIn optimal length)
- Use professional yet conversational tone
- Include relevant emojis sparingly (1-3 max)
- Focus on practical implications and industry impact

Format the post in a way that's ready to copy-paste into LinkedIn."""

def user_prompt_for_linkedin(content_source: ContentSource):
    user_prompt = f"""Transform the following {content_source.content_type} into a compelling LinkedIn thought leadership post.

Title: {content_source.title}
URL: {content_source.url}

Content:
{content_source.text[:4000]}  # Limit to avoid token limits

Create a LinkedIn post that:
1. Captures the most important insights
2. Explains why this matters to professionals
3. Engages the reader with a strong opening
4. Ends with a question or discussion prompt

Generate ONLY the LinkedIn post text, ready to publish."""
    return user_prompt

def messages_for_linkedin(content_source: ContentSource):
    """Create message format for Ollama"""
    return [
        {"role": "system", "content": linkedin_system_prompt},
        {"role": "user", "content": user_prompt_for_linkedin(content_source)}
    ]

def generate_linkedin_post(url, content_type='article'):
    """
    Generate a LinkedIn post from a URL directly
    """
    print(f"Extracting content from {url}...")
    content = ContentSource(url, content_type)
    
    print(f"Generating LinkedIn post with {MODEL}...")
    messages = messages_for_linkedin(content)
    response = ollama.chat(model=MODEL, messages=messages)
    
    return response['message']['content']