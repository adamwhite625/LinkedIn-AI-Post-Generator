import requests
from bs4 import BeautifulSoup
import re
import fitz  # PyMuPDF
from io import BytesIO

def is_pdf_url(url: str) -> bool:
    return url.lower().endswith(".pdf")

class ContentSource:
    """
    Represents an AI paper or article to transform into content
    """

    def __init__(self, url, content_type='article'):
        self.url = url
        self.content_type = content_type

        # Auto-detect PDF based on URL or explicit content_type
        if self.content_type == "paper" or is_pdf_url(url):
            self._extract_pdf()
        else:
            self._extract_html()

    def _extract_html(self):
        response = requests.get(self.url, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        self.title = soup.title.string if soup.title else "No title found"

        if soup.body:
            for tag in soup.body.find_all(
                ["script", "style", "img", "input", "nav", "footer", "header"]
            ):
                tag.decompose()

            self.text = soup.body.get_text(separator="\n", strip=True)
        else:
            self.text = soup.get_text(separator="\n", strip=True)

        self.text = re.sub(r'\n\s*\n', '\n\n', self.text)

    def _extract_pdf(self):
        response = requests.get(self.url, timeout=20)
        response.raise_for_status()

        pdf = fitz.open(stream=BytesIO(response.content), filetype="pdf")

        pages_text = []
        for page in pdf:
            pages_text.append(page.get_text())

        self.text = "\n\n".join(pages_text)

        # Fallback title extraction
        self.title = self._infer_title_from_text()

    def _infer_title_from_text(self):
        lines = [l.strip() for l in self.text.split("\n") if len(l.strip()) > 10]
        return lines[0][:200] if lines else "AI Paper"