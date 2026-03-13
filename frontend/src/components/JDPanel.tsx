import { useState } from 'react'

interface Props {
  onStart: (jdText: string) => void
  hasSession: boolean
  running: boolean
}

export function JDPanel({ onStart, hasSession, running }: Props) {
  const [jdText, setJdText] = useState('')

  const canStart = hasSession && jdText.trim().length > 50 && !running

  return (
    <div className="panel jd-panel">
      <h2 className="panel-title">
        <span className="panel-icon">💼</span> Job Description
      </h2>

      <textarea
        className="jd-textarea"
        placeholder="Paste the full job description here...&#10;&#10;Include all requirements, skills, responsibilities, and any keywords from the posting."
        value={jdText}
        onChange={e => setJdText(e.target.value)}
        disabled={running}
      />

      <div className="jd-footer">
        <span className="char-count">{jdText.length} characters</span>
        <button
          className={`start-btn ${canStart ? 'start-btn-active' : ''}`}
          disabled={!canStart}
          onClick={() => onStart(jdText)}
        >
          {running ? (
            <>
              <span className="btn-spinner" /> Processing...
            </>
          ) : (
            <>Start Analysis →</>
          )}
        </button>
      </div>

      {!hasSession && jdText.length > 0 && (
        <p className="hint-text">Upload your resume first to enable analysis</p>
      )}
      {hasSession && jdText.trim().length <= 50 && jdText.length > 0 && (
        <p className="hint-text">Paste the complete job description (at least 50 characters)</p>
      )}
    </div>
  )
}
