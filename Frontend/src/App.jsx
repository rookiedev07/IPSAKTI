import React from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Main from './Pages/Main'

const App = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Main />} />
        <Route path="/main" element={<Main />} />
        {/* Redirect legacy routes to the single console */}
        <Route path="/login" element={<Navigate to="/" replace />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App