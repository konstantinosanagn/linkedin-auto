import React, { useState, useEffect } from 'react';
import { UsersIcon } from '@heroicons/react/24/outline';
import { contactAPI } from '../services/api';
import toast from 'react-hot-toast';

const Contacts = () => {
  const [contacts, setContacts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({
    status: '',
    variant: '',
    company: '',
  });

  useEffect(() => {
    loadContacts();
  }, [filters]);

  const loadContacts = async () => {
    try {
      setLoading(true);
      const response = await contactAPI.getAll(filters);
      setContacts(response.data || []);
    } catch (error) {
      console.error('Error loading contacts:', error);
      toast.error('Failed to load contacts');
    } finally {
      setLoading(false);
    }
  };

  const getStatusBadge = (status) => {
    const statusConfig = {
      'Invitation sent': { color: 'badge-info', text: 'Invitation Sent' },
      'Invitation accepted': { color: 'badge-success', text: 'Accepted' },
      'Replied (Connection request)': { color: 'badge-warning', text: 'Replied' },
      'Replied (Follow-up)': { color: 'badge-success', text: 'Follow-up Reply' },
      'Connection declined': { color: 'badge-danger', text: 'Declined' },
      'No response': { color: 'badge-secondary', text: 'No Response' },
    };

    const config = statusConfig[status] || { color: 'badge-secondary', text: status };
    return <span className={`badge ${config.color}`}>{config.text}</span>;
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Contacts</h1>
        <p className="mt-1 text-sm text-gray-500">
          Manage your LinkedIn contacts and track their status
        </p>
      </div>

      {/* Filters */}
      <div className="card">
        <div className="card-body">
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
            <div>
              <label className="block text-sm font-medium text-gray-700">Status</label>
              <select
                value={filters.status}
                onChange={(e) => setFilters(prev => ({ ...prev, status: e.target.value }))}
                className="input mt-1"
              >
                <option value="">All Statuses</option>
                <option value="Invitation sent">Invitation Sent</option>
                <option value="Invitation accepted">Accepted</option>
                <option value="Replied (Connection request)">Replied</option>
                <option value="Replied (Follow-up)">Follow-up Reply</option>
                <option value="Connection declined">Declined</option>
                <option value="No response">No Response</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Variant</label>
              <select
                value={filters.variant}
                onChange={(e) => setFilters(prev => ({ ...prev, variant: e.target.value }))}
                className="input mt-1"
              >
                <option value="">All Variants</option>
                <option value="networking">Networking</option>
                <option value="business_opportunity">Business Opportunity</option>
                <option value="industry_insights">Industry Insights</option>
                <option value="collaboration">Collaboration</option>
                <option value="mentorship">Mentorship</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Company</label>
              <input
                type="text"
                value={filters.company}
                onChange={(e) => setFilters(prev => ({ ...prev, company: e.target.value }))}
                className="input mt-1"
                placeholder="Filter by company"
              />
            </div>
          </div>
        </div>
      </div>

      {/* Contacts List */}
      <div className="card">
        <div className="card-header">
          <h3 className="text-lg font-medium text-gray-900">All Contacts ({contacts.length})</h3>
        </div>
        <div className="card-body">
          {contacts.length === 0 ? (
            <div className="text-center py-12">
              <UsersIcon className="mx-auto h-12 w-12 text-gray-400" />
              <h3 className="mt-2 text-sm font-medium text-gray-900">No contacts found</h3>
              <p className="mt-1 text-sm text-gray-500">
                {Object.values(filters).some(f => f) ? 'Try adjusting your filters.' : 'Start a campaign to add contacts.'}
              </p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Contact
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Company
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Status
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Variant
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Follow-ups
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Added
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {contacts.map((contact) => (
                    <tr key={contact.id} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div>
                          <div className="text-sm font-medium text-gray-900">
                            {contact.name}
                          </div>
                          <div className="text-sm text-gray-500">
                            {contact.job_title}
                          </div>
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {contact.company}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        {getStatusBadge(contact.status)}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {contact.variant}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {contact.followup_attempts || 0}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {new Date(contact.created_at).toLocaleDateString()}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Contacts; 