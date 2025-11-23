import api from './api'

export const authService = {
  async login(email, password) {
    const formData = new FormData()
    formData.append('username', email)
    formData.append('password', password)
    
    const response = await api.post('/api/auth/token', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    return response.data
  },

  async register(email, password, fullName) {
    const response = await api.post('/api/auth/register', {
      email,
      password,
      full_name: fullName
    })
    return response.data
  },

  async getProfile() {
    const response = await api.get('/api/auth/users/me')
    return response.data
  }
}
