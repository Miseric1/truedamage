import Home from './pages/Home'

// App.tsx will eventually own routing (React Router) once there's more than
// one page. Keeping it a dumb pass-through now avoids guessing at a routing
// structure before there's a second page to justify it.
function App() {
  return <Home />
}

export default App
