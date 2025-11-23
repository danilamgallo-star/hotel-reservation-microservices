import { useEffect, useState } from 'react'
import { bookingService } from '../services/bookingService'
import './MyBookings.css'

export default function MyBookings() {
  const [bookings, setBookings] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadBookings()
  }, [])

  const loadBookings = async () => {
    try {
      const data = await bookingService.getMyBookings()
      setBookings(data)
    } catch (error) {
      console.error('Error cargando reservas:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleCancel = async (id) => {
    if (!confirm('¿Seguro que querés cancelar esta reserva?')) return
    
    try {
      await bookingService.cancelBooking(id)
      loadBookings()
    } catch (error) {
      alert('No se pudo cancelar la reserva')
    }
  }

  if (loading) return <div className="loading">Cargando reservas...</div>

  return (
    <div className="my-bookings">
      <h1>Mis Reservas</h1>
      
      {bookings.length === 0 ? (
        <div className="no-bookings card">
          <p>No tenés reservas todavía</p>
        </div>
      ) : (
        <div className="bookings-list">
          {bookings.map(booking => (
            <div key={booking.id} className="booking-card card">
              <div className="booking-header">
                <h3>Reserva #{booking.id}</h3>
                <span className={`status status-${booking.status}`}>
                  {booking.status}
                </span>
              </div>
              
              <div className="booking-info">
                <div className="info-row">
                  <span>Habitación:</span>
                  <strong>#{booking.room_id}</strong>
                </div>
                <div className="info-row">
                  <span>Check-in:</span>
                  <strong>{new Date(booking.check_in_date).toLocaleDateString()}</strong>
                </div>
                <div className="info-row">
                  <span>Check-out:</span>
                  <strong>{new Date(booking.check_out_date).toLocaleDateString()}</strong>
                </div>
                <div className="info-row">
                  <span>Huéspedes:</span>
                  <strong>{booking.guests}</strong>
                </div>
                <div className="info-row">
                  <span>Total:</span>
                  <strong>${booking.total_price}</strong>
                </div>
              </div>
              
              {booking.status === 'confirmed' && (
                <button 
                  onClick={() => handleCancel(booking.id)}
                  className="cancel-btn"
                >
                  Cancelar Reserva
                </button>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
