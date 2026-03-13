import asyncio
import json
from typing import Callable, Coroutine

from agents.base_agent import HumanInputRequired
from agents.parse_agent import ParseAgent
from agents.match_scorer_agent import MatchScorerAgent
from agents.keyword_extractor_agent import KeywordExtractorAgent
from agents.role_safety_agent import RoleSafetyAgent
from agents.domain_mapper_agent import DomainMapperAgent
from agents.narrative_builder_agent import NarrativeBuilderAgent
from agents.resume_rewriter_agent import ResumeRewriterAgent
from agents.validator_agent import ValidatorAgent
from agents.document_generator_agent import DocumentGeneratorAgent

AGENT_CLASSES = [
    ParseAgent,
    MatchScorerAgent,
    KeywordExtractorAgent,
    RoleSafetyAgent,
    DomainMapperAgent,
    NarrativeBuilderAgent,
    ResumeRewriterAgent,
    ValidatorAgent,
    DocumentGeneratorAgent,
]


class Orchestrator:
    def __init__(self, ws_send: Callable[[str], Coroutine], context: dict):
        self.ws_send = ws_send
        self.context = context
        self._resume_event = asyncio.Event()
        self._user_reply: str | None = None
        self._paused_agent = None
        self._waiting_for_input = False

    async def send(self, message: dict):
        await self.ws_send(json.dumps(message))

    async def receive_user_reply(self, text: str):
        self._user_reply = text
        self._resume_event.set()

    async def run(self):
        step_names = [cls.name for cls in AGENT_CLASSES]

        await self.send({
            "type": "PIPELINE_STARTED",
            "steps": step_names,
        })

        for AgentClass in AGENT_CLASSES:
            agent = AgentClass(ws_send=self.ws_send, context=self.context)

            await self.send({
                "type": "AGENT_STARTED",
                "agent": AgentClass.name,
                "step_index": AgentClass.step_index,
            })

            try:
                result = await agent.run()
                self.context.update(result)

                # Emit structured output for UI widgets
                await self._emit_structured_output(AgentClass.name, AgentClass.step_index, result)

                await self.send({
                    "type": "AGENT_COMPLETE",
                    "agent": AgentClass.name,
                    "step_index": AgentClass.step_index,
                })

            except HumanInputRequired as e:
                # Pause the pipeline and wait for user input
                self._waiting_for_input = True
                self._paused_agent = agent

                await self.send({
                    "type": "AGENT_PAUSED",
                    "agent": AgentClass.name,
                    "step_index": AgentClass.step_index,
                    "prompt": e.prompt,
                })

                # Wait for user reply
                self._resume_event.clear()
                await self._resume_event.wait()

                reply = self._user_reply
                self._user_reply = None
                self._waiting_for_input = False

                await self.send({
                    "type": "AGENT_RESUMED",
                    "agent": AgentClass.name,
                    "step_index": AgentClass.step_index,
                })

                # Inject reply and re-run agent
                agent.inject_reply(reply)
                result = await agent.run()
                self.context.update(result)

                await self._emit_structured_output(AgentClass.name, AgentClass.step_index, result)

                await self.send({
                    "type": "AGENT_COMPLETE",
                    "agent": AgentClass.name,
                    "step_index": AgentClass.step_index,
                })

            except Exception as e:
                await self.send({
                    "type": "PIPELINE_ERROR",
                    "agent": AgentClass.name,
                    "message": str(e),
                })
                raise

        # Pipeline complete — send download link
        docx_path = self.context.get("docx_path")
        session_id = self.context.get("session_id", "resume")

        if docx_path:
            await self.send({
                "type": "DOWNLOAD_READY",
                "url": f"/download/{session_id}",
            })

        await self.send({"type": "PIPELINE_COMPLETE"})

    async def _emit_structured_output(self, agent_name: str, step_index: int, result: dict):
        structured_keys = {
            "MatchScorerAgent": "match_score",
            "KeywordExtractorAgent": "missing_keywords",
            "DomainMapperAgent": "domain_map",
        }
        key = structured_keys.get(agent_name)
        if key and key in result:
            await self.send({
                "type": "STRUCTURED_OUTPUT",
                "agent": agent_name,
                "step_index": step_index,
                "key": key,
                "data": result[key],
            })
