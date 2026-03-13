from .base_agent import BaseAgent

SYSTEM_PROMPT = """You are a career narrative architect. Your ONLY job right now is Part 5: Career Narrative Mapping.

Read the entire career timeline from EARLIEST to MOST RECENT and:
1. Identify the natural progression thread — how responsibilities, seniority, and technical depth evolved
2. Map which JD skills first appear early and how they grow in complexity across roles
3. Identify which JD skills are anchored to recent roles only (architecture, leadership, mentoring)
4. Build a skill evolution plan for every key JD technology

Threading Rule (NON-NEGOTIABLE):
Every important JD skill must appear at multiple career stages at the right depth:
- Early roles → foundational, learning, supporting level
- Mid roles → independent application, growing scale
- Recent roles → ownership, architecture, mentoring, enterprise decisions

Domain-specific skills only thread through clients in the MATCHING domain.

At the END, output a JSON block:
```json
{
  "career_arc": "2-3 sentence description of the candidate's career progression narrative",
  "skill_threading_plan": [
    {
      "skill": "Apache Kafka",
      "appearances": [
        {"company": "Early Corp", "depth_level": "foundational", "suggested_angle": "Consumed Kafka streams for downstream processing"},
        {"company": "Mid Corp", "depth_level": "independent", "suggested_angle": "Designed Kafka topic architecture for 5 microservices"},
        {"company": "Recent Corp", "depth_level": "ownership", "suggested_angle": "Architected enterprise Kafka cluster handling 50K events/sec"}
      ]
    }
  ]
}
```"""


class NarrativeBuilderAgent(BaseAgent):
    name = "NarrativeBuilderAgent"
    step_index = 5

    async def run(self) -> dict:
        resume_text = self.context["resume_text"]
        jd_text = self.context["jd_text"]
        domain_map = self.context.get("domain_map", [])
        missing_keywords = self.context.get("missing_keywords", [])

        domain_str = ""
        for entry in domain_map:
            domain_str += f"\n- {entry.get('client')}: {entry.get('domain')} | Safe keywords: {', '.join(entry.get('domain_safe_keywords', []))}"

        keywords_str = "\n".join([
            f"{'🔴' if k['flag'] == 'RED' else '🟡'} {k['term']}: {k['reason']}"
            for k in missing_keywords[:40]
        ]) if missing_keywords else "None identified"

        user_message = f"""RESUME:
{resume_text}

---

JOB DESCRIPTION:
{jd_text}

---

DOMAIN MAP:
{domain_str}

---

MISSING/MISALIGNED KEYWORDS:
{keywords_str}

Perform Part 5: Career Narrative Mapping. Build the skill threading plan for all key JD technologies."""

        full_text = await self.call_claude_streaming(SYSTEM_PROMPT, user_message, max_tokens=4096)

        parsed = self.extract_json_block(full_text)
        if not parsed:
            return {"career_arc": "", "skill_threading_plan": []}

        return {
            "career_arc": parsed.get("career_arc", ""),
            "skill_threading_plan": parsed.get("skill_threading_plan", []),
        }
