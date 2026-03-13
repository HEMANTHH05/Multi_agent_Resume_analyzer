from .base_agent import BaseAgent, HumanInputRequired

SYSTEM_PROMPT = """You are a client domain identification expert. Your ONLY job right now is Part 4: Client Domain Identification.

For EVERY client/project listed in the resume:
1. Identify the industry domain (Healthcare, Finance/Banking, Retail/E-commerce, Insurance, Telecom, Manufacturing, Logistics, Government, Energy, Media, Education, SaaS/Technology, etc.)
2. Map which JD keywords are domain-safe for that client

Domain lock-in rule (NON-NEGOTIABLE):
- Domain-neutral keywords (Kubernetes, CI/CD, Python, REST APIs, Terraform) → safe for ANY client
- Domain-specific keywords (FHIR=Healthcare, FIX protocol=Finance, HL7=Healthcare, Basel III=Finance) → ONLY for matching domain clients

If ANY client's domain cannot be determined from context → list them in "ambiguous_clients" and DO NOT guess.

At the END, output a JSON block:
```json
{
  "domain_map": [
    {
      "client": "Accenture / Client A",
      "domain": "Finance/Banking",
      "domain_safe_keywords": ["Python", "Kafka", "REST APIs", "risk modeling"]
    }
  ],
  "ambiguous_clients": ["Client XYZ - insufficient context to determine domain"]
}
```"""

CLARIFICATION_PROMPT = """The user has provided domain clarification. Now complete the domain map with all clients including the clarified ones.

User's clarification: {user_reply}

Output the complete domain map JSON:
```json
{
  "domain_map": [...],
  "ambiguous_clients": []
}
```"""


class DomainMapperAgent(BaseAgent):
    name = "DomainMapperAgent"
    step_index = 4

    async def run(self) -> dict:
        resume_text = self.context["resume_text"]
        jd_text = self.context["jd_text"]
        missing_keywords = self.context.get("missing_keywords", [])

        keywords_str = ", ".join([k["term"] for k in missing_keywords[:30]]) if missing_keywords else "N/A"

        if self._resume_reply is not None:
            # Second pass with user clarification
            user_message = f"""RESUME:
{resume_text}

---

JOB DESCRIPTION:
{jd_text}

Key JD keywords to map: {keywords_str}

User clarification on ambiguous domains: {self._resume_reply}

Now complete the full domain map for ALL clients."""

            full_text = await self.call_claude_streaming(
                CLARIFICATION_PROMPT.replace("{user_reply}", self._resume_reply),
                user_message
            )
        else:
            user_message = f"""RESUME:
{resume_text}

---

JOB DESCRIPTION:
{jd_text}

Key JD keywords to map: {keywords_str}

Perform Part 4: Client Domain Identification."""

            full_text = await self.call_claude_streaming(SYSTEM_PROMPT, user_message)

        parsed = self.extract_json_block(full_text)
        if not parsed:
            return {"domain_map": [], "ambiguous_clients": []}

        ambiguous = parsed.get("ambiguous_clients", [])
        if ambiguous and self._resume_reply is None:
            ambiguous_list = "\n".join(f"• {c}" for c in ambiguous)
            prompt = (
                f"I could not confidently identify the industry domain for the following client(s):\n{ambiguous_list}\n\n"
                "Could you tell me what domain/industry each one operates in? "
                "(e.g., 'Client XYZ is in Healthcare, Client ABC is in Finance')"
            )
            await self.require_human_input(prompt)

        return {
            "domain_map": parsed.get("domain_map", []),
            "ambiguous_clients": [],
        }
