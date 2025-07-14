import React, { useState, useEffect } from 'react';
import {
  PlusIcon,
  PlayIcon,
  PauseIcon,
  ArrowPathIcon,
  PencilIcon,
  TrashIcon,
  EyeIcon,
  MegaphoneIcon,
} from '@heroicons/react/24/outline';
import { campaignAPI } from '../services/api';
import toast from 'react-hot-toast';
import CreateCampaignModal from '../components/Campaigns/CreateCampaignModal';
import CampaignDetailsModal from '../components/Campaigns/CampaignDetailsModal';

const Campaigns = () => {
  const [campaigns, setCampaigns] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showDetailsModal, setShowDetailsModal] = useState(false);
  const [selectedCampaign, setSelectedCampaign] = useState(null);

  useEffect(() => {
    loadCampaigns();
  }, []);

  const loadCampaigns = async () => {
    try {
      setLoading(true);
      const response = await campaignAPI.getAll();
      setCampaigns(response.data || []);
    } catch (error) {
      console.error('Error loading campaigns:', error);
      toast.error('Failed to load campaigns');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateCampaign = async (campaignData) => {
    try {
      await campaignAPI.create(campaignData);
      toast.success('Campaign created successfully');
      setShowCreateModal(false);
      loadCampaigns();
    } catch (error) {
      console.error('Error creating campaign:', error);
      toast.error('Failed to create campaign');
    }
  };

  const handleLaunchCampaign = async (campaignId) => {
    try {
      await campaignAPI.launch(campaignId);
      toast.success('Campaign launched successfully');
      loadCampaigns();
    } catch (error) {
      console.error('Error launching campaign:', error);
      toast.error('Failed to launch campaign');
    }
  };

  const handleSyncCampaign = async (campaignId) => {
    try {
      await campaignAPI.sync(campaignId);
      toast.success('Campaign synced successfully');
      loadCampaigns();
    } catch (error) {
      console.error('Error syncing campaign:', error);
      toast.error('Failed to sync campaign');
    }
  };

  const handleDeleteCampaign = async (campaignId) => {
    if (window.confirm('Are you sure you want to delete this campaign?')) {
      try {
        await campaignAPI.delete(campaignId);
        toast.success('Campaign deleted successfully');
        loadCampaigns();
      } catch (error) {
        console.error('Error deleting campaign:', error);
        toast.error('Failed to delete campaign');
      }
    }
  };

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
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Campaigns</h1>
          <p className="mt-1 text-sm text-gray-500">
            Manage your LinkedIn outreach campaigns
          </p>
        </div>
        <button
          onClick={() => setShowCreateModal(true)}
          className="btn-primary"
        >
          <PlusIcon className="h-5 w-5 mr-2" />
          Create Campaign
        </button>
      </div>

      {/* Campaigns List */}
      <div className="card">
        <div className="card-header">
          <h3 className="text-lg font-medium text-gray-900">All Campaigns</h3>
        </div>
        <div className="card-body">
          {campaigns.length === 0 ? (
            <div className="text-center py-12">
              <MegaphoneIcon className="mx-auto h-12 w-12 text-gray-400" />
              <h3 className="mt-2 text-sm font-medium text-gray-900">No campaigns</h3>
              <p className="mt-1 text-sm text-gray-500">
                Get started by creating your first campaign.
              </p>
              <div className="mt-6">
                <button
                  onClick={() => setShowCreateModal(true)}
                  className="btn-primary"
                >
                  <PlusIcon className="h-5 w-5 mr-2" />
                  Create Campaign
                </button>
              </div>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Campaign
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Variant
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Status
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Contacts
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Created
                    </th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Actions
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {campaigns.map((campaign) => (
                    <tr key={campaign.id} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div>
                          <div className="text-sm font-medium text-gray-900">
                            {campaign.name}
                          </div>
                          <div className="text-sm text-gray-500">
                            {campaign.description}
                          </div>
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        {getVariantBadge(campaign.variant)}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        {getStatusBadge(campaign.status)}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {campaign.contact_count || 0}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {new Date(campaign.created_at).toLocaleDateString()}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                        <div className="flex justify-end space-x-2">
                          <button
                            onClick={() => {
                              setSelectedCampaign(campaign);
                              setShowDetailsModal(true);
                            }}
                            className="text-primary-600 hover:text-primary-900"
                          >
                            <EyeIcon className="h-4 w-4" />
                          </button>
                          {campaign.status === 'active' ? (
                            <button
                              onClick={() => handleLaunchCampaign(campaign.id)}
                              className="text-success-600 hover:text-success-900"
                            >
                              <PlayIcon className="h-4 w-4" />
                            </button>
                          ) : (
                            <button
                              onClick={() => handleLaunchCampaign(campaign.id)}
                              className="text-warning-600 hover:text-warning-900"
                            >
                              <PauseIcon className="h-4 w-4" />
                            </button>
                          )}
                          <button
                            onClick={() => handleSyncCampaign(campaign.id)}
                            className="text-info-600 hover:text-info-900"
                          >
                            <ArrowPathIcon className="h-4 w-4" />
                          </button>
                          <button
                            onClick={() => handleDeleteCampaign(campaign.id)}
                            className="text-danger-600 hover:text-danger-900"
                          >
                            <TrashIcon className="h-4 w-4" />
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>

      {/* Modals */}
      {showCreateModal && (
        <CreateCampaignModal
          onClose={() => setShowCreateModal(false)}
          onSubmit={handleCreateCampaign}
        />
      )}

      {showDetailsModal && selectedCampaign && (
        <CampaignDetailsModal
          campaign={selectedCampaign}
          onClose={() => {
            setShowDetailsModal(false);
            setSelectedCampaign(null);
          }}
        />
      )}
    </div>
  );
};

export default Campaigns; 