import io
import pdfplumber
from docx import Document as DocxDocument
from .base_agent import BaseAgent


class ParseAgent(BaseAgent):
    name = "ParseAgent"
    step_index = 0

    async def run(self) -> dict:
        await self.stream_to_client("Parsing your resume...\n")

        file_bytes: bytes = self.context["resume_bytes"]
        file_extension: str = self.context["file_extension"].lower()

        if file_extension == ".pdf":
            resume_text = self._parse_pdf(file_bytes)
        elif file_extension in (".docx", ".doc"):
            resume_text = self._parse_docx(file_bytes)
        else:
            resume_text = file_bytes.decode("utf-8", errors="ignore")

        await self.stream_to_client(f"Resume parsed successfully. ({len(resume_text)} characters extracted)\n")

        return {
            "resume_text": resume_text,
        }

    def _parse_pdf(self, file_bytes: bytes) -> str:
        text_parts = []
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
        return "\n".join(text_parts)

    def _parse_docx(self, file_bytes: bytes) -> str:
        doc = DocxDocument(io.BytesIO(file_bytes))
        text_parts = []
        for para in doc.paragraphs:
            if para.text.strip():
                text_parts.append(para.text)
        return "\n".join(text_parts)
