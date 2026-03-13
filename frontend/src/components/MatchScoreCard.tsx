import { MatchScore } from '../types'

const CATEGORY_LABELS: Record<string, string> = {
  technical_skills: 'Technical Skills',
  tools_platforms: 'Tools & Platforms',
  domain_experience: 'Domain / Industry',
  experience_level: 'Experience Level',
  soft_skills: 'Soft Skills',
  certifications: 'Certifications',
}

interface Props {
  data: MatchScore
}

function ScoreRing({ score }: { score: number }) {
  const r = 42
  const circ = 2 * Math.PI * r
  const offset = circ - (score / 100) * circ
  const color = score >= 75 ? '#22c55e' : score >= 50 ? '#f59e0b' : '#ef4444'

  return (
    <div className="score-ring-wrap">
      <svg width="100" height="100" viewBox="0 0 100 100">
        <circle cx="50" cy="50" r={r} fill="none" stroke="#1e293b" strokeWidth="10" />
        <circle
          cx="50" cy="50" r={r} fill="none"
          stroke={color} strokeWidth="10"
          strokeDasharray={circ}
          strokeDashoffset={offset}
          strokeLinecap="round"
          transform="rotate(-90 50 50)"
          style={{ transition: 'stroke-dashoffset 1s ease' }}
        />
      </svg>
      <div className="score-ring-label" style={{ color }}>
        <span className="score-ring-number">{score}%</span>
        <span className="score-ring-sub">Match</span>
      </div>
    </div>
  )
}

function ScoreBar({ label, value }: { label: string; value: number }) {
  const color = value >= 75 ? '#22c55e' : value >= 50 ? '#f59e0b' : '#ef4444'
  return (
    <div className="score-bar-row">
      <span className="score-bar-label">{label}</span>
      <div className="score-bar-track">
        <div className="score-bar-fill" style={{ width: `${value}%`, background: color }} />
      </div>
      <span className="score-bar-value" style={{ color }}>{value}%</span>
    </div>
  )
}

export function MatchScoreCard({ data }: Props) {
  return (
    <div className="match-score-card">
      <div className="match-score-header">
        <ScoreRing score={data.overall_score} />
        <div className="match-score-summary">
          <h3>Match Analysis</h3>
          <p>{data.summary}</p>
        </div>
      </div>
      <div className="score-bars">
        {Object.entries(data.categories).map(([key, val]) => (
          <ScoreBar key={key} label={CATEGORY_LABELS[key] || key} value={val} />
        ))}
      </div>
    </div>
  )
}
