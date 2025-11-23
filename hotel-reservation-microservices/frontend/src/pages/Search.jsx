import { useState, useEffect } from 'react'
import { roomsService } from '../services/roomsService'
import { useNavigate } from 'react-router-dom'
import './Search.css'

export default function Search() {
  const [rooms, setRooms] = useState([])
  const [loading, setLoading] = useState(true)
  const [filters, setFilters] = useState({
    checkIn: '',
    checkOut: '',
    guests: '',
    roomType: ''
  })
  
  const navigate = useNavigate()

  useEffect(() => {
    loadRooms()
  }, [])

  const loadRooms = async () => {
    try {
      setLoading(true)
      const data = await roomsService.searchRooms(filters)
      setRooms(data)
    } catch (error) {
      console.error('Error cargando habitaciones:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSearch = (e) => {
    e.preventDefault()
    loadRooms()
  }

  return (
    <div className="search-page">
      <div className="search-filters card">
        <h2>Buscar Habitaciones</h2>
        <form onSubmit={handleSearch}>
          <div className="filters-grid">
            <div className="form-group">
              <label>Check-in</label>
              <input
                type="date"
                value={filters.checkIn}
                onChange={(e) => setFilters({...filters, checkIn: e.target.value})}
              />
            </div>
            
            <div className="form-group">
              <label>Check-out</label>
              <input
                type="date"
                value={filters.checkOut}
                onChange={(e) => setFilters({...filters, checkOut: e.target.value})}
              />
            </div>
            
            <div className="form-group">
              <label>Huéspedes</label>
              <input
                type="number"
                min="1"
                value={filters.guests}
                onChange={(e) => setFilters({...filters, guests: e.target.value})}
                placeholder="Cantidad"
              />
            </div>
            
            <div className="form-group">
              <label>Tipo</label>
              <select
                value={filters.roomType}
                onChange={(e) => setFilters({...filters, roomType: e.target.value})}
              >
                <option value="">Todos</option>
                <option value="single">Individual</option>
                <option value="double">Doble</option>
                <option value="suite">Suite</option>
              </select>
            </div>
          </div>
          
          <button type="submit" className="primary">Buscar</button>
        </form>
      </div>

      {loading ? (
        <div className="loading">Cargando habitaciones...</div>
      ) : (
        <div className="rooms-grid">
          {rooms.map(room => (
            <div key={room.id} className="room-card card" onClick={() => navigate(`/room/${room.id}`)}>
              <div className="room-image">
                🏨
              </div>
              <h3>{room.room_number} - {room.room_type}</h3>
              <p className="room-price">${room.price_per_night} / noche</p>
              <p>Capacidad: {room.capacity} personas</p>
              <p className="room-status">
                {room.is_available ? '✅ Disponible' : '❌ No disponible'}
              </p>
            </div>
          ))}
        </div>
      )}
      
      {!loading && rooms.length === 0 && (
        <div className="no-results card">
          <p>No se encontraron habitaciones con estos filtros</p>
        </div>
      )}
    </div>
  )
}
