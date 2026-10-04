import { useState } from 'react'
import { ToastContainer } from 'react-toastify'
import AuthPage from '../features/auth/AuthPage'
import Dashboard from '../features/dashboard/Dashboard'
import 'react-toastify/dist/ReactToastify.css'

const App = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(
    () => Boolean(localStorage.getItem('access_token')),
  )
  const [username, setUsername] = useState(() => localStorage.getItem('username') || 'User')
  const [role, setRole] = useState(() => localStorage.getItem('user_role') || 'User')

  const handleLogin = (loggedInUsername, loggedInRole) => {
    setUsername(loggedInUsername)
    setRole(loggedInRole)
    localStorage.setItem('username', loggedInUsername)
    localStorage.setItem('user_role', loggedInRole)
    setIsAuthenticated(true)
  }

  const handleLogout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('username')
    localStorage.removeItem('user_role')
    setIsAuthenticated(false)
  }

  return (
    <>
      {isAuthenticated ? (
        <Dashboard username={username} role={role} onLogout={handleLogout} />
      ) : (
        <AuthPage onLogin={handleLogin} />
      )}
      <ToastContainer position="top-center" autoClose={4000} newestOnTop />
    </>
  )
}

export default App
