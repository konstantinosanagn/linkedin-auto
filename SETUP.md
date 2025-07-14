# LinkedIn Automation System - Setup Guide

This guide will help you set up the LinkedIn automation system step by step.

## Quick Start (Without API Keys - Testing Mode)

If you want to test the system without setting up API keys first:

1. **Run the test script**:
   ```bash
   python test_setup.py
   ```

2. **Initialize the system**:
   ```bash
   python main.py --init
   ```

3. **Test basic functionality**:
   ```bash
   python example.py
   ```

## Full Setup (With API Keys)

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Set Up API Keys

1. **Create a `.env` file** in the project root:
   ```bash
   copy config_template.txt .env
   ```

2. **Edit the `.env` file** and add your API keys:
   ```env
   PHANTOMBUSTER_API_KEY=your_actual_phantombuster_api_key
   DEEPSEEK_API_KEY=your_actual_deepseek_api_key
   PHANTOM_ID=your_actual_phantom_id
   ```

### Step 3: Get API Keys

#### PhantomBuster API Key
1. Sign up at [PhantomBuster](https://phantombuster.com)
2. Create a LinkedIn outreach phantom
3. Go to your dashboard
4. Copy your API key
5. Note your phantom ID

#### DeepSeek API Key
1. Sign up at [DeepSeek](https://platform.deepseek.com)
2. Go to API settings
3. Generate a new API key
4. Copy the key

### Step 4: Initialize the System

```bash
python main.py --init
```

### Step 5: Test the Setup

```bash
python test_setup.py
```

## Usage Examples

### Create a Campaign
```bash
python main.py --create-campaign "Tech Outreach" "Outreach to tech professionals" "networking" "https://docs.google.com/spreadsheets/d/your_spreadsheet_id" "Hi {first_name}, I noticed your work at {company}..."
```

### Run a Campaign
```bash
python main.py --campaign 1
```

### Sync Results
```bash
python main.py --sync
```

### Process Follow-ups
```bash
python main.py --followup
```

### View Analytics
```bash
python main.py --analytics
```

## Troubleshooting

### Common Issues

1. **"Missing required configuration" error**
   - Solution: Set up your API keys in the `.env` file
   - Or use testing mode: `python test_setup.py`

2. **"no such table" errors**
   - Solution: Run `python main.py --init` to initialize the database

3. **"401 Unauthorized" errors**
   - Solution: Check your API keys are correct
   - Verify your PhantomBuster phantom ID

4. **Import errors**
   - Solution: Make sure you're in the correct directory
   - Run `pip install -r requirements.txt`

### Testing Without API Keys

If you don't have API keys yet, you can still test the system:

1. **Test database functionality**:
   ```bash
   python test_setup.py
   ```

2. **Run examples**:
   ```bash
   python example.py
   ```

3. **Initialize system**:
   ```bash
   python main.py --init
   ```

The system will work for database operations and message template management, but API-dependent features (PhantomBuster integration, LLM message generation) will show warnings.

## Next Steps

Once the system is set up:

1. **Create your first campaign** using the CLI or programmatically
2. **Set up your LinkedIn outreach phantom** in PhantomBuster
3. **Prepare your target list** in a Google Spreadsheet
4. **Run campaigns** and monitor results
5. **Analyze performance** using the analytics features
6. **Optimize your approach** based on variant performance

## Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review the logs in `linkedin_automation.log`
3. Run the test script to identify specific problems
4. Check the README.md for detailed documentation 