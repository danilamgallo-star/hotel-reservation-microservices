import api from './api'

export const paymentService = {
  async processPayment(paymentData) {
    const response = await api.post('/api/payments/', paymentData)
    return response.data
  },

  async getPaymentStatus(paymentId) {
    const response = await api.get(`/api/payments/${paymentId}`)
    return response.data
  }
}
