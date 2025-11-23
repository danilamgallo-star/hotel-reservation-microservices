import api from './api'

export const roomsService = {
  async searchRooms(filters = {}) {
    const params = new URLSearchParams()
    if (filters.checkIn) params.append('check_in', filters.checkIn)
    if (filters.checkOut) params.append('check_out', filters.checkOut)
    if (filters.guests) params.append('guests', filters.guests)
    if (filters.roomType) params.append('room_type', filters.roomType)
    
    const response = await api.get(`/api/rooms/search?${params.toString()}`)
    return response.data
  },

  async getRoomById(id) {
    const response = await api.get(`/api/rooms/${id}`)
    return response.data
  },

  async checkAvailability(roomId, checkIn, checkOut) {
    const response = await api.get(`/api/rooms/${roomId}/availability`, {
      params: { check_in: checkIn, check_out: checkOut }
    })
    return response.data
  }
}
