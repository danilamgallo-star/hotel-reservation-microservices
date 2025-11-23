import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import Search from './pages/Search'
import RoomDetail from './pages/RoomDetail'
import Confirmation from './pages/Confirmation'
import MyBookings from './pages/MyBookings'
import Header from './components/Header'

function App() {
  return (
    <Router>
      <div className="app">
        <Header />
        <main className="main-content">
          <Routes>
            <Route path="/search" element={<Search />} />
            <Route path="/room/:id" element={<RoomDetail />} />
            <Route path="/confirmation/:bookingId" element={<Confirmation />} />
            <Route path="/my-bookings" element={<MyBookings />} />
            <Route path="/" element={<Navigate to="/search" />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App
