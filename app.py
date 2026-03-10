import gradio as gr
import ollama
from src.config import MODEL
from src.extractor import ContentSource, is_pdf_url
from src.generator import messages_for_linkedin

def generate_linkedin_post_gradio(url, content_type):
    try:
        if not url.strip():
            return "Please enter a valid URL."

        # Auto-detect PDF
        if is_pdf_url(url):
            content_type = "paper"

        content = ContentSource(url, content_type)

        messages = messages_for_linkedin(content)
        response = ollama.chat(model=MODEL, messages=messages)

        return response["message"]["content"]

    except Exception as e:
        return f"Error: {str(e)}"

with gr.Blocks(
    title="AI Paper → LinkedIn Post Generator",
    theme=gr.themes.Soft()
) as demo:

    gr.Markdown(
        """
        # AI Paper → LinkedIn Thought Leadership Generator

        Paste a **paper or article URL** and get a **ready-to-publish LinkedIn post**.

        Works great with:
        - arXiv papers 
        - Blogs & research articles 
        """
    )

    with gr.Row():
        url_input = gr.Textbox(
            label="Article / Paper URL",
            placeholder="https://arxiv.org/abs/1706.03762",
            scale=4
        )

    content_type = gr.Radio(
        choices=["article", "paper"],
        value="paper",
        label="Content Type"
    )

    generate_btn = gr.Button("Generate LinkedIn Post", variant="primary")

    output = gr.Textbox(
        label="LinkedIn Post (Copy & Paste)",
        lines=15
    )

    generate_btn.click(
        fn=generate_linkedin_post_gradio,
        inputs=[url_input, content_type],
        outputs=output
    )

if __name__ == "__main__":
    print(f"Starting Gradio App. Using model: {MODEL}")
    demo.launch()