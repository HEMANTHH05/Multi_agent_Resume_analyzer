from .base_agent import BaseAgent, HumanInputRequired

SYSTEM_PROMPT = """You are a career transition safety analyst. Your ONLY job right now is Part 3: Role Change Safety Check.

Read the resume and job description carefully. Determine:
Does this JD require a significantly different role than what the resume currently reflects?

Examples of significant shifts:
- Cloud/DevOps → ML Engineer
- Data Engineer → Data Scientist
- Backend → AI Engineer
- Software Engineer → Product Manager

If YES — provide:
1. A clear explanation of what is changing and why it is a significant shift
2. 2–4 tailored repositioning options, each with:
   - What gets emphasized
   - What gets de-emphasized
   - Enterprise credibility rating out of 5

At the END, output a JSON block exactly like this:
```json
{
  "role_shift_detected": true,
  "current_role": "Data Engineer",
  "target_role": "ML Engineer",
  "explanation": "The JD requires heavy ML modeling experience...",
  "options": [
    {
      "title": "Option 1: ML-First Pivot",
      "emphasize": "Python, data pipelines, feature engineering",
      "de_emphasize": "ETL tooling, data warehousing",
      "credibility_rating": 4
    }
  ]
}
```

If NO significant shift:
```json
{
  "role_shift_detected": false,
  "current_role": "Data Engineer",
  "target_role": "Senior Data Engineer",
  "explanation": "The JD aligns well with the candidate's current trajectory.",
  "options": []
}
```"""

RESUME_AFTER_PROMPT = """You confirmed the direction. Now record the user's choice and proceed.

Output a JSON block:
```json
{
  "role_shift_detected": true,
  "role_direction": "{user_reply}",
  "confirmed": true
}
```"""


class RoleSafetyAgent(BaseAgent):
    name = "RoleSafetyAgent"
    step_index = 3

    async def run(self) -> dict:
        # If we already have a resume reply, skip detection
        if self._resume_reply is not None:
            await self.stream_to_client(
                f"\n✅ Direction confirmed: \"{self._resume_reply}\"\nProceeding with the pipeline...\n"
            )
            return {
                "role_shift_detected": True,
                "role_direction": self._resume_reply,
                "confirmed": True,
            }

        resume_text = self.context["resume_text"]
        jd_text = self.context["jd_text"]

        user_message = f"""RESUME:
{resume_text}

---

JOB DESCRIPTION:
{jd_text}

Perform Part 3: Role Change Safety Check."""

        full_text = await self.call_claude_streaming(SYSTEM_PROMPT, user_message)

        parsed = self.extract_json_block(full_text)
        if not parsed:
            return {"role_shift_detected": False, "role_direction": None}

        if parsed.get("role_shift_detected"):
            options_text = ""
            for i, opt in enumerate(parsed.get("options", []), 1):
                options_text += f"\n**{i}. {opt.get('title', f'Option {i}')}**"
                options_text += f"\n   Emphasize: {opt.get('emphasize', '')}"
                options_text += f"\n   De-emphasize: {opt.get('de_emphasize', '')}"
                options_text += f"\n   Enterprise credibility: {opt.get('credibility_rating', '?')}/5\n"

            prompt = (
                f"⚠️ Role shift detected: {parsed.get('current_role')} → {parsed.get('target_role')}\n\n"
                f"{parsed.get('explanation', '')}\n\n"
                f"**Your repositioning options:**{options_text}\n"
                "Which direction would you like to go? (Type the option number or describe a blend)"
            )
            await self.require_human_input(prompt)

        return {
            "role_shift_detected": parsed.get("role_shift_detected", False),
            "role_direction": None,
        }
