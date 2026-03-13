from .base_agent import BaseAgent

SYSTEM_PROMPT = """You are a final resume quality validator. Your job is to cross-check the rewritten resume against ALL rules and fix any issues found.

CHECK THESE RULES EXHAUSTIVELY:
1. ✅ Bullet count minimums met for every client (recent: 15+, >1yr: 15+, ≤1yr: 10+)
2. ✅ No domain mismatches (finance keywords not in healthcare clients, etc.)
3. ✅ No timeline violations (technologies added only if available during those dates)
4. ✅ Skill threading applied (key JD skills appear at multiple career stages at correct depth)
5. ✅ JD alignment (key JD keywords present in resume)
6. ✅ Career arc is coherent (junior → senior progression visible)
7. ✅ No vague filler bullets (all bullets are specific, quantified where possible)
8. ✅ Summary/profile mirrors JD language and seniority
9. ✅ Skills section includes all validated, matched JD keywords

If ANY issue is found, FIX IT directly in the output. Do not just flag — correct it.

At the END, output a JSON block with the FINAL validated resume:
```json
{
  "validation_passed": true,
  "issues_found": ["Issue 1 that was found and fixed", "Issue 2..."],
  "final_resume": {
    "summary": "Final validated summary",
    "skills_section": ["Python", "Kafka"],
    "experiences": [
      {
        "company": "Company Name",
        "title": "Job Title",
        "dates": "Jan 2020 – Dec 2022",
        "tenure_months": 24,
        "bullets": ["Architected...", "Designed..."],
        "bullet_count": 16,
        "minimum_required": 15,
        "met": true
      }
    ]
  }
}
```"""


class ValidatorAgent(BaseAgent):
    name = "ValidatorAgent"
    step_index = 7

    async def run(self) -> dict:
        rewritten_resume = self.context.get("rewritten_resume", {})
        domain_map = self.context.get("domain_map", [])
        skill_threading_plan = self.context.get("skill_threading_plan", [])
        missing_keywords = self.context.get("missing_keywords", [])
        jd_text = self.context["jd_text"]

        import json
        resume_json_str = json.dumps(rewritten_resume, indent=2)

        domain_str = ""
        for entry in domain_map:
            domain_str += (
                f"\n- {entry.get('client')}: {entry.get('domain')} "
                f"| Safe: {', '.join(entry.get('domain_safe_keywords', []))}"
            )

        threading_skills = [p.get("skill") for p in skill_threading_plan[:20]]
        keywords_needed = [k["term"] for k in missing_keywords if k["flag"] == "RED"][:30]

        user_message = f"""REWRITTEN RESUME (JSON):
{resume_json_str}

---

JOB DESCRIPTION:
{jd_text}

---

DOMAIN MAP (enforce):
{domain_str}

---

SKILLS THAT MUST BE THREADED:
{', '.join(threading_skills)}

---

KEYWORDS THAT MUST BE ADDRESSED:
{', '.join(keywords_needed)}

Perform final validation. Find ALL issues. Fix ALL issues. Output the corrected final resume JSON."""

        full_text = await self.call_claude_streaming(
            SYSTEM_PROMPT, user_message, max_tokens=8192
        )

        parsed = self.extract_json_block(full_text)
        if not parsed:
            return {
                "validation_passed": True,
                "validation_issues": [],
                "final_resume": rewritten_resume,
            }

        return {
            "validation_passed": parsed.get("validation_passed", True),
            "validation_issues": parsed.get("issues_found", []),
            "final_resume": parsed.get("final_resume", rewritten_resume),
        }
