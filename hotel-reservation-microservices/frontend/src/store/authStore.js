import { create } from 'zustand'
import { authService } from '../services/authService'

export const useAuthStore = create((set) => ({
  user: null,
  token: localStorage.getItem('token'),
  
  login: async (email, password) => {
    const data = await authService.login(email, password)
    localStorage.setItem('token', data.access_token)
    const user = await authService.getProfile()
    set({ user, token: data.access_token })
  },
  
  register: async (email, password, fullName) => {
    await authService.register(email, password, fullName)
  },
  
  logout: () => {
    localStorage.removeItem('token')
    set({ user: null, token: null })
  },
  
  loadUser: async () => {
    const token = localStorage.getItem('token')
    if (token) {
      try {
        const user = await authService.getProfile()
        set({ user, token })
      } catch (error) {
        localStorage.removeItem('token')
        set({ user: null, token: null })
      }
    }
  }
}))
