import React from 'react';
import { XMarkIcon } from '@heroicons/react/24/outline';

const CampaignDetailsModal = ({ campaign, onClose }) => {
  const getStatusBadge = (status) => {
    const statusConfig = {
      active: { color: 'badge-success', text: 'Active' },
      paused: { color: 'badge-warning', text: 'Paused' },
      completed: { color: 'badge-info', text: 'Completed' },
      draft: { color: 'badge-secondary', text: 'Draft' },
    };

    const config = statusConfig[status] || { color: 'badge-secondary', text: status };
    return <span className={`badge ${config.color}`}>{config.text}</span>;
  };

  const getVariantBadge = (variant) => {
    const variantConfig = {
      networking: { color: 'badge-info', text: 'Networking' },
      business_opportunity: { color: 'badge-success', text: 'Business Opportunity' },
      industry_insights: { color: 'badge-warning', text: 'Industry Insights' },
      collaboration: { color: 'badge-primary', text: 'Collaboration' },
      mentorship: { color: 'badge-secondary', text: 'Mentorship' },
    };

    const config = variantConfig[variant] || { color: 'badge-secondary', text: variant };
    return <span className={`badge ${config.color}`}>{config.text}</span>;
  };

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto">
      <div className="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" onClick={onClose}></div>

        <div className="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-2xl sm:w-full">
          <div className="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-medium text-gray-900">Campaign Details</h3>
              <button
                onClick={onClose}
                className="text-gray-400 hover:text-gray-600"
              >
                <XMarkIcon className="h-6 w-6" />
              </button>
            </div>

            <div className="space-y-6">
              {/* Basic Information */}
              <div>
                <h4 className="text-sm font-medium text-gray-900 mb-3">Basic Information</h4>
                <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
                  <div>
                    <label className="block text-sm font-medium text-gray-500">Name</label>
                    <p className="mt-1 text-sm text-gray-900">{campaign.name}</p>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-500">Status</label>
                    <div className="mt-1">{getStatusBadge(campaign.status)}</div>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-500">Variant</label>
                    <div className="mt-1">{getVariantBadge(campaign.variant)}</div>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-500">Created</label>
                    <p className="mt-1 text-sm text-gray-900">
                      {new Date(campaign.created_at).toLocaleDateString()}
                    </p>
                  </div>
                </div>
                <div className="mt-4">
                  <label className="block text-sm font-medium text-gray-500">Description</label>
                  <p className="mt-1 text-sm text-gray-900">{campaign.description || 'No description provided'}</p>
                </div>
              </div>

              {/* Campaign Configuration */}
              <div>
                <h4 className="text-sm font-medium text-gray-900 mb-3">Campaign Configuration</h4>
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-500">Spreadsheet URL</label>
                    <p className="mt-1 text-sm text-gray-900 break-all">
                      <a 
                        href={campaign.spreadsheet_url} 
                        target="_blank" 
                        rel="noopener noreferrer"
                        className="text-primary-600 hover:text-primary-500"
                      >
                        {campaign.spreadsheet_url}
                      </a>
                    </p>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-500">Connection Template</label>
                    <div className="mt-1 p-3 bg-gray-50 rounded-md">
                      <p className="text-sm text-gray-900 whitespace-pre-wrap">
                        {campaign.connection_template || 'No template provided'}
                      </p>
                    </div>
                  </div>
                </div>
              </div>

              {/* Statistics */}
              <div>
                <h4 className="text-sm font-medium text-gray-900 mb-3">Campaign Statistics</h4>
                <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
                  <div className="text-center">
                    <p className="text-2xl font-bold text-primary-600">{campaign.contact_count || 0}</p>
                    <p className="text-xs text-gray-500">Total Contacts</p>
                  </div>
                  <div className="text-center">
                    <p className="text-2xl font-bold text-success-600">{campaign.connection_rate || 0}%</p>
                    <p className="text-xs text-gray-500">Connection Rate</p>
                  </div>
                  <div className="text-center">
                    <p className="text-2xl font-bold text-warning-600">{campaign.response_rate || 0}%</p>
                    <p className="text-xs text-gray-500">Response Rate</p>
                  </div>
                  <div className="text-center">
                    <p className="text-2xl font-bold text-info-600">{campaign.pending_followups || 0}</p>
                    <p className="text-xs text-gray-500">Pending Follow-ups</p>
                  </div>
                </div>
              </div>

              {/* Recent Activity */}
              {campaign.recent_activity && campaign.recent_activity.length > 0 && (
                <div>
                  <h4 className="text-sm font-medium text-gray-900 mb-3">Recent Activity</h4>
                  <div className="space-y-2">
                    {campaign.recent_activity.map((activity, index) => (
                      <div key={index} className="flex items-center space-x-3 text-sm">
                        <div className="flex-shrink-0">
                          <div className="h-2 w-2 bg-primary-500 rounded-full"></div>
                        </div>
                        <div className="flex-1">
                          <p className="text-gray-900">{activity.message}</p>
                          <p className="text-gray-500">{new Date(activity.timestamp).toLocaleString()}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>

          <div className="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
            <button
              type="button"
              onClick={onClose}
              className="btn-secondary w-full sm:w-auto"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CampaignDetailsModal; 