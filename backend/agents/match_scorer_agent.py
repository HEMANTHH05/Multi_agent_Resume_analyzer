from .base_agent import BaseAgent

SYSTEM_PROMPT = """You are a resume match scoring expert. Your ONLY job right now is Part 1: Match Score Analysis.

Analyze the resume against the job description and provide an overall match score (0–100%) broken down by these exact categories:
- Technical Skills
- Tools & Platforms
- Domain / Industry Experience
- Experience Level & Seniority
- Soft Skills & Methodologies
- Certifications & Education

Be thorough and specific. Explain your reasoning for each score.

At the END of your analysis, output a JSON block exactly like this:
```json
{
  "overall_score": 72,
  "categories": {
    "technical_skills": 80,
    "tools_platforms": 75,
    "domain_experience": 65,
    "experience_level": 70,
    "soft_skills": 68,
    "certifications": 60
  },
  "summary": "Brief 2-sentence summary of the match"
}
```"""


class MatchScorerAgent(BaseAgent):
    name = "MatchScorerAgent"
    step_index = 1

    async def run(self) -> dict:
        resume_text = self.context["resume_text"]
        jd_text = self.context["jd_text"]

        user_message = f"""RESUME:
{resume_text}

---

JOB DESCRIPTION:
{jd_text}

Perform Part 1: Match Score Analysis as instructed."""

        full_text = await self.call_claude_streaming(SYSTEM_PROMPT, user_message)

        parsed = self.extract_json_block(full_text)
        match_score = parsed if parsed else {
            "overall_score": 0,
            "categories": {},
            "summary": "Could not parse score"
        }

        return {"match_score": match_score}
