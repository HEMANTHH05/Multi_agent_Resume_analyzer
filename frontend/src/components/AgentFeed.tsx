import { useEffect, useRef } from 'react'
import { AgentMessage } from '../types'
import { MatchScoreCard } from './MatchScoreCard'
import { KeywordList } from './KeywordList'

const AGENT_COLORS: Record<string, string> = {
  ParseAgent: '#6366f1',
  MatchScorerAgent: '#0ea5e9',
  KeywordExtractorAgent: '#f59e0b',
  RoleSafetyAgent: '#ef4444',
  DomainMapperAgent: '#10b981',
  NarrativeBuilderAgent: '#8b5cf6',
  ResumeRewriterAgent: '#ec4899',
  ValidatorAgent: '#14b8a6',
  DocumentGeneratorAgent: '#22c55e',
  System: '#64748b',
}

const AGENT_ICONS: Record<string, string> = {
  ParseAgent: '📄',
  MatchScorerAgent: '📊',
  KeywordExtractorAgent: '🔍',
  RoleSafetyAgent: '⚠️',
  DomainMapperAgent: '🗺️',
  NarrativeBuilderAgent: '🧵',
  ResumeRewriterAgent: '✏️',
  ValidatorAgent: '✅',
  DocumentGeneratorAgent: '📁',
}

interface Props {
  messages: AgentMessage[]
}

export function AgentFeed({ messages }: Props) {
  const bottomRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  if (messages.length === 0) return null

  return (
    <div className="agent-feed">
      {messages.map(msg => (
        <MessageBubble key={msg.id} msg={msg} />
      ))}
      <div ref={bottomRef} />
    </div>
  )
}

function MessageBubble({ msg }: { msg: AgentMessage }) {
  const color = AGENT_COLORS[msg.agent] || '#64748b'
  const icon = AGENT_ICONS[msg.agent] || '🤖'

  if (msg.type === 'structured') {
    return (
      <div className="feed-structured">
        {msg.dataKey === 'match_score' && <MatchScoreCard data={msg.data as any} />}
        {msg.dataKey === 'missing_keywords' && <KeywordList data={msg.data as any} />}
      </div>
    )
  }

  if (msg.type === 'pause') {
    return (
      <div className="feed-pause-card">
        <div className="pause-header">
          <span className="pause-icon">⏸</span>
          <span className="pause-agent" style={{ color }}>
            {icon} {msg.agent}
          </span>
          <span className="pause-badge">Waiting for your input</span>
        </div>
        <div className="pause-prompt">{msg.text}</div>
      </div>
    )
  }

  if (msg.type === 'error') {
    return (
      <div className="feed-error-card">
        <span className="error-icon">❌</span>
        <span className="error-msg">{msg.text}</span>
      </div>
    )
  }

  return (
    <div className="feed-message">
      <div className="feed-msg-header">
        <div className="agent-badge" style={{ background: color + '22', borderColor: color + '44' }}>
          <span className="agent-icon">{icon}</span>
          <span className="agent-name" style={{ color }}>{msg.agent}</span>
        </div>
      </div>
      <div className="feed-msg-body">
        <pre className="feed-text">{msg.text}</pre>
      </div>
    </div>
  )
}
