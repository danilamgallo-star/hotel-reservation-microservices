import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { bookingService } from '../services/bookingService'
import './Confirmation.css'

export default function Confirmation() {
  const { bookingId } = useParams()
  const navigate = useNavigate()
  const [booking, setBooking] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadBooking()
  }, [bookingId])

  const loadBooking = async () => {
    try {
      const data = await bookingService.getBookingById(bookingId)
      setBooking(data)
    } catch (error) {
      console.error('Error cargando reserva:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) return <div className="loading">Cargando...</div>

  return (
    <div className="confirmation-page">
      <div className="confirmation-card card">
        <div className="success-icon">✅</div>
        <h1>¡Reserva Confirmada!</h1>
        <p className="confirmation-message">
          Tu reserva ha sido procesada exitosamente
        </p>

        {booking && (
          <div className="booking-details">
            <h2>Detalles de la Reserva</h2>
            <div className="detail-row">
              <span>ID de Reserva:</span>
              <strong>#{booking.id}</strong>
            </div>
            <div className="detail-row">
              <span>Habitación:</span>
              <strong>#{booking.room_id}</strong>
            </div>
            <div className="detail-row">
              <span>Check-in:</span>
              <strong>{new Date(booking.check_in_date).toLocaleDateString()}</strong>
            </div>
            <div className="detail-row">
              <span>Check-out:</span>
              <strong>{new Date(booking.check_out_date).toLocaleDateString()}</strong>
            </div>
            <div className="detail-row">
              <span>Huéspedes:</span>
              <strong>{booking.guests}</strong>
            </div>
            <div className="detail-row total">
              <span>Total Pagado:</span>
              <strong>${booking.total_price}</strong>
            </div>
          </div>
        )}

        <div className="actions">
          <button onClick={() => navigate('/my-bookings')} className="primary">
            Ver Mis Reservas
          </button>
          <button onClick={() => navigate('/search')} className="secondary">
            Buscar Más Habitaciones
          </button>
        </div>
      </div>
    </div>
  )
}
