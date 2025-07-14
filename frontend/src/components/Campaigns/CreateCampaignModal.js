import React, { useState } from 'react';
import { XMarkIcon } from '@heroicons/react/24/outline';

const CreateCampaignModal = ({ onClose, onSubmit }) => {
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    variant: 'networking',
    spreadsheet_url: '',
    connection_template: '',
  });

  const variants = [
    { value: 'networking', label: 'Networking' },
    { value: 'business_opportunity', label: 'Business Opportunity' },
    { value: 'industry_insights', label: 'Industry Insights' },
    { value: 'collaboration', label: 'Collaboration' },
    { value: 'mentorship', label: 'Mentorship' },
  ];

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto">
      <div className="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" onClick={onClose}></div>

        <div className="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
          <div className="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-medium text-gray-900">Create New Campaign</h3>
              <button
                onClick={onClose}
                className="text-gray-400 hover:text-gray-600"
              >
                <XMarkIcon className="h-6 w-6" />
              </button>
            </div>

            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label htmlFor="name" className="block text-sm font-medium text-gray-700">
                  Campaign Name
                </label>
                <input
                  type="text"
                  name="name"
                  id="name"
                  required
                  value={formData.name}
                  onChange={handleChange}
                  className="input mt-1"
                  placeholder="Enter campaign name"
                />
              </div>

              <div>
                <label htmlFor="description" className="block text-sm font-medium text-gray-700">
                  Description
                </label>
                <textarea
                  name="description"
                  id="description"
                  rows={3}
                  value={formData.description}
                  onChange={handleChange}
                  className="input mt-1"
                  placeholder="Enter campaign description"
                />
              </div>

              <div>
                <label htmlFor="variant" className="block text-sm font-medium text-gray-700">
                  Message Variant
                </label>
                <select
                  name="variant"
                  id="variant"
                  value={formData.variant}
                  onChange={handleChange}
                  className="input mt-1"
                >
                  {variants.map(variant => (
                    <option key={variant.value} value={variant.value}>
                      {variant.label}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label htmlFor="spreadsheet_url" className="block text-sm font-medium text-gray-700">
                  Spreadsheet URL
                </label>
                <input
                  type="url"
                  name="spreadsheet_url"
                  id="spreadsheet_url"
                  required
                  value={formData.spreadsheet_url}
                  onChange={handleChange}
                  className="input mt-1"
                  placeholder="https://docs.google.com/spreadsheets/d/..."
                />
              </div>

              <div>
                <label htmlFor="connection_template" className="block text-sm font-medium text-gray-700">
                  Connection Message Template
                </label>
                <textarea
                  name="connection_template"
                  id="connection_template"
                  rows={4}
                  value={formData.connection_template}
                  onChange={handleChange}
                  className="input mt-1"
                  placeholder="Hi {first_name}, I noticed your work at {company}..."
                />
                <p className="mt-1 text-sm text-gray-500">
                  Use placeholders: {'{first_name}'}, {'{company}'}, {'{job_title}'}
                </p>
              </div>
            </form>
          </div>

          <div className="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
            <button
              type="submit"
              onClick={handleSubmit}
              className="btn-primary w-full sm:w-auto sm:ml-3"
            >
              Create Campaign
            </button>
            <button
              type="button"
              onClick={onClose}
              className="btn-secondary w-full sm:w-auto mt-3 sm:mt-0"
            >
              Cancel
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CreateCampaignModal; 