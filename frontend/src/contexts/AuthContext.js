import React, { createContext, useContext, useState, useEffect } from 'react';
import { api } from '../services/api';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [config, setConfig] = useState({
    phantomBusterApiKey: '',
    deepSeekApiKey: '',
    phantomId: '',
  });

  useEffect(() => {
    checkAuth();
    loadConfig();
  }, []);

  const checkAuth = async () => {
    try {
      // For now, we'll just check if the system is configured
      const response = await api.get('/health');
      if (response.data.status === 'ok') {
        setUser({ name: 'Admin User', role: 'admin' });
      }
    } catch (error) {
      console.log('System not configured yet');
    } finally {
      setLoading(false);
    }
  };

  const loadConfig = async () => {
    try {
      const response = await api.get('/config');
      setConfig(response.data);
    } catch (error) {
      console.log('Config not loaded');
    }
  };

  const updateConfig = async (newConfig) => {
    try {
      const response = await api.post('/config', newConfig);
      setConfig(response.data);
      return { success: true };
    } catch (error) {
      return { success: false, error: error.response?.data?.message || 'Failed to update configuration' };
    }
  };

  const logout = () => {
    setUser(null);
  };

  const value = {
    user,
    loading,
    config,
    updateConfig,
    logout,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}; 