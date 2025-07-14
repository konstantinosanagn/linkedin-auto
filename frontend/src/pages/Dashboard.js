import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  UsersIcon,
  MegaphoneIcon,
  ChartBarIcon,
  CheckCircleIcon,
  ClockIcon,
  ExclamationTriangleIcon,
  DocumentTextIcon,
} from '@heroicons/react/24/outline';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { analyticsAPI, systemAPI } from '../services/api';
import toast from 'react-hot-toast';

const COLORS = ['#3b82f6', '#22c55e', '#f59e0b', '#ef4444', '#8b5cf6'];

const Dashboard = () => {
  const [stats, setStats] = useState({
    totalContacts: 0,
    totalCampaigns: 0,
    activeCampaigns: 0,
    pendingFollowups: 0,
    connectionRate: 0,
    responseRate: 0,
  });
  const [statusData, setStatusData] = useState([]);
  const [variantData, setVariantData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      const [analyticsResponse, healthResponse] = await Promise.all([
        analyticsAPI.getDashboard(),
        systemAPI.health(),
      ]);

      if (analyticsResponse.data) {
        const data = analyticsResponse.data;
        setStats({
          totalContacts: data.total_contacts || 0,
          totalCampaigns: data.total_campaigns || 0,
          activeCampaigns: data.active_campaigns || 0,
          pendingFollowups: data.pending_followups || 0,
          connectionRate: data.connection_rate || 0,
          responseRate: data.response_rate || 0,
        });

        // Format status data for pie chart
        if (data.status_breakdown) {
          const statusChartData = Object.entries(data.status_breakdown).map(([status, count]) => ({
            name: status,
            value: count,
          }));
          setStatusData(statusChartData);
        }

        // Format variant data for bar chart
        if (data.variant_performance) {
          const variantChartData = data.variant_performance.map(variant => ({
            name: variant.variant,
            total: variant.total,
            replied: variant.replied_connection,
            followup: variant.replied_followup,
          }));
          setVariantData(variantChartData);
        }
      }
    } catch (error) {
      console.error('Error loading dashboard data:', error);
      toast.error('Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  };

  const StatCard = ({ title, value, icon: Icon, color, subtitle }) => (
    <div className="card">
      <div className="card-body">
        <div className="flex items-center">
          <div className={`flex-shrink-0 p-3 rounded-md ${color}`}>
            <Icon className="h-6 w-6 text-white" />
          </div>
          <div className="ml-5 w-0 flex-1">
            <dl>
              <dt className="text-sm font-medium text-gray-500 truncate">{title}</dt>
              <dd className="text-lg font-medium text-gray-900">{value}</dd>
              {subtitle && <dd className="text-sm text-gray-500">{subtitle}</dd>}
            </dl>
          </div>
        </div>
      </div>
    </div>
  );

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
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <p className="mt-1 text-sm text-gray-500">
          Overview of your LinkedIn automation campaigns and performance
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
        <StatCard
          title="Total Contacts"
          value={stats.totalContacts}
          icon={UsersIcon}
          color="bg-primary-500"
        />
        <StatCard
          title="Active Campaigns"
          value={stats.activeCampaigns}
          icon={MegaphoneIcon}
          color="bg-success-500"
        />
        <StatCard
          title="Pending Follow-ups"
          value={stats.pendingFollowups}
          icon={ClockIcon}
          color="bg-warning-500"
        />
        <StatCard
          title="Connection Rate"
          value={`${stats.connectionRate}%`}
          icon={CheckCircleIcon}
          color="bg-success-500"
          subtitle="Invitations accepted"
        />
        <StatCard
          title="Response Rate"
          value={`${stats.responseRate}%`}
          icon={ChartBarIcon}
          color="bg-primary-500"
          subtitle="Messages replied to"
        />
        <StatCard
          title="Total Campaigns"
          value={stats.totalCampaigns}
          icon={MegaphoneIcon}
          color="bg-info-500"
        />
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        {/* Status Distribution */}
        <div className="card">
          <div className="card-header">
            <h3 className="text-lg font-medium text-gray-900">Contact Status Distribution</h3>
          </div>
          <div className="card-body">
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={statusData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {statusData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>

        {/* Variant Performance */}
        <div className="card">
          <div className="card-header">
            <h3 className="text-lg font-medium text-gray-900">Variant Performance</h3>
          </div>
          <div className="card-body">
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={variantData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="total" fill="#3b82f6" name="Total" />
                  <Bar dataKey="replied" fill="#22c55e" name="Replied" />
                  <Bar dataKey="followup" fill="#f59e0b" name="Follow-up" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="card">
        <div className="card-header">
          <h3 className="text-lg font-medium text-gray-900">Quick Actions</h3>
        </div>
        <div className="card-body">
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
            <Link
              to="/campaigns"
              className="group relative rounded-lg border border-gray-300 bg-white p-6 hover:border-primary-500 hover:shadow-md transition-all"
            >
              <div>
                <span className="inline-flex rounded-lg bg-primary-50 p-3 text-primary-600 group-hover:bg-primary-100">
                  <MegaphoneIcon className="h-6 w-6" />
                </span>
              </div>
              <div className="mt-4">
                <h3 className="text-lg font-medium text-gray-900">Create Campaign</h3>
                <p className="mt-2 text-sm text-gray-500">
                  Start a new LinkedIn outreach campaign
                </p>
              </div>
            </Link>

            <Link
              to="/contacts"
              className="group relative rounded-lg border border-gray-300 bg-white p-6 hover:border-primary-500 hover:shadow-md transition-all"
            >
              <div>
                <span className="inline-flex rounded-lg bg-success-50 p-3 text-success-600 group-hover:bg-success-100">
                  <UsersIcon className="h-6 w-6" />
                </span>
              </div>
              <div className="mt-4">
                <h3 className="text-lg font-medium text-gray-900">Manage Contacts</h3>
                <p className="mt-2 text-sm text-gray-500">
                  View and manage your contact list
                </p>
              </div>
            </Link>

            <Link
              to="/templates"
              className="group relative rounded-lg border border-gray-300 bg-white p-6 hover:border-primary-500 hover:shadow-md transition-all"
            >
              <div>
                <span className="inline-flex rounded-lg bg-warning-50 p-3 text-warning-600 group-hover:bg-warning-100">
                  <DocumentTextIcon className="h-6 w-6" />
                </span>
              </div>
              <div className="mt-4">
                <h3 className="text-lg font-medium text-gray-900">Message Templates</h3>
                <p className="mt-2 text-sm text-gray-500">
                  Create and manage message templates
                </p>
              </div>
            </Link>

            <Link
              to="/analytics"
              className="group relative rounded-lg border border-gray-300 bg-white p-6 hover:border-primary-500 hover:shadow-md transition-all"
            >
              <div>
                <span className="inline-flex rounded-lg bg-info-50 p-3 text-info-600 group-hover:bg-info-100">
                  <ChartBarIcon className="h-6 w-6" />
                </span>
              </div>
              <div className="mt-4">
                <h3 className="text-lg font-medium text-gray-900">View Analytics</h3>
                <p className="mt-2 text-sm text-gray-500">
                  Detailed performance analytics
                </p>
              </div>
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard; 