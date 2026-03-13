import { useRef, useState, DragEvent } from 'react'

interface Props {
  onUploaded: (sessionId: string, filename: string) => void
  disabled: boolean
}

export function UploadPanel({ onUploaded, disabled }: Props) {
  const [dragging, setDragging] = useState(false)
  const [uploading, setUploading] = useState(false)
  const [uploadedFile, setUploadedFile] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)
  const inputRef = useRef<HTMLInputElement>(null)

  const handleFile = async (file: File) => {
    if (!file) return
    const ext = file.name.split('.').pop()?.toLowerCase()
    if (!['pdf', 'docx', 'doc'].includes(ext || '')) {
      setError('Only PDF and DOCX files are supported.')
      return
    }
    setError(null)
    setUploading(true)
    try {
      const form = new FormData()
      form.append('file', file)
      const res = await fetch('/upload', { method: 'POST', body: form })
      const data = await res.json()
      if (data.session_id) {
        setUploadedFile(file.name)
        onUploaded(data.session_id, file.name)
      } else {
        setError('Upload failed. Please try again.')
      }
    } catch {
      setError('Upload failed. Is the backend running?')
    } finally {
      setUploading(false)
    }
  }

  const onDrop = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault()
    setDragging(false)
    if (disabled) return
    const file = e.dataTransfer.files[0]
    if (file) handleFile(file)
  }

  return (
    <div className="panel upload-panel">
      <h2 className="panel-title">
        <span className="panel-icon">📄</span> Your Resume
      </h2>

      <div
        className={`drop-zone ${dragging ? 'dragging' : ''} ${uploadedFile ? 'uploaded' : ''} ${disabled ? 'zone-disabled' : ''}`}
        onDragOver={e => { e.preventDefault(); if (!disabled) setDragging(true) }}
        onDragLeave={() => setDragging(false)}
        onDrop={onDrop}
        onClick={() => !disabled && !uploadedFile && inputRef.current?.click()}
      >
        <input
          ref={inputRef}
          type="file"
          accept=".pdf,.docx,.doc"
          style={{ display: 'none' }}
          onChange={e => e.target.files?.[0] && handleFile(e.target.files[0])}
        />

        {uploading ? (
          <div className="drop-zone-content">
            <div className="spinner" />
            <p>Uploading...</p>
          </div>
        ) : uploadedFile ? (
          <div className="drop-zone-content uploaded-content">
            <div className="file-icon">✅</div>
            <p className="file-name">{uploadedFile}</p>
            <p className="file-status">Ready to process</p>
          </div>
        ) : (
          <div className="drop-zone-content">
            <div className="upload-icon">⬆️</div>
            <p className="drop-text">Drop your resume here</p>
            <p className="drop-subtext">or click to browse</p>
            <p className="drop-formats">PDF · DOCX</p>
          </div>
        )}
      </div>

      {error && <p className="error-text">{error}</p>}
    </div>
  )
}
