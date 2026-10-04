import { useState } from 'react'
import { useFormik } from 'formik'
import { FiEye, FiEyeOff } from 'react-icons/fi'
import { toast } from 'react-toastify'
import { getCurrentUser, loginUser, registerUser } from '../../services/api'

const initialValues = {
  username: '',
  email: '',
  password: '',
  role: 'student',
}

const AuthPage = ({ onLogin }) => {
  const [mode, setMode] = useState('login')
  const [showPassword, setShowPassword] = useState(false)

  const isRegistering = mode === 'register'

  const validate = (values) => {
    const errors = {}

    if (!values.username.trim()) {
      errors.username = 'Username is required.'
    } else if (values.username.trim().length < 3) {
      errors.username = 'Username must be at least 3 characters.'
    } else if (values.username.trim().length > 50) {
      errors.username = 'Username must be 50 characters or fewer.'
    }

    if (isRegistering) {
      if (!values.email.trim()) {
        errors.email = 'Email is required.'
      } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(values.email)) {
        errors.email = 'Enter a valid email address.'
      }

      if (!values.password) {
        errors.password = 'Password is required.'
      } else if (values.password.length < 8) {
        errors.password = 'Password must be at least 8 characters.'
      } else if (values.password.length > 128) {
        errors.password = 'Password must be 128 characters or fewer.'
      }
    } else if (!values.password) {
      errors.password = 'Password is required.'
    }

    return errors
  }

  const formik = useFormik({
    initialValues,
    validate,
    validateOnBlur: true,
    validateOnChange: false,
    onSubmit: async (values, { resetForm, setFieldValue }) => {
      try {
        if (isRegistering) {
          await registerUser({
            username: values.username.trim(),
            email: values.email.trim(),
            password: values.password,
            role: values.role,
          })
          toast.success('Registration successful. You can now log in.')
          resetForm({
            values: {
              ...initialValues,
              username: values.username,
            },
          })
          setMode('login')
        } else {
          const response = await loginUser({
            username: values.username.trim(),
            password: values.password,
          })
          localStorage.setItem('access_token', response.access_token)
          const currentUser = await getCurrentUser(response.access_token)
          toast.success('Login successful.')
          await new Promise((resolve) => setTimeout(resolve, 5000))
          onLogin(currentUser.username, currentUser.role)
        }
      } catch (error) {
        toast.error(error.message)
      } finally {
        setFieldValue('password', '')
      }
    },
  })

  const switchMode = () => {
    setMode((currentMode) => (currentMode === 'login' ? 'register' : 'login'))
    setShowPassword(false)
    formik.resetForm({ values: initialValues })
  }

  const showError = (field) => formik.touched[field] && formik.errors[field]

  return (
    <main className="auth-page">
      <section className="auth-card" aria-labelledby="auth-title">
        <div className="auth-heading">
          <h1 id="auth-title">{isRegistering ? 'Create your account' : 'Welcome back'}</h1>
          <p className="auth-description">
            {isRegistering
              ? 'Sign up to get started with your school workspace.'
              : 'Sign in to continue to your school workspace.'}
          </p>
        </div>

        <form onSubmit={formik.handleSubmit} noValidate>
          <label htmlFor="username">Username</label>
          <input
            id="username"
            name="username"
            value={formik.values.username}
            onChange={formik.handleChange}
            onBlur={formik.handleBlur}
            placeholder="Enter your username"
            autoComplete="username"
            required
            disabled={formik.isSubmitting}
            aria-invalid={Boolean(showError('username'))}
          />
          {showError('username') && <span className="field-error">{formik.errors.username}</span>}

          {isRegistering && (
            <>
              <label htmlFor="email">Email address</label>
              <input
                id="email"
                name="email"
                type="email"
                value={formik.values.email}
                onChange={formik.handleChange}
                onBlur={formik.handleBlur}
                placeholder="you@example.com"
                autoComplete="email"
                required
                disabled={formik.isSubmitting}
                aria-invalid={Boolean(showError('email'))}
              />
              {showError('email') && <span className="field-error">{formik.errors.email}</span>}
            </>
          )}

          <label htmlFor="password">Password</label>
          <div className="password-field">
            <input
              id="password"
              name="password"
              type={showPassword ? 'text' : 'password'}
              value={formik.values.password}
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              placeholder="Enter your password"
              autoComplete={isRegistering ? 'new-password' : 'current-password'}
              required
              disabled={formik.isSubmitting}
              aria-invalid={Boolean(showError('password'))}
            />
            <button
              className="password-toggle"
              type="button"
              onClick={() => setShowPassword((visible) => !visible)}
              disabled={formik.isSubmitting}
              aria-label={showPassword ? 'Hide password' : 'Show password'}
            >
              {showPassword ? <FiEyeOff aria-hidden="true" /> : <FiEye aria-hidden="true" />}
            </button>
          </div>
          {showError('password') && <span className="field-error">{formik.errors.password}</span>}

          {!isRegistering && (
            <a className="forgot-password" href="#forgot-password" onClick={(event) => event.preventDefault()}>
              Forgot password?
            </a>
          )}

          {isRegistering && (
            <>
              <label htmlFor="role">Role</label>
              <select
                id="role"
                name="role"
                value={formik.values.role}
                onChange={formik.handleChange}
                onBlur={formik.handleBlur}
                disabled={formik.isSubmitting}
              >
                <option value="student">Student</option>
                <option value="teacher">Teacher</option>
              </select>
            </>
          )}

          <button className="submit-button" type="submit" disabled={formik.isSubmitting}>
            {formik.isSubmitting ? (
              <>
                <span className="spinner" aria-hidden="true" />
                {isRegistering ? 'Creating account...' : 'Signing in...'}
              </>
            ) : (
              isRegistering ? 'Create account' : 'Sign in'
            )}
          </button>
        </form>

        <p className="auth-switch">
          {isRegistering ? 'Already have an account?' : "Don't have an account?"}{' '}
          <button type="button" onClick={switchMode} disabled={formik.isSubmitting}>
            {isRegistering ? 'Sign in' : 'Sign up'}
          </button>
        </p>
      </section>
    </main>
  )
}

export default AuthPage
