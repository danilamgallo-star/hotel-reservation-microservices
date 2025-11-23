import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { roomsService } from '../services/roomsService'
import { bookingService } from '../services/bookingService'
import { paymentService } from '../services/paymentService'
import './RoomDetail.css'

export default function RoomDetail() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [room, setRoom] = useState(null)
  const [loading, setLoading] = useState(true)
  const [booking, setBooking] = useState({
    checkIn: '',
    checkOut: '',
    guests: 1
  })
  const [processing, setProcessing] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    loadRoom()
  }, [id])

  const loadRoom = async () => {
    try {
      const data = await roomsService.getRoomById(id)
      setRoom(data)
    } catch (error) {
      setError('No se pudo cargar la habitación')
    } finally {
      setLoading(false)
    }
  }

  const handleBooking = async (e) => {
    e.preventDefault()
    setProcessing(true)
    setError('')

    try {
      // Crear reserva
      const bookingData = {
        room_id: parseInt(id),
        check_in_date: booking.checkIn,
        check_out_date: booking.checkOut,
        guests: parseInt(booking.guests),
        total_price: calculateTotal()
      }
      
      const newBooking = await bookingService.createBooking(bookingData)
      
      // Procesar pago
      await paymentService.processPayment({
        booking_id: newBooking.id,
        amount: calculateTotal(),
        payment_method: 'credit_card'
      })
      
      navigate(`/confirmation/${newBooking.id}`)
    } catch (err) {
      setError(err.response?.data?.detail || 'Error al crear la reserva')
    } finally {
      setProcessing(false)
    }
  }

  const calculateTotal = () => {
    if (!booking.checkIn || !booking.checkOut || !room) return 0
    const days = Math.ceil((new Date(booking.checkOut) - new Date(booking.checkIn)) / (1000 * 60 * 60 * 24))
    return days * room.price_per_night
  }

  if (loading) return <div className="loading">Cargando...</div>
  if (!room) return <div className="error">Habitación no encontrada</div>

  return (
    <div className="room-detail">
      <div className="room-info card">
        <div className="room-header">
          <h1>Habitación {room.room_number}</h1>
          <p className="room-type">{room.room_type}</p>
        </div>
        
        <div className="room-image-large">
          🏨
        </div>
        
        <div className="room-specs">
          <p><strong>Precio:</strong> ${room.price_per_night} por noche</p>
          <p><strong>Capacidad:</strong> {room.capacity} personas</p>
          <p><strong>Estado:</strong> {room.is_available ? '✅ Disponible' : '❌ No disponible'}</p>
        </div>
      </div>

      <div className="booking-form card">
        <h2>Hacer Reserva</h2>
        
        {error && <div className="error">{error}</div>}
        
        <form onSubmit={handleBooking}>
          <div className="form-group">
            <label>Check-in</label>
            <input
              type="date"
              value={booking.checkIn}
              onChange={(e) => setBooking({...booking, checkIn: e.target.value})}
              required
              min={new Date().toISOString().split('T')[0]}
            />
          </div>
          
          <div className="form-group">
            <label>Check-out</label>
            <input
              type="date"
              value={booking.checkOut}
              onChange={(e) => setBooking({...booking, checkOut: e.target.value})}
              required
              min={booking.checkIn || new Date().toISOString().split('T')[0]}
            />
          </div>
          
          <div className="form-group">
            <label>Huéspedes</label>
            <input
              type="number"
              min="1"
              max={room.capacity}
              value={booking.guests}
              onChange={(e) => setBooking({...booking, guests: e.target.value})}
              required
            />
          </div>
          
          {booking.checkIn && booking.checkOut && (
            <div className="total-price">
              <h3>Total: ${calculateTotal()}</h3>
            </div>
          )}
          
          <button 
            type="submit" 
            className="primary" 
            disabled={processing || !room.is_available}
          >
            {processing ? 'Procesando...' : 'Confirmar Reserva'}
          </button>
        </form>
      </div>
    </div>
  )
}
