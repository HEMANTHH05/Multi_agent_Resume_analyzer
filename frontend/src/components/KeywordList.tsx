import { KeywordItem } from '../types'

interface Props {
  data: KeywordItem[]
}

export function KeywordList({ data }: Props) {
  const red = data.filter(k => k.flag === 'RED')
  const yellow = data.filter(k => k.flag === 'YELLOW')

  return (
    <div className="keyword-list-card">
      <h3 className="keyword-list-title">Keyword Gap Analysis</h3>
      <div className="keyword-columns">
        <div className="keyword-col">
          <div className="keyword-col-header red-header">
            🔴 Completely Missing ({red.length})
          </div>
          {red.map((k, i) => (
            <div key={i} className="keyword-item keyword-red">
              <span className="keyword-term">{k.term}</span>
              <span className="keyword-reason">{k.reason}</span>
            </div>
          ))}
        </div>
        <div className="keyword-col">
          <div className="keyword-col-header yellow-header">
            🟡 Needs Reframing ({yellow.length})
          </div>
          {yellow.map((k, i) => (
            <div key={i} className="keyword-item keyword-yellow">
              <span className="keyword-term">{k.term}</span>
              <span className="keyword-reason">{k.reason}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
