import React, { createContext, useContext, useState, useEffect } from 'react';
import api from './api';

// Create the authentication context
const AuthContext = createContext();

// Custom hook to use the auth context
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

// AuthProvider component
export const AuthProvider = ({ children }) => {
  const [userId, setUserId] = useState(null);
  const [token, setToken] = useState(null);

  // Check for existing token and userId on mount
  useEffect(() => {
    const storedToken = localStorage.getItem('token');
    const storedUserId = localStorage.getItem('userId');
    
    if (storedToken && storedUserId) {
      setToken(storedToken);
      setUserId(storedUserId);
    }
  }, []);

  // Login function
  const login = async (loginData) => {
    try {
      const response = await api.post('/auth/login', loginData);
      const { token, userId } = response.data;
      
      // Store token and userId in state
      setToken(token);
      setUserId(userId);
      
      // Store in local storage
      localStorage.setItem('token', token);
      localStorage.setItem('userId', userId);
      
      return { success: true, data: response.data };
    } catch (error) {
      return { success: false, error: error.response?.data?.message || 'Login failed' };
    }
  };

  // Logout function
  const logout = async () => {
    try {
      // Only call logout API if user is actually logged in
      if (userId) {
        await api.post('/auth/logout', { userId });
      }
    } catch (error) {
      console.error('Logout error:', error);
      // Continue with logout even if API call fails
    } finally {
      // Clear state
      setToken(null);
      setUserId(null);
      
      // Remove from local storage
      localStorage.removeItem('token');
      localStorage.removeItem('userId');
    }
  };

  const value = {
    userId,
    token,
    login,
    logout
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthContext;