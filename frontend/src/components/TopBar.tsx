import { PipelineStep } from '../types'

const AGENT_LABELS: Record<string, string> = {
  ParseAgent: 'Parse',
  MatchScorerAgent: 'Score',
  KeywordExtractorAgent: 'Keywords',
  RoleSafetyAgent: 'Role Check',
  DomainMapperAgent: 'Domains',
  NarrativeBuilderAgent: 'Narrative',
  ResumeRewriterAgent: 'Rewrite',
  ValidatorAgent: 'Validate',
  DocumentGeneratorAgent: 'Generate',
}

interface Props {
  steps: PipelineStep[]
}

export function TopBar({ steps }: Props) {
  return (
    <header className="topbar">
      <div className="topbar-logo">
        <span className="logo-icon">✦</span>
        <span className="logo-text">ResumeAI</span>
      </div>

      {steps.length > 0 && (
        <div className="pipeline-steps">
          {steps.map((step, i) => (
            <div key={step.name} className="step-item">
              <div className={`step-dot step-${step.status}`}>
                {step.status === 'done' ? '✓' : step.status === 'active' ? '…' : step.status === 'paused' ? '⏸' : i + 1}
              </div>
              <span className={`step-label step-label-${step.status}`}>
                {AGENT_LABELS[step.name] || step.name}
              </span>
              {i < steps.length - 1 && <div className={`step-line ${step.status === 'done' ? 'step-line-done' : ''}`} />}
            </div>
          ))}
        </div>
      )}

      <div className="topbar-spacer" />
    </header>
  )
}
