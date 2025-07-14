# LinkedIn Automation System

A comprehensive system for automating LinkedIn outreach campaigns using PhantomBuster API and DeepSeek LLM for personalized messaging.

## Features

- 🤖 **Automated Connection Requests** with personalized messages
- 📊 **Campaign Management** and analytics tracking
- 🧠 **AI-Powered Follow-ups** using DeepSeek LLM
- 📈 **Message Variant Testing** and performance tracking
- 🗄️ **Database Management** for contact tracking
- 🌐 **Modern Web UI** with React and Tailwind CSS
- 🔧 **RESTful API** with Flask backend

## Tech Stack

### Backend
- **Python 3.8+**
- **Flask** - Web API framework
- **SQLite** - Database
- **PhantomBuster API** - LinkedIn automation
- **DeepSeek LLM** - AI message generation

### Frontend
- **React.js** - UI framework
- **Tailwind CSS** - Styling
- **Axios** - HTTP client

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- PhantomBuster API key
- DeepSeek API key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/kostasateulerion/linkedin-auto.git
   cd linkedin-auto
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install frontend dependencies**
   ```bash
   cd frontend
   npm install
   cd ..
   ```

4. **Configure API keys**
   - Copy `config.py.example` to `config.py`
   - Add your PhantomBuster and DeepSeek API keys

### Running the Application

1. **Start the backend API**
   ```bash
   python api.py
   ```
   The API will run on `http://localhost:5000`

2. **Start the frontend**
   ```bash
   cd frontend
   npm start
   ```
   The UI will open on `http://localhost:3000`

## Usage

### 1. Configure Settings
- Go to the Settings tab in the web UI
- Add your PhantomBuster API key, DeepSeek API key, and Phantom ID

### 2. Create Campaigns
- Use the Campaigns tab to create new outreach campaigns
- Upload a Google Sheets with headers: `linkedin_url,first_name,last_name,company,job_title`

### 3. Monitor Progress
- Track campaign progress in the Dashboard
- View contact details and responses in the Contacts tab
- Analyze performance metrics in the Analytics section

### 4. Manage Templates
- Create and customize message templates
- Test different message variants for optimal performance

## API Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `GET /config` - Get configuration
- `POST /config` - Update configuration
- `GET /campaigns` - List campaigns
- `POST /campaigns` - Create campaign
- `GET /contacts` - List contacts
- `GET /analytics/dashboard` - Get analytics
- `POST /sync` - Sync campaign results
- `POST /followup` - Process follow-ups

## Google Sheets Format

Your spreadsheet should have these columns:
```
linkedin_url,first_name,last_name,company,job_title
```

Example:
```
https://linkedin.com/in/johndoe,John,Doe,Acme Corp,Software Engineer
https://linkedin.com/in/janesmith,Jane,Smith,Tech Inc,Product Manager
```

## Development

### Project Structure
```
linkedin_auto/
├── api.py              # Flask API server
├── main.py             # Main automation logic
├── config.py           # Configuration management
├── db.py               # Database operations
├── phantom.py          # PhantomBuster API integration
├── llm.py              # DeepSeek LLM integration
├── messaging.py        # Message template management
├── models.py           # Data models
├── frontend/           # React frontend
│   ├── src/
│   ├── package.json
│   └── ...
├── requirements.txt    # Python dependencies
└── README.md
```

### Adding New Features
1. Backend changes go in the Python files
2. Frontend changes go in the `frontend/` directory
3. Update API endpoints in `api.py` as needed
4. Test thoroughly before pushing

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
- Create an issue on GitHub
- Check the documentation
- Review the logs in `linkedin_automation.log`

## Security Notes

- Never commit API keys or sensitive data
- Use environment variables for production
- Keep your `config.py` file secure
- Regularly update dependencies
