import React, { useContext, useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, useNavigate } from 'react-router-dom';
import TabsBottomNavExample from './Menu';
import LoginPage from './Login';

const AuthContext = React.createContext(null);

function ProtectedRoute({ children }) {
  const { isAuthenticated } = useContext(AuthContext);
  return isAuthenticated ? children : <Navigate to="/login" replace />;
}

function RedirectIfAuthenticated() {
  const navigate = useNavigate();
  const { isAuthenticated } = useContext(AuthContext);

  useEffect(() => {
    if (isAuthenticated) {
      navigate('/menu'); // Redirect to /menu if authenticated
    }
  }, [isAuthenticated, navigate]);

  return null; // This component does not render anything, it just performs actions
}

function App() {
  const [isAuthenticated, setAuthenticated] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('token');
    setAuthenticated(!!token);
  }, []);

  return (
    <AuthContext.Provider value={{ isAuthenticated, setAuthenticated }}>
      <Router>
        <RedirectIfAuthenticated /> {/* This component handles the redirection logic */}
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/menu" element={
            <ProtectedRoute>
              <TabsBottomNavExample />
            </ProtectedRoute>
          } />
          <Route path="/" element={<Navigate to="/menu" replace />} />
        </Routes>
      </Router>
    </AuthContext.Provider>
  );
}

export default App;
