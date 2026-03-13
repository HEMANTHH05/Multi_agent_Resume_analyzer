import { useCallback, useEffect, useRef, useState } from 'react'
import { AgentMessage, PipelineStep, WSMessage } from '../types'

let msgCounter = 0

export function useWebSocket(sessionId: string | null) {
  const wsRef = useRef<WebSocket | null>(null)
  const [connected, setConnected] = useState(false)
  const [messages, setMessages] = useState<AgentMessage[]>([])
  const [steps, setSteps] = useState<PipelineStep[]>([])
  const [waitingForInput, setWaitingForInput] = useState(false)
  const [inputPrompt, setInputPrompt] = useState('')
  const [downloadUrl, setDownloadUrl] = useState<string | null>(null)
  const [pipelineDone, setPipelineDone] = useState(false)
  const [pipelineError, setPipelineError] = useState<string | null>(null)

  const appendChunk = useCallback((agent: string, step_index: number, text: string) => {
    setMessages(prev => {
      const last = prev[prev.length - 1]
      if (last && last.agent === agent && last.type === 'chunk') {
        const updated = { ...last, text: (last.text || '') + text }
        return [...prev.slice(0, -1), updated]
      }
      return [
        ...prev,
        { id: `msg-${++msgCounter}`, agent, step_index, type: 'chunk', text },
      ]
    })
  }, [])

  const addMessage = useCallback((msg: AgentMessage) => {
    setMessages(prev => [...prev, { ...msg, id: `msg-${++msgCounter}` }])
  }, [])

  const handleMessage = useCallback(
    (raw: string) => {
      let msg: WSMessage
      try {
        msg = JSON.parse(raw)
      } catch {
        return
      }

      switch (msg.type) {
        case 'PIPELINE_STARTED':
          setSteps(
            msg.steps.map((name, i) => ({ name, step_index: i, status: 'idle' }))
          )
          break

        case 'AGENT_STARTED':
          setSteps(prev =>
            prev.map(s =>
              s.step_index === msg.step_index ? { ...s, status: 'active' } : s
            )
          )
          break

        case 'AGENT_COMPLETE':
          setSteps(prev =>
            prev.map(s =>
              s.step_index === msg.step_index ? { ...s, status: 'done' } : s
            )
          )
          break

        case 'AGENT_CHUNK':
          appendChunk(msg.agent, msg.step_index, msg.text)
          break

        case 'STRUCTURED_OUTPUT':
          addMessage({
            id: '',
            agent: msg.agent,
            step_index: msg.step_index,
            type: 'structured',
            dataKey: msg.key,
            data: msg.data,
          })
          break

        case 'AGENT_PAUSED':
          setSteps(prev =>
            prev.map(s =>
              s.step_index === msg.step_index ? { ...s, status: 'paused' } : s
            )
          )
          setWaitingForInput(true)
          setInputPrompt(msg.prompt)
          addMessage({
            id: '',
            agent: msg.agent,
            step_index: msg.step_index,
            type: 'pause',
            text: msg.prompt,
          })
          break

        case 'AGENT_RESUMED':
          setWaitingForInput(false)
          setInputPrompt('')
          setSteps(prev =>
            prev.map(s =>
              s.step_index === msg.step_index ? { ...s, status: 'active' } : s
            )
          )
          break

        case 'DOWNLOAD_READY':
          setDownloadUrl(msg.url)
          break

        case 'PIPELINE_COMPLETE':
          setPipelineDone(true)
          break

        case 'PIPELINE_ERROR':
          setPipelineError(msg.message)
          if (msg.agent) {
            setSteps(prev =>
              prev.map(s =>
                s.name === msg.agent ? { ...s, status: 'error' } : s
              )
            )
          }
          addMessage({
            id: '',
            agent: msg.agent || 'System',
            step_index: -1,
            type: 'error',
            text: msg.message,
          })
          break
      }
    },
    [appendChunk, addMessage]
  )

  const connect = useCallback(
    (jdText: string) => {
      if (!sessionId) return
      const ws = new WebSocket(`ws://localhost:8000/ws/${sessionId}`)
      wsRef.current = ws

      ws.onopen = () => {
        setConnected(true)
        ws.send(JSON.stringify({ type: 'START', jd_text: jdText }))
      }

      ws.onmessage = e => handleMessage(e.data)

      ws.onclose = () => {
        setConnected(false)
      }

      ws.onerror = () => {
        setPipelineError('WebSocket connection failed. Is the backend running?')
      }
    },
    [sessionId, handleMessage]
  )

  const sendReply = useCallback((text: string) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify({ type: 'USER_REPLY', text }))
      setWaitingForInput(false)
    }
  }, [])

  useEffect(() => {
    return () => {
      wsRef.current?.close()
    }
  }, [])

  return {
    connect,
    connected,
    messages,
    steps,
    waitingForInput,
    inputPrompt,
    downloadUrl,
    pipelineDone,
    pipelineError,
    sendReply,
  }
}
