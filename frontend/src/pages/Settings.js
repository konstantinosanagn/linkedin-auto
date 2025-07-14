import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import toast from 'react-hot-toast';

const Settings = () => {
  const { config, updateConfig } = useAuth();
  const [formData, setFormData] = useState({
    phantomBusterApiKey: '',
    deepSeekApiKey: '',
    phantomId: '',
  });
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (config) {
      setFormData({
        phantomBusterApiKey: config.phantomBusterApiKey || '',
        deepSeekApiKey: config.deepSeekApiKey || '',
        phantomId: config.phantomId || '',
      });
    }
  }, [config]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const result = await updateConfig(formData);
      if (result.success) {
        toast.success('Configuration updated successfully');
      } else {
        toast.error(result.error || 'Failed to update configuration');
      }
    } catch (error) {
      console.error('Error updating config:', error);
      toast.error('Failed to update configuration');
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Settings</h1>
        <p className="mt-1 text-sm text-gray-500">
          Configure your API keys and system settings
        </p>
      </div>

      {/* Configuration Form */}
      <div className="card">
        <div className="card-header">
          <h3 className="text-lg font-medium text-gray-900">API Configuration</h3>
        </div>
        <div className="card-body">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label htmlFor="phantomBusterApiKey" className="block text-sm font-medium text-gray-700">
                PhantomBuster API Key
              </label>
              <input
                type="password"
                name="phantomBusterApiKey"
                id="phantomBusterApiKey"
                value={formData.phantomBusterApiKey}
                onChange={handleChange}
                className="input mt-1"
                placeholder="Enter your PhantomBuster API key"
              />
              <p className="mt-1 text-sm text-gray-500">
                Get your API key from the PhantomBuster dashboard
              </p>
            </div>

            <div>
              <label htmlFor="deepSeekApiKey" className="block text-sm font-medium text-gray-700">
                DeepSeek API Key
              </label>
              <input
                type="password"
                name="deepSeekApiKey"
                id="deepSeekApiKey"
                value={formData.deepSeekApiKey}
                onChange={handleChange}
                className="input mt-1"
                placeholder="Enter your DeepSeek API key"
              />
              <p className="mt-1 text-sm text-gray-500">
                Get your API key from the DeepSeek platform
              </p>
            </div>

            <div>
              <label htmlFor="phantomId" className="block text-sm font-medium text-gray-700">
                Phantom ID
              </label>
              <input
                type="text"
                name="phantomId"
                id="phantomId"
                value={formData.phantomId}
                onChange={handleChange}
                className="input mt-1"
                placeholder="Enter your LinkedIn outreach phantom ID"
              />
              <p className="mt-1 text-sm text-gray-500">
                The ID of your LinkedIn outreach phantom in PhantomBuster
              </p>
            </div>

            <div className="flex justify-end">
              <button
                type="submit"
                disabled={loading}
                className="btn-primary"
              >
                {loading ? 'Saving...' : 'Save Configuration'}
              </button>
            </div>
          </form>
        </div>
      </div>

      {/* System Information */}
      <div className="card">
        <div className="card-header">
          <h3 className="text-lg font-medium text-gray-900">System Information</h3>
        </div>
        <div className="card-body">
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <div>
              <label className="block text-sm font-medium text-gray-500">System Status</label>
              <p className="mt-1 text-sm text-gray-900">Active</p>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-500">Database</label>
              <p className="mt-1 text-sm text-gray-900">SQLite</p>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-500">Version</label>
              <p className="mt-1 text-sm text-gray-900">1.0.0</p>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-500">Last Updated</label>
              <p className="mt-1 text-sm text-gray-900">
                {new Date().toLocaleDateString()}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Help Section */}
      <div className="card">
        <div className="card-header">
          <h3 className="text-lg font-medium text-gray-900">Getting Started</h3>
        </div>
        <div className="card-body">
          <div className="space-y-4">
            <div>
              <h4 className="text-sm font-medium text-gray-900">1. Set up PhantomBuster</h4>
              <p className="mt-1 text-sm text-gray-500">
                Create a LinkedIn outreach phantom in PhantomBuster and get your API key and phantom ID.
              </p>
            </div>
            <div>
              <h4 className="text-sm font-medium text-gray-900">2. Get DeepSeek API Key</h4>
              <p className="mt-1 text-sm text-gray-500">
                Sign up for DeepSeek and generate an API key for AI-powered message generation.
              </p>
            </div>
            <div>
              <h4 className="text-sm font-medium text-gray-900">3. Create Your First Campaign</h4>
              <p className="mt-1 text-sm text-gray-500">
                Set up a Google Spreadsheet with your target contacts and create your first campaign.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Settings; 