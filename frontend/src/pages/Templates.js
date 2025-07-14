import React, { useState, useEffect } from 'react';
import { PlusIcon, PencilIcon, TrashIcon, DocumentTextIcon } from '@heroicons/react/24/outline';
import { templateAPI } from '../services/api';
import toast from 'react-hot-toast';

const Templates = () => {
  const [templates, setTemplates] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [editingTemplate, setEditingTemplate] = useState(null);

  useEffect(() => {
    loadTemplates();
  }, []);

  const loadTemplates = async () => {
    try {
      setLoading(true);
      const response = await templateAPI.getAll();
      setTemplates(response.data || []);
    } catch (error) {
      console.error('Error loading templates:', error);
      toast.error('Failed to load templates');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTemplate = async (templateData) => {
    try {
      await templateAPI.create(templateData);
      toast.success('Template created successfully');
      setShowCreateModal(false);
      loadTemplates();
    } catch (error) {
      console.error('Error creating template:', error);
      toast.error('Failed to create template');
    }
  };

  const handleDeleteTemplate = async (templateId) => {
    if (window.confirm('Are you sure you want to delete this template?')) {
      try {
        await templateAPI.delete(templateId);
        toast.success('Template deleted successfully');
        loadTemplates();
      } catch (error) {
        console.error('Error deleting template:', error);
        toast.error('Failed to delete template');
      }
    }
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

  const getTypeBadge = (type) => {
    const typeConfig = {
      connection: { color: 'badge-info', text: 'Connection' },
      followup: { color: 'badge-warning', text: 'Follow-up' },
    };

    const config = typeConfig[type] || { color: 'badge-secondary', text: type };
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
          <h1 className="text-2xl font-bold text-gray-900">Message Templates</h1>
          <p className="mt-1 text-sm text-gray-500">
            Create and manage your message templates
          </p>
        </div>
        <button
          onClick={() => setShowCreateModal(true)}
          className="btn-primary"
        >
          <PlusIcon className="h-5 w-5 mr-2" />
          Create Template
        </button>
      </div>

      {/* Templates Grid */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        {templates.length === 0 ? (
          <div className="col-span-full text-center py-12">
            <DocumentTextIcon className="mx-auto h-12 w-12 text-gray-400" />
            <h3 className="mt-2 text-sm font-medium text-gray-900">No templates</h3>
            <p className="mt-1 text-sm text-gray-500">
              Get started by creating your first message template.
            </p>
            <div className="mt-6">
              <button
                onClick={() => setShowCreateModal(true)}
                className="btn-primary"
              >
                <PlusIcon className="h-5 w-5 mr-2" />
                Create Template
              </button>
            </div>
          </div>
        ) : (
          templates.map((template) => (
            <div key={template.id} className="card">
              <div className="card-header">
                <div className="flex justify-between items-start">
                  <div>
                    <h3 className="text-lg font-medium text-gray-900">{template.name}</h3>
                    <div className="mt-1 flex space-x-2">
                      {getVariantBadge(template.variant)}
                      {getTypeBadge(template.template_type)}
                    </div>
                  </div>
                  <div className="flex space-x-2">
                    <button
                      onClick={() => setEditingTemplate(template)}
                      className="text-primary-600 hover:text-primary-900"
                    >
                      <PencilIcon className="h-4 w-4" />
                    </button>
                    <button
                      onClick={() => handleDeleteTemplate(template.id)}
                      className="text-danger-600 hover:text-danger-900"
                    >
                      <TrashIcon className="h-4 w-4" />
                    </button>
                  </div>
                </div>
              </div>
              <div className="card-body">
                <div className="prose prose-sm max-w-none">
                  <p className="text-gray-700 whitespace-pre-wrap">{template.content}</p>
                </div>
                <div className="mt-4 text-xs text-gray-500">
                  Created: {new Date(template.created_at).toLocaleDateString()}
                </div>
              </div>
            </div>
          ))
        )}
      </div>

      {/* Create Template Modal */}
      {showCreateModal && (
        <CreateTemplateModal
          onClose={() => setShowCreateModal(false)}
          onSubmit={handleCreateTemplate}
        />
      )}

      {/* Edit Template Modal */}
      {editingTemplate && (
        <EditTemplateModal
          template={editingTemplate}
          onClose={() => setEditingTemplate(null)}
          onSubmit={handleCreateTemplate}
        />
      )}
    </div>
  );
};

// Simple Create Template Modal Component
const CreateTemplateModal = ({ onClose, onSubmit }) => {
  const [formData, setFormData] = useState({
    name: '',
    variant: 'networking',
    template_type: 'connection',
    content: '',
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto">
      <div className="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" onClick={onClose}></div>
        <div className="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
          <div className="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Create Template</h3>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">Name</label>
                <input
                  type="text"
                  required
                  value={formData.name}
                  onChange={(e) => setFormData(prev => ({ ...prev, name: e.target.value }))}
                  className="input mt-1"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Variant</label>
                <select
                  value={formData.variant}
                  onChange={(e) => setFormData(prev => ({ ...prev, variant: e.target.value }))}
                  className="input mt-1"
                >
                  <option value="networking">Networking</option>
                  <option value="business_opportunity">Business Opportunity</option>
                  <option value="industry_insights">Industry Insights</option>
                  <option value="collaboration">Collaboration</option>
                  <option value="mentorship">Mentorship</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Type</label>
                <select
                  value={formData.template_type}
                  onChange={(e) => setFormData(prev => ({ ...prev, template_type: e.target.value }))}
                  className="input mt-1"
                >
                  <option value="connection">Connection</option>
                  <option value="followup">Follow-up</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Content</label>
                <textarea
                  required
                  rows={6}
                  value={formData.content}
                  onChange={(e) => setFormData(prev => ({ ...prev, content: e.target.value }))}
                  className="input mt-1"
                  placeholder="Enter your message template..."
                />
              </div>
            </form>
          </div>
          <div className="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
            <button onClick={handleSubmit} className="btn-primary w-full sm:w-auto sm:ml-3">
              Create Template
            </button>
            <button onClick={onClose} className="btn-secondary w-full sm:w-auto mt-3 sm:mt-0">
              Cancel
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

const EditTemplateModal = ({ template, onClose, onSubmit }) => {
  const [formData, setFormData] = useState({
    name: template.name,
    variant: template.variant,
    template_type: template.template_type,
    content: template.content,
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit({ ...formData, id: template.id });
  };

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto">
      <div className="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" onClick={onClose}></div>
        <div className="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
          <div className="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Edit Template</h3>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">Name</label>
                <input
                  type="text"
                  required
                  value={formData.name}
                  onChange={(e) => setFormData(prev => ({ ...prev, name: e.target.value }))}
                  className="input mt-1"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Variant</label>
                <select
                  value={formData.variant}
                  onChange={(e) => setFormData(prev => ({ ...prev, variant: e.target.value }))}
                  className="input mt-1"
                >
                  <option value="networking">Networking</option>
                  <option value="business_opportunity">Business Opportunity</option>
                  <option value="industry_insights">Industry Insights</option>
                  <option value="collaboration">Collaboration</option>
                  <option value="mentorship">Mentorship</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Type</label>
                <select
                  value={formData.template_type}
                  onChange={(e) => setFormData(prev => ({ ...prev, template_type: e.target.value }))}
                  className="input mt-1"
                >
                  <option value="connection">Connection</option>
                  <option value="followup">Follow-up</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Content</label>
                <textarea
                  required
                  rows={6}
                  value={formData.content}
                  onChange={(e) => setFormData(prev => ({ ...prev, content: e.target.value }))}
                  className="input mt-1"
                />
              </div>
            </form>
          </div>
          <div className="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
            <button onClick={handleSubmit} className="btn-primary w-full sm:w-auto sm:ml-3">
              Update Template
            </button>
            <button onClick={onClose} className="btn-secondary w-full sm:w-auto mt-3 sm:mt-0">
              Cancel
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Templates; 