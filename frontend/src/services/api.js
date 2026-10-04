import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

const getErrorMessage = (error) => {
  const detail = error.response?.data?.detail

  if (Array.isArray(detail)) {
    return detail.map((validationError) => validationError.msg).join(', ')
  }

  return detail || error.message || 'Something went wrong. Please try again.'
}

const request = async (requestConfig) => {
  try {
    const response = await api.request(requestConfig)
    return response.data
  } catch (error) {
    throw new Error(getErrorMessage(error), { cause: error })
  }
}

export const registerUser = (user) =>
  request({
    url: '/auth/register',
    method: 'POST',
    data: user,
  })

export const loginUser = (credentials) =>
  request({
    url: '/auth/login',
    method: 'POST',
    data: credentials,
  })

export const getCurrentUser = (token) =>
  request({
    url: '/auth/me',
    method: 'GET',
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })
