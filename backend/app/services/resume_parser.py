import io
from typing import Optional
import fitz  # PyMuPDF
from docx import Document
from loguru import logger


class ResumeParser:
    """Service for parsing resume files (PDF and DOCX)."""

    async def parse(self, file_content: bytes, filename: str) -> Optional[str]:
        """Parse resume file and extract text content."""
        if filename.lower().endswith('.pdf'):
            return self._parse_pdf(file_content)
        elif filename.lower().endswith('.docx'):
            return self._parse_docx(file_content)
        else:
            logger.warning(f"Unsupported file format: {filename}")
            return None

    def _parse_pdf(self, content: bytes) -> Optional[str]:
        """Extract text from PDF file."""
        try:
            doc = fitz.open(stream=content, filetype="pdf")
            text_parts = []
            for page in doc:
                text_parts.append(page.get_text())
            doc.close()
            return "\n".join(text_parts)
        except Exception as e:
            logger.error(f"PDF parsing failed: {e}")
            return None

    def _parse_docx(self, content: bytes) -> Optional[str]:
        """Extract text from DOCX file."""
        try:
            doc = Document(io.BytesIO(content))
            text_parts = []
            for paragraph in doc.paragraphs:
                text_parts.append(paragraph.text)
            return "\n".join(text_parts)
        except Exception as e:
            logger.error(f"DOCX parsing failed: {e}")
            return None

    def extract_skills_basic(self, text: str) -> list:
        """Basic skill extraction using keyword matching (fallback)."""
        # Common tech skills to look for
        skills_keywords = [
            # Programming Languages
            "python", "java", "javascript", "typescript", "c++", "c#", "go", "rust",
            "ruby", "php", "swift", "kotlin", "scala",
            # Frontend
            "react", "angular", "vue", "next.js", "html", "css", "tailwind",
            "redux", "webpack", "vite",
            # Backend
            "node.js", "express", "fastapi", "django", "flask", "spring",
            ".net", "rails", "laravel",
            # Databases
            "sql", "postgresql", "mysql", "mongodb", "redis", "elasticsearch",
            "dynamodb", "cassandra", "neo4j",
            # Cloud & DevOps
            "aws", "azure", "gcp", "docker", "kubernetes", "terraform",
            "jenkins", "github actions", "ci/cd",
            # AI/ML
            "machine learning", "deep learning", "tensorflow", "pytorch",
            "langchain", "llm", "nlp", "computer vision", "rag",
            # Tools & Concepts
            "git", "linux", "rest api", "graphql", "microservices",
            "distributed systems", "system design", "data structures",
            "algorithms", "agile", "scrum",
        ]

        text_lower = text.lower()
        found_skills = []
        for skill in skills_keywords:
            if skill in text_lower:
                found_skills.append(skill.title())

        return list(set(found_skills))


# Singleton instance
resume_parser = ResumeParser()
