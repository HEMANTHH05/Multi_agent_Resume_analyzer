import { useState } from 'react'
import { TopBar } from './components/TopBar'
import { UploadPanel } from './components/UploadPanel'
import { JDPanel } from './components/JDPanel'
import { AgentFeed } from './components/AgentFeed'
import { ChatBar } from './components/ChatBar'
import { useWebSocket } from './hooks/useWebSocket'

export default function App() {
  const [sessionId, setSessionId] = useState<string | null>(null)
  const [running, setRunning] = useState(false)
  const [started, setStarted] = useState(false)

  const {
    connect,
    messages,
    steps,
    waitingForInput,
    inputPrompt,
    downloadUrl,
    pipelineDone,
    pipelineError,
    sendReply,
  } = useWebSocket(sessionId)

  const handleUploaded = (id: string) => {
    setSessionId(id)
  }

  const handleStart = (jdText: string) => {
    if (!sessionId) return
    setRunning(true)
    setStarted(true)
    connect(jdText)
  }

  return (
    <div className="app">
      <TopBar steps={steps} />

      <main className="main-layout">
        {/* Input panels — shown until pipeline starts, then collapse */}
        {!started && (
          <div className="input-row">
            <UploadPanel onUploaded={handleUploaded} disabled={running} />
            <JDPanel onStart={handleStart} hasSession={!!sessionId} running={running} />
          </div>
        )}

        {/* Agent feed */}
        {started && (
          <div className="feed-area">
            {pipelineError && (
              <div className="pipeline-error-banner">
                ❌ {pipelineError}
              </div>
            )}
            <AgentFeed messages={messages} />
          </div>
        )}
      </main>

      <ChatBar
        waitingForInput={waitingForInput}
        inputPrompt={inputPrompt}
        onSend={sendReply}
        downloadUrl={downloadUrl}
        pipelineDone={pipelineDone}
      />
    </div>
  )
}
