import { useEffect, useState } from 'react'
import { getHealth } from '../api/client'

type ConnectionStatus = 'checking' | 'connected' | 'error'

/**
 * This page exists purely to prove the stack is wired together end to end:
 * React renders, calls FastAPI, FastAPI responds. Nothing about summoners,
 * matches, or Riot data belongs here yet — that's follow-on feature work
 * once this base is confirmed working.
 */
function Home() {
  const [status, setStatus] = useState<ConnectionStatus>('checking')
  const [detail, setDetail] = useState<string>('')

  useEffect(() => {
    getHealth()
      .then((data) => {
        setStatus('connected')
        setDetail(data.status)
      })
      .catch((err: unknown) => {
        setStatus('error')
        setDetail(err instanceof Error ? err.message : 'Unknown error')
      })
  }, [])

  return (
    <main style={{ fontFamily: 'sans-serif', padding: '2rem' }}>
      <h1>LoL Analytics Platform</h1>
      <p>
        Backend connection status: <strong>{status}</strong>
      </p>
      {detail && <p>Detail: {detail}</p>}
    </main>
  )
}

export default Home
