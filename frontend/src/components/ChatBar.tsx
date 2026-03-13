import { useState, KeyboardEvent } from 'react'

interface Props {
  waitingForInput: boolean
  inputPrompt: string
  onSend: (text: string) => void
  downloadUrl: string | null
  pipelineDone: boolean
}

export function ChatBar({ waitingForInput, onSend, downloadUrl, pipelineDone }: Props) {
  const [text, setText] = useState('')

  const handleSend = () => {
    if (!text.trim()) return
    onSend(text.trim())
    setText('')
  }

  const handleKey = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div className="chatbar-wrap">
      {waitingForInput && (
        <div className="input-banner">
          <span className="banner-icon">⏸</span>
          Agent is waiting for your input — type your reply below
        </div>
      )}

      {pipelineDone && downloadUrl && (
        <div className="download-banner">
          <span>🎉 Your tailored resume is ready!</span>
          <a href={downloadUrl} download="tailored_resume.docx" className="download-btn">
            ⬇️ Download Resume (.docx)
          </a>
        </div>
      )}

      <div className={`chatbar ${waitingForInput ? 'chatbar-active' : 'chatbar-idle'}`}>
        <textarea
          className="chat-input"
          placeholder={
            waitingForInput
              ? 'Type your reply here... (Enter to send)'
              : 'Start a new analysis by uploading a resume and pasting a JD above'
          }
          value={text}
          onChange={e => setText(e.target.value)}
          onKeyDown={handleKey}
          disabled={!waitingForInput}
          rows={1}
        />
        <button
          className={`send-btn ${waitingForInput && text.trim() ? 'send-btn-active' : ''}`}
          onClick={handleSend}
          disabled={!waitingForInput || !text.trim()}
        >
          ➤
        </button>
      </div>
    </div>
  )
}
