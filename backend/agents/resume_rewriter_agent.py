from .base_agent import BaseAgent

SYSTEM_PROMPT = """You are a professional resume rewriter. Your ONLY job right now is Part 6: Project-by-Project Resume Rewrite.

BULLET POINT COUNT RULES — MANDATORY:
- Most Recent Client: 15 minimum (15–20 range)
- Any other client with tenure > 12 months: 15 minimum (15–18 range)
- Any other client with tenure ≤ 12 months: 10 minimum (10–13 range)

For EACH client/project, apply the 4-CHECK VALIDATION GATE silently before adding any technology:
✅ Check 1 — Timeline Integrity: Was the tech publicly available and in production use during these exact dates?
✅ Check 2 — Enterprise Adoption Reality: Is this tech used by large enterprises in production (not just hype)?
✅ Check 3 — Application Credibility: Would a senior hiring manager believe this tech was used at this client?
✅ Check 4 — Domain Compatibility: Is this keyword domain-neutral OR does it match this client's confirmed domain?

ONLY add technologies passing ALL 4 checks.

For each client, output:
✅ ADD – New bullets, fully written, ready to paste
✏️ MODIFY – Original bullet → Improved version
✔️ KEEP – Already well-aligned
🚫 TRUE GAP – Cannot be mapped to any project
⚠️ FLAGGED — NOT ADDED – Failed a check (state which check and why)
🧵 THREADING NOTE – Where this skill appears next
🔢 BULLET COUNT CONFIRMATION – "Total bullets for [Client]: X — Tenure: [duration] — Minimum: X — Met: ✅/❌"

Use strong action verbs. Quantify where possible. Match career stage depth (foundational → independent → ownership).

At the END, output a JSON block with the rewritten resume:
```json
{
  "summary": "Rewritten profile/summary section",
  "skills_section": ["Python", "Kafka", "Kubernetes"],
  "experiences": [
    {
      "company": "Company Name",
      "title": "Job Title",
      "dates": "Jan 2020 – Dec 2022",
      "tenure_months": 24,
      "bullets": [
        "Architected...",
        "Designed..."
      ],
      "bullet_count": 16,
      "minimum_required": 15,
      "met": true
    }
  ]
}
```"""


class ResumeRewriterAgent(BaseAgent):
    name = "ResumeRewriterAgent"
    step_index = 6

    async def run(self) -> dict:
        resume_text = self.context["resume_text"]
        jd_text = self.context["jd_text"]
        domain_map = self.context.get("domain_map", [])
        skill_threading_plan = self.context.get("skill_threading_plan", [])
        missing_keywords = self.context.get("missing_keywords", [])
        role_direction = self.context.get("role_direction")

        domain_str = ""
        for entry in domain_map:
            domain_str += (
                f"\n- Client: {entry.get('client')} | Domain: {entry.get('domain')} "
                f"| Safe keywords: {', '.join(entry.get('domain_safe_keywords', []))}"
            )

        threading_str = ""
        for plan in skill_threading_plan[:15]:
            threading_str += f"\n- {plan.get('skill')}:"
            for app in plan.get("appearances", []):
                threading_str += (
                    f"\n    • {app.get('company')} ({app.get('depth_level')}): {app.get('suggested_angle')}"
                )

        keywords_str = "\n".join([
            f"{'🔴' if k['flag'] == 'RED' else '🟡'} {k['term']}: {k['reason']}"
            for k in missing_keywords[:40]
        ]) if missing_keywords else "None"

        direction_str = f"\nROLE DIRECTION CONFIRMED BY USER: {role_direction}" if role_direction else ""

        user_message = f"""RESUME:
{resume_text}

---

JOB DESCRIPTION:
{jd_text}
{direction_str}

---

DOMAIN MAP (enforce strictly — no domain mismatches):
{domain_str}

---

SKILL THREADING PLAN (apply to all bullets):
{threading_str}

---

MISSING/MISALIGNED KEYWORDS TO ADDRESS:
{keywords_str}

---

Perform Part 6: Complete Project-by-Project Resume Rewrite.
Apply the 4-check validation gate to every technology suggestion.
Enforce bullet count minimums strictly.
At the end, output the complete JSON of the rewritten resume."""

        full_text = await self.call_claude_streaming(
            SYSTEM_PROMPT, user_message, max_tokens=8192
        )

        parsed = self.extract_json_block(full_text)
        if not parsed:
            return {"rewritten_resume": {"summary": "", "skills_section": [], "experiences": []}}

        return {"rewritten_resume": parsed}
