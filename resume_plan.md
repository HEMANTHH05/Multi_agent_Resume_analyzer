Here is the fully genericized, dynamic prompt ready for anyone to use:

I am attaching two documents:

My Resume – Read every single word, bullet point, technology, tool, methodology, and project detail without skipping anything.
Job Description (JD) – Read every single requirement, preferred skill, technology, tool, responsibility, and keyword without skipping anything.

Your task has 6 parts. Take your time — accuracy and completeness matter more than speed.

PART 1 — MATCH SCORE
Give me an overall match score (0–100%) based on how well my current resume aligns with the JD. Break it down by category:

Technical Skills
Tools & Platforms
Domain / Industry Experience
Experience Level & Seniority
Soft Skills & Methodologies
Certifications & Education


PART 2 — MISSING TECH STACK & KEYWORDS
List every single technology, tool, framework, methodology, platform, or keyword mentioned in the JD that is either:

Completely absent from my resume, OR
Present but not worded/framed the way the JD expects it

Go line by line through the JD to verify. Do NOT skip a single item. Flag each one as:

🔴 Completely Missing – not anywhere in my resume
🟡 Present but Needs Reframing – exists but not aligned to JD language


PART 3 — ROLE CHANGE SAFETY CHECK (Do this BEFORE making any edits)
Read the JD carefully and determine:

Does this JD require a significantly different role than what my resume currently reflects? (e.g., shifting from Cloud/DevOps → ML Engineer, or Data Engineer → Data Scientist, or Backend → AI Engineer)

If YES — STOP and ask me first. Do not proceed to Part 4 until I confirm.
Present:

A clear explanation of what is changing and why it is a significant shift
2–4 tailored repositioning options, each with: what gets emphasized, what gets de-emphasized, and enterprise credibility rating out of 5
Ask: "Which direction would you like to go? Or would you like a blend?"

Only after confirmation, proceed to Parts 4, 5, and 6.
If NO significant role shift is needed, proceed directly.

PART 4 — CLIENT DOMAIN IDENTIFICATION (Do this BEFORE the career narrative or any rewrites)
For every client/project listed in my resume, you must identify the industry domain of that client before writing a single bullet point.
Step 1 — Auto-identify from context:
Read the resume carefully. Use your knowledge and any context clues (company name, project description, technologies used, sector language) to determine the domain of each client:

Examples: Healthcare, Finance/Banking, Retail/E-commerce, Insurance, Telecommunications, Manufacturing, Logistics, Government/Public Sector, Energy/Utilities, Media/Entertainment, Education, SaaS/Technology, etc.

Step 2 — Confirm or ask:

If the domain is clearly identifiable from the resume → state it confidently and proceed
If the domain is ambiguous or cannot be determined from context alone → STOP and ask the user:


"I could not confidently identify the industry domain for the following client(s): [list them]. Could you tell me what domain/industry each one operates in? This is important so I only write domain-appropriate bullet points and do not mix finance language into a healthcare project or vice versa."

Step 3 — Domain lock-in rule (Non-Negotiable):
Once each client's domain is confirmed, that domain becomes a hard constraint on every bullet written for that client:

Never write JD-specific domain language (e.g., financial risk models, claims processing, trading systems, patient data, loan origination) into a client that operates in a completely different domain
If the JD is finance-based but a client is in healthcare → only write technically transferable bullets for that client (cloud infrastructure, data pipelines, APIs, DevOps, security) — never finance-specific outcomes
If a JD keyword is domain-neutral (e.g., Kubernetes, CI/CD, Python, REST APIs, Terraform) → it can appear in any client regardless of domain
If a JD keyword is domain-specific (e.g., FHIR for healthcare, FIX protocol for finance, HL7, Basel III) → it can ONLY appear in clients whose confirmed domain matches

Present a Domain Map before proceeding to Part 5:
Client: [Name] | Domain: [Industry] | Domain-Safe JD Keywords: [list]
Client: [Name] | Domain: [Industry] | Domain-Safe JD Keywords: [list]
Client: [Name] | Domain: [Industry] | Domain-Safe JD Keywords: [list]

PART 5 — CAREER NARRATIVE MAPPING (Do this BEFORE writing any bullet points)
Read the entire career timeline from earliest to most recent and build a career arc map:

Identify the natural progression thread — how responsibilities, seniority, and technical depth evolved
Map which JD skills first appear early and how they grow in complexity across roles
Identify which JD skills are anchored to recent roles only (architecture, leadership, mentoring)
Build a skill evolution plan for every key JD technology that should appear in more than one project

Threading Rule — Non-Negotiable:
Every important JD skill must appear at multiple career stages at the right depth — not just dropped once:

Early roles → foundational, learning, supporting level
Mid roles → independent application, growing scale
Recent roles → ownership, architecture, mentoring, enterprise decisions

Example (if JD asks for FastAPI):

Early role: "Built lightweight REST endpoints using FastAPI to expose pipeline outputs for downstream team consumption"
Mid role: "Designed and deployed FastAPI microservices serving real-time predictions at 10K+ requests/day"
Recent role: "Architected enterprise FastAPI gateway with authentication, rate limiting, and observability across 6 services"

Apply threading to every significant JD skill. Domain-specific skills only thread through clients in the matching domain.

PART 6 — PROJECT-BY-PROJECT RESUME REWRITE
📌 BULLET POINT COUNT RULES — MANDATORY, NON-NEGOTIABLE:
Before writing a single bullet, read each client's tenure duration from the resume and apply this count scale:
Client TypeTenure RuleMinimum BulletsTarget RangeMost Recent / Current ClientAlways — regardless of tenure15 minimum15–20Any other client — tenure above 1 yearWorked there more than 12 months15 minimum15–18Any other client — tenure below 1 yearWorked there 12 months or less10 minimum10–13
How to calculate tenure:

Read the exact start and end dates from the resume for each client
Calculate the duration in months
Apply the correct minimum from the table above
If dates are missing or unclear → ask the user before proceeding:


"I could not find clear dates for [Client Name]. How long did you work there? This determines the bullet point target for that section."

Additional bullet count rules:

Every bullet must be specific, credible, and grounded in the JD or the candidate's actual background — no padding with vague statements
For longer-tenure clients, spread bullets across multiple responsibility areas — do not cluster all bullets into one theme
For the most recent client, bullets must reflect senior ownership — architectural decisions, scale, performance outcomes, stakeholder impact
At the end of every client section, explicitly count and confirm:


"Total bullets for [Client Name]: X — Tenure: [X months/years] — Minimum required: X — Met: ✅ / ❌"


If minimum is not met → keep writing until it is


🔎 VALIDATION GATE — Run silently before every technology suggestion:

Check 1 — Timeline Integrity
Was this technology publicly available, stable, and in production use during the exact dates of this role?
If launched after or only in beta → ❌ DO NOT ADD → Flag: ⚠️ "Timeline Conflict — [Tech] was not mature during [dates]"


Check 2 — Enterprise Adoption Reality
Is this technology used in production by a significant number of large enterprises (Fortune 500s, major banks, healthcare systems, etc.) — not just startups or experiments?
If mostly hype or niche → ❌ DO NOT ADD → Flag: ⚠️ "Low Enterprise Adoption — [Tech] not widely used in production at scale"


Check 3 — Application Credibility
Would a senior hiring manager believe this technology was genuinely used at this client, given its industry, scale, and the role's seniority?
If it feels forced or mismatched → ❌ DO NOT ADD → Flag: ⚠️ "Credibility Risk — [Tech] does not fit this project's scope or domain"


Check 4 — Domain Compatibility (new)
Is this JD keyword domain-neutral OR does it match this client's confirmed domain?
If the keyword is domain-specific and this client is in a different domain → ❌ DO NOT ADD → Flag: ⚠️ "Domain Mismatch — [Tech/Term] is [Finance/Healthcare/etc.]-specific and this client is in [different domain]"

Only technologies and keywords passing ALL 4 checks get added.

For each client/project, provide:

✅ ADD – New bullets, fully written, ready to paste. Strong action verbs. Quantified where possible. Correct depth for career stage. Domain-appropriate.
✏️ MODIFY – Original bullet → Improved version side by side. JD-aligned language. Career-stage-accurate.
✔️ KEEP – Already well-aligned with JD and domain.
🚫 TRUE GAP – JD requirements that cannot be mapped to any project.
⚠️ FLAGGED — NOT ADDED – Failed one or more of the 4 validation checks. State which check and why.
🧵 THREADING NOTE – Where this skill will appear next at a deeper level.
🔢 BULLET COUNT CONFIRMATION – "Total bullets for [Client]: X — Tenure: [duration] — Minimum: X — Met: ✅ / ❌"


PART 7 — GENERATE THE FINAL RESUME AS A WORD DOCUMENT
Once all edits are confirmed:

Produce a complete, clean, ready-to-apply Word (.docx) resume
Layout: professional, ATS-friendly, enterprise-grade formatting
All validated bullets incorporated under the correct sections at the right career stage depth
Bullet counts honored — confirm all minimums before generating
Career arc readable — natural junior → senior progression visible top to bottom
Skills section updated with all matched, timeline-safe, enterprise-adopted, domain-appropriate JD keywords
Summary/Profile rewritten to mirror JD's language, seniority, and domain while reflecting the threading narrative
100% safe to submit — no placeholders, no incomplete sections, no vague language, no domain mismatches, no timeline violations
Every line reflects something true from the candidate's background or a confirmed, validated, threaded addition


STRICT RULES — NON-NEGOTIABLE:

Do NOT generalize — be exhaustive and specific
Do NOT miss any JD keyword or technology
Do NOT fail the 4-check validation gate silently — always flag rejections
Do NOT apply domain-specific language to a client in a different domain
Do NOT write more bullets than the tenure justifies with vague filler
Do NOT make role changes without explicit user approval
Do NOT generate the Word document until ALL bullet count minimums are confirmed
Ask the user when domain or tenure is unclear — never guess and proceed
The final resume must be: match-ready, timeline-honest, domain-accurate, narrative-strong, and enterprise-credible

