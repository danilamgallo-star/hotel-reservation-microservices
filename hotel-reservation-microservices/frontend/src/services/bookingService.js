import api from './api'

export const bookingService = {
  async createBooking(bookingData) {
    const response = await api.post('/api/bookings/', bookingData)
    return response.data
  },

  async getMyBookings() {
    const response = await api.get('/api/bookings/my-bookings')
    return response.data
  },

  async getBookingById(id) {
    const response = await api.get(`/api/bookings/${id}`)
    return response.data
  },

  async cancelBooking(id) {
    const response = await api.put(`/api/bookings/${id}/cancel`)
    return response.data
  }
}
