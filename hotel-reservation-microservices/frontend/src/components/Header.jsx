import { Link } from 'react-router-dom'
import './Header.css'

export default function Header() {
  return (
    <header className="header">
      <div className="header-content">
        <Link to="/" className="logo">
          <h1>🏨 Hotel Reservations</h1>
        </Link>
        
        <nav className="nav">
          <Link to="/search">Buscar</Link>
          <Link to="/my-bookings">Mis Reservas</Link>
        </nav>
      </div>
    </header>
  )
}
