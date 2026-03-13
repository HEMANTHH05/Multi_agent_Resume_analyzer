export type StepStatus = 'idle' | 'active' | 'paused' | 'done' | 'error'

export interface PipelineStep {
  name: string
  status: StepStatus
  step_index: number
}

export interface AgentMessage {
  id: string
  agent: string
  step_index: number
  type: 'chunk' | 'structured' | 'system' | 'pause' | 'error'
  text?: string
  data?: unknown
  dataKey?: string
}

export interface MatchScore {
  overall_score: number
  categories: {
    technical_skills: number
    tools_platforms: number
    domain_experience: number
    experience_level: number
    soft_skills: number
    certifications: number
  }
  summary: string
}

export interface KeywordItem {
  term: string
  flag: 'RED' | 'YELLOW'
  reason: string
}

export interface DomainMapEntry {
  client: string
  domain: string
  domain_safe_keywords: string[]
}

export type WSMessage =
  | { type: 'PIPELINE_STARTED'; steps: string[] }
  | { type: 'PIPELINE_COMPLETE' }
  | { type: 'PIPELINE_ERROR'; message: string; agent?: string }
  | { type: 'AGENT_STARTED'; agent: string; step_index: number }
  | { type: 'AGENT_COMPLETE'; agent: string; step_index: number }
  | { type: 'AGENT_CHUNK'; agent: string; step_index: number; text: string }
  | { type: 'STRUCTURED_OUTPUT'; agent: string; step_index: number; key: string; data: unknown }
  | { type: 'AGENT_PAUSED'; agent: string; step_index: number; prompt: string }
  | { type: 'AGENT_RESUMED'; agent: string; step_index: number }
  | { type: 'DOWNLOAD_READY'; url: string }
