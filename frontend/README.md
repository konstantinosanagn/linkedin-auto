# LinkedIn Automation System - Frontend

A modern React.js web application for managing LinkedIn automation campaigns with AI-powered personalization.

## Features

- **Dashboard**: Overview with key metrics and charts
- **Campaign Management**: Create, launch, and monitor campaigns
- **Contact Management**: View and filter contact lists
- **Analytics**: Detailed performance metrics and insights
- **Message Templates**: Create and manage message templates
- **Settings**: Configure API keys and system settings

## Tech Stack

- **React 18** - Modern React with hooks
- **Tailwind CSS** - Utility-first CSS framework
- **React Router** - Client-side routing
- **Axios** - HTTP client for API calls
- **Recharts** - Data visualization library
- **React Hot Toast** - Toast notifications
- **Heroicons** - Beautiful SVG icons

## Getting Started

### Prerequisites

- Node.js 16+ and npm
- Backend API running (see main README)

### Installation

1. **Navigate to the frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start the development server**:
   ```bash
   npm start
   ```

4. **Open your browser** and navigate to `http://localhost:3000`

### Building for Production

```bash
npm run build
```

This creates a `build` folder with optimized production files.

## Project Structure

```
frontend/
├── public/                 # Static files
├── src/
│   ├── components/         # Reusable components
│   │   ├── Layout/        # Layout components
│   │   └── Campaigns/     # Campaign-specific components
│   ├── contexts/          # React contexts
│   ├── pages/             # Page components
│   ├── services/          # API services
│   ├── App.js             # Main app component
│   ├── index.js           # Entry point
│   └── index.css          # Global styles
├── package.json           # Dependencies and scripts
├── tailwind.config.js     # Tailwind configuration
└── README.md             # This file
```

## Key Components

### Pages

- **Dashboard** (`pages/Dashboard.js`) - Overview with metrics and charts
- **Campaigns** (`pages/Campaigns.js`) - Campaign management interface
- **Contacts** (`pages/Contacts.js`) - Contact list and filtering
- **Analytics** (`pages/Analytics.js`) - Detailed analytics and reports
- **Templates** (`pages/Templates.js`) - Message template management
- **Settings** (`pages/Settings.js`) - Configuration and system settings

### Components

- **Layout** (`components/Layout/Layout.js`) - Main layout with sidebar navigation
- **CreateCampaignModal** (`components/Campaigns/CreateCampaignModal.js`) - Campaign creation form
- **CampaignDetailsModal** (`components/Campaigns/CampaignDetailsModal.js`) - Campaign details view

### Services

- **API Service** (`services/api.js`) - Centralized API communication
- **Auth Context** (`contexts/AuthContext.js`) - Authentication and configuration state

## API Integration

The frontend communicates with the backend through RESTful APIs:

- **Campaigns**: CRUD operations for campaigns
- **Contacts**: Contact management and filtering
- **Analytics**: Performance metrics and reports
- **Templates**: Message template management
- **System**: Configuration and health checks

## Styling

The application uses Tailwind CSS with custom components:

- **Cards**: `.card`, `.card-header`, `.card-body`
- **Buttons**: `.btn`, `.btn-primary`, `.btn-secondary`, etc.
- **Badges**: `.badge`, `.badge-success`, `.badge-warning`, etc.
- **Inputs**: `.input` for form controls

## State Management

- **React Context** for global state (auth, config)
- **Local state** with useState for component-specific data
- **API state** managed with async/await and error handling

## Responsive Design

The application is fully responsive with:
- Mobile-first design approach
- Responsive grid layouts
- Collapsible sidebar for mobile
- Touch-friendly interactions

## Development

### Available Scripts

- `npm start` - Start development server
- `npm run build` - Build for production
- `npm test` - Run tests
- `npm run eject` - Eject from Create React App

### Code Style

- ESLint configuration included
- Prettier formatting recommended
- Component-based architecture
- Functional components with hooks

## Deployment

### Build Process

1. Run `npm run build`
2. Deploy the `build` folder to your web server
3. Configure your server to serve `index.html` for all routes

### Environment Variables

Create a `.env` file in the frontend directory:

```env
REACT_APP_API_URL=http://localhost:5000
```

## Troubleshooting

### Common Issues

1. **API Connection Errors**
   - Ensure the backend is running
   - Check the API URL in `.env`
   - Verify CORS configuration

2. **Build Errors**
   - Clear `node_modules` and reinstall
   - Check for missing dependencies
   - Verify Node.js version

3. **Styling Issues**
   - Ensure Tailwind CSS is properly configured
   - Check for CSS conflicts
   - Verify PostCSS configuration

## Contributing

1. Follow the existing code style
2. Add proper error handling
3. Include loading states
4. Test on different screen sizes
5. Update documentation as needed

## License

This project is licensed under the MIT License. 