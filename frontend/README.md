# Frontend

Aquí va la app de React.

## Estructura

```
frontend/
├── src/
│   ├── components/      # Reusable UI components
│   ├── pages/          # Page components
│   ├── services/       # API service calls
│   ├── store/          # State management (Zustand)
│   ├── hooks/          # Custom React hooks
│   ├── utils/          # Utility functions
│   └── App.jsx         # Main App component
├── public/             # Static assets
└── package.json        # Dependencies
```

## Páginas principales

1. **Login/Register** - Para entrar o crear cuenta
2. **Búsqueda** - Buscar habitaciones con filtros
3. **Detalle** - Ver la habitación y hacer reserva
4. **Confirmación** - Cuando ya reservaste
5. **Mis Reservas** - Historial de reservas del usuario

## Stack

- React 18
- React Router para navegar
- Axios para llamar a la API
- Zustand para manejar estado (más simple que Redux)
- Vite para compilar (más rápido que webpack)
