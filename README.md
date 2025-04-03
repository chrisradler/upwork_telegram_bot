# Upwork AI Job Scraper with Proposal Generator

An automated tool that scrapes Upwork for AI-related job postings, generates customized proposals using Claude AI, creates implementation flowcharts, and sends everything to your Telegram channel.

## Overview

This bot periodically scrapes Upwork for the latest AI job opportunities that match specific criteria (hourly rate, client hiring history, location, etc.). For each job found, it uses Claude AI to generate a tailored proposal and a custom implementation flowchart, then sends the job details, proposal, and flowchart link directly to a Telegram chat. It runs on GitHub Actions, so there's no need for a dedicated server.

## Features

- 🔍 Scrapes multiple Upwork search queries focused on AI jobs
- 💰 Filters for jobs with higher budgets ($1000+) and rates ($35+/hour)
- 👥 Targets clients with proven hiring history
- 🌎 Focuses on jobs from Americas and Europe
- 🤖 Automatically generates customized proposals with Claude AI
- 📊 Creates custom implementation flowcharts for each job using Mermaid.js
- 🔄 Runs automatically every 30 minutes during business hours (Mon-Fri, 9am-7pm EST)
- 📱 Sends formatted job notifications and proposals to Telegram
- ⏰ ONLY Returns job that have been posted in the lAST hour
- ✍️ Supports manual job processing for custom opportunities

## Requirements

- Python 3.13
- Apify account with API token
- Telegram bot token and chat ID
- Claude API key (Claude 3.5 Sonnet model)
- GitHub account (for running GitHub Actions)
- Apify account
- Apify actor https://console.apify.com/actors/Cvx9keeu3XbxwYF6J/input

## Installation

1. Fork this repository

2. Open up an apify account and subscribe to the actor arlusm/upwork-scraper-with-fresh-job-posts:
    - https://console.apify.com/actors/Cvx9keeu3XbxwYF6J/input to sign in
    - Click the green start button when you are on the correct actor, you will activate a FREE TRIAL
    - Create a new api key. Settings -> API & Integrations -> Create New Token
    - Add api key to the .env file and as defualt values (not necessary) in scraper.py

3. Setup telegram bot:
    - Open Telegram and search for "@BotFather"
    - Start a chat with BotFather and send the command /newbot
    - Follow  the prompts to name your bot and create a username (must end with "bot")
    - BotFather will give you an API token (keep this secure!) 
    - Make sure to message the chat to initialize it

4. Obtain Telegram chat_id:
    - Create a new group in telegram and add your new bot to it. 
    - Visit this URL in a browser (replace with your actual bot token): https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates
    - Look for the "chat" object in the JSON response to find the "id" field. It will look like -723738272

5. Set up the required secrets in your GitHub repository (YOUR_APIFY_TOKEN, YOUR_TELEGRAM_BOT_TOKEN, YOUR_TELEGRAM_CHAT_ID):
    - Access repository
    - Navigate to secrets and Variables -> Actions -> New Repository Secrets -> Enter your keys
    - Make sure your repository is private so you do not leak any secrets!

6. Enable Github Actions:
    - Access repository
    - Settings -> Actions -> General -> Allow all actions and reusable workflows

7. Create a .env file, look for templete below

8. Adjust the system prompt to your use case. Line 30 in scraper.py

9. Everything should work and the bot should run every 30 minutes. You can run python3 scraper.py and manually run the bot to test. make sure you have activated the virtual environment. source venv/bin/activate

### .env Template

APIFY_TOKEN=YOUR_APIFY_TOKEN
TELEGRAM_BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
TELEGRAM_CHAT_ID=YOUR_TELEGRAM_CHAT_ID
CLAUDE_API_KEY=YOUR_CLAUDE_API_KEY
PROXY_URL=http://user:pass@proxy.example.com:8080
MAX_RETRIES=3
RETRY_DELAY=5
BATCH_SIZE=1

### GitHub Workflow

The scraper runs on a schedule defined in `.github/workflows/upwork_scraper.yml`:

```yaml
schedule:
- cron: '*/30 13-23 * * 1-5'  # Run every 30 minutes mon-fri from 9am - 7pm EST
```

You can adjust this schedule to your preferred frequency and timezone.

### Search Queries

The search criteria are defined in `scraper.py`. Current criteria include:

- AI-related jobs (Web Development, Software Development)
- Budget range: $1000-$4999, $5000+
- Hourly rate: $35+
- Client history: 1-9 hires, 10+ hires
- Location: Americas, Europe
- Contractor tier: Intermediate, Expert
- Proposal count: 0-4, 5-9, 10-14
- Sorted by: Most recent

You can modify these search parameters in the `run_input` section of `scraper.py`.

### Proposal and Flowchart Customization

### Proposal Generation

The AI-generated proposals are tailored to present your business (tmplogic) as a custom AI/Automation and software company. The proposal template is defined in the `generate_proposal_with_claude` function and includes:

1. An introduction about your company
2. A customized pitch showing understanding of the project
3. A closing paragraph suggesting a call to discuss the project

Modify the prompt in this function to adjust the proposal style and content to match your business.

### Flowchart Generation
For each job listing, the system generates a custom implementation flowchart using Mermaid.js. The flowchart visualizes the approach your team would take to complete the project, including:

1. Project phases organized in subgraphs
2. 8-12 detailed steps specific to the project requirements
3. Decision points where applicable
4. Professional styling with color-coded phases

The flowcharts are generated using the Claude API and shared as viewable links using Mermaid Live Editor.

## Usage

Once set up, the scraper will run automatically according to the schedule. You can also trigger it manually from the Actions tab in your GitHub repository.

For each job listing found, the system will:
1. Scrape the job details from Upwork
2. Generate a customized proposal using Claude AI
3. Send both to your Telegram chat

The message will contain:
- Job title and budget
- Brief description
- Posting date
- Direct link to the job
- Full AI-generated proposal

### Manual Job Processing

You can also manually process job descriptions to generate proposals and flowcharts without running the full scraper. This is useful for:

- Creating proposals for jobs you found manually
- Testing customized proposal formats
- Processing job descriptions from other sources

To use this feature, simply edit the variables "JOB_TITLE" and "JOB_DESCRIPTION" at the top of manual_job_processor.py and run the file

## Dependencies

- `apify-client`: Interface with Apify web scraping service
- `requests`: HTTP requests for API communication
- `python-dotenv`: Environment variable management

## Troubleshooting

Check the GitHub Actions logs for any errors. Common issues include:

- Invalid API tokens or authentication failures
- Rate limiting from Upwork, Telegram, or Claude APIs
- Proposal or flowchart generation failures (Claude API overloaded)

The script includes retry logic for API calls to handle temporary service disruptions.

## License

MIT

## Acknowledgments

This project uses:
- [Apify](https://apify.com/) for web scraping capabilities
- [Claude AI](https://www.anthropic.com/claude) for automated proposal generation
- Mermaid.js for flowchart visualization