from .base_agent import BaseAgent

SYSTEM_PROMPT = """You are a technical keyword gap analyst. Your ONLY job right now is Part 2: Missing Tech Stack & Keywords.

Go LINE BY LINE through the job description. For every single technology, tool, framework, methodology, platform, certification, or keyword:
- Check if it appears in the resume
- Flag it as:
  🔴 Completely Missing – not anywhere in the resume
  🟡 Present but Needs Reframing – exists but not aligned to JD language

Do NOT skip a single item. Be exhaustive.

At the END, output a JSON block exactly like this:
```json
{
  "missing_keywords": [
    {"term": "Kubernetes", "flag": "RED", "reason": "Not mentioned anywhere in resume"},
    {"term": "CI/CD", "flag": "YELLOW", "reason": "Mentioned as 'continuous integration' but JD uses CI/CD pipeline language"},
    {"term": "FastAPI", "flag": "RED", "reason": "Only Flask mentioned, no FastAPI"}
  ]
}
```"""


class KeywordExtractorAgent(BaseAgent):
    name = "KeywordExtractorAgent"
    step_index = 2

    async def run(self) -> dict:
        resume_text = self.context["resume_text"]
        jd_text = self.context["jd_text"]

        user_message = f"""RESUME:
{resume_text}

---

JOB DESCRIPTION:
{jd_text}

Perform Part 2: Missing Tech Stack & Keywords Analysis. Go line by line through the JD. Do NOT skip anything."""

        full_text = await self.call_claude_streaming(SYSTEM_PROMPT, user_message)

        parsed = self.extract_json_block(full_text)
        missing_keywords = parsed.get("missing_keywords", []) if parsed else []

        return {"missing_keywords": missing_keywords}
