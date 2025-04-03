import requests
import time
import os
import logging
import json
import re

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Get credentials from environment variables
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "TELEGRAM_CHAT_ID")
CLAUDE_API_KEY = os.environ.get("CLAUDE_API_KEY", "CLAUDE_API_KEY")

# ========================
# EDIT THESE VARIABLES FOR EACH NEW JOB
# ========================

# Job details - update these variables for each new job
JOB_TITLE = "AI-Powered Analytics Dashboard"
JOB_DESCRIPTION = """
We need a developer to create an analytics dashboard that uses AI to provide insights from our customer data. The dashboard should:
1. Connect to our existing PostgreSQL database
2. Analyze customer behavior patterns
3. Provide visualizations of key metrics
4. Use machine learning to identify trends and make predictions
5. Include a user-friendly interface for our marketing team

The ideal solution will be built with modern web technologies and integrate with our existing systems.
"""

# ========================
# DON'T MODIFY BELOW THIS LINE
# ========================

def generate_mermaid_flowchart(job_title, job_description, skills_list=None):
    """
    Generate a customized Mermaid flowchart code based on job details using Claude
    Returns the Mermaid code and a shareable URL to view the flowchart
    """
    logging.info(f"Generating custom flowchart for: {job_title}")
    
    if skills_list is None:
        skills_list = []
    
    # Claude API endpoint
    url = "https://api.anthropic.com/v1/messages"
    
    # Construct a prompt that asks Claude to generate a Mermaid.js flowchart
    prompt = f"""
    Create a professional Mermaid.js flowchart diagram showing our implementation approach for this job:
    
    Job Title: {job_title}
    
    Job Description: {job_description}
    
    Required Skills: {', '.join(skills_list) if skills_list else 'Not specified'}
    
    Please create a detailed, customized flowchart that demonstrates our project approach for this specific job.
    The flowchart should:
    1. Include 8-12 steps that are specifically tailored to this project
    2. Use appropriate industry terminology relevant to this job
    3. Show a logical progression from project initiation to completion
    4. Include decision points if applicable to this type of project
    5. Use subgraphs to organize phases of the project
    6. Include professional styling with colors that enhance readability
    
    Use Mermaid.js flowchart TD (top-down) syntax. Here's an example of the format:
    
    ```mermaid
    flowchart TD
        subgraph Phase1[Project Initiation]
            A[Start] --> B[Requirements Gathering]
            B --> C[Technical Assessment]
        end
        
        subgraph Phase2[Development]
            C --> D[Architecture Design]
            D --> E[Implementation]
            E --> F[Unit Testing]
        end
        
        subgraph Phase3[Quality Assurance]
            F --> G[Integration Testing]
            G --> H[User Acceptance]
        end
        
        subgraph Phase4[Deployment]
            H --> I[Production Release]
            I --> J[Maintenance Plan]
        end
        
        style Phase1 fill:#e1f5fe,stroke:#01579b,stroke-width:2px
        style Phase2 fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
        style Phase3 fill:#fff8e1,stroke:#ff8f00,stroke-width:2px
        style Phase4 fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    ```
    
    But that's just a generic example. Your flowchart should be completely customized to match the specific requirements, technologies, and processes relevant to this job posting.
    
    ONLY return the Mermaid.js code, nothing else. No explanations or additional text.
    """
    
    # Set up request headers and payload for Claude API
    headers = {
        "x-api-key": CLAUDE_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    
    payload = {
        "model": "claude-3-5-sonnet-20240620",
        "max_tokens": 1500,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    
    # Retry settings
    max_retries = 3
    retry_delay = 5  # seconds
    current_retry = 0
    
    while current_retry < max_retries:
        try:
            # Make the API call to Claude
            response = requests.post(url, headers=headers, json=payload)
            response_data = response.json()
            
            # Check for successful response
            if response.status_code == 200 and 'content' in response_data:
                mermaid_code = response_data['content'][0]['text']
                
                # Clean up the response to extract just the Mermaid code
                # Remove any markdown code block syntax if present
                mermaid_code = re.sub(r'```mermaid\s*', '', mermaid_code)
                mermaid_code = re.sub(r'```\s*$', '', mermaid_code)
                mermaid_code = mermaid_code.strip()
                
                logging.info("Successfully generated custom Mermaid flowchart")
                
                # Create a shareable URL using Mermaid Live Editor
                mermaid_live_url = create_mermaid_live_url(mermaid_code)
                
                return mermaid_code, mermaid_live_url
            
            # Check specifically for overloaded error
            elif response_data.get('error', {}).get('type') == 'overloaded_error':
                current_retry += 1
                wait_time = retry_delay * current_retry
                logging.warning(f"Claude API overloaded. Retry {current_retry}/{max_retries} after {wait_time}s")
                time.sleep(wait_time)
                continue
            
            # Other errors - don't retry
            else:
                logging.error(f"Failed to generate Mermaid flowchart: {response_data}")
                return None, None
                
        except Exception as e:
            logging.error(f"Exception calling Claude API: {str(e)}")
            return None, None
    
    # If we've exhausted all retries
    return None, None

def create_mermaid_live_url(mermaid_code):
    """
    Create a shareable URL for the Mermaid flowchart using Mermaid Live Editor
    """
    # Prepare the JSON data for Mermaid Live Editor
    mermaid_state = {
        "code": mermaid_code,
        "mermaid": {
            "theme": "default"
        },
        "updateEditor": True,
        "autoSync": True,
        "updateDiagram": True
    }
    
    # Convert the state to a base64 encoded string
    import base64
    state_json = json.dumps(mermaid_state)
    state_bytes = state_json.encode('utf-8')
    state_base64 = base64.b64encode(state_bytes).decode('utf-8')
    
    # Create the shareable URL
    mermaid_live_url = f"https://mermaid.live/edit#base64:{state_base64}"
    
    return mermaid_live_url

def generate_proposal_with_claude(job_title, job_description, skills_list=None, budget=None, flowchart_url=None):
    """
    Generate a job proposal using Claude API based on the job details
    """
    logging.info(f"Generating proposal for: {job_title}")
    
    if skills_list is None:
        skills_list = []
    if budget is None:
        budget = "Not specified"
    
    # Claude API endpoint
    url = "https://api.anthropic.com/v1/messages"
    
    # Add flowchart information to the prompt if available
    flowchart_info = ""
    if flowchart_url:
        flowchart_info = f"""
        I have also created a custom project implementation flowchart for this job, which can be viewed at: {flowchart_url}
        
        Please mention this flowchart in the proposal and explain that it shows our implementation approach specifically designed for this project. Encourage the client to view it to understand our methodology.
        """
    
    # Construct a prompt that gives Claude context on what to generate
    prompt = f"""
    Job Title: {job_title}
    
    Job Description: {job_description}
    
    Required Skills: {', '.join(skills_list) if skills_list else 'Not specified'}
    
    Budget: {budget}
    
    {flowchart_info}
    
    I am trying to obtain jobs on upwork as a co-founder of tmplogic, which is a small custom AI/Automation and software company. I need claude to be able to generate properly structured proposals based off of the job listing that I provide. 
    
    The first part of the proposal should start with "I run a small custom AI, automation, and software company where all of the dev work is done by my partner and I" should be a background about tmplogic and how confindent we are that we can deliver because of our related skills. Keep it short and simple. 
    
    The next part of the proposal is to format a customized sales pitch explaining that we understand how to complete and deliver the project. Do not re iterate that the project is good for us or right up our alley or anything like that in the 2nd paragraph. The 2nd paragraph is meant do a couple things, 
    
    we want to inform the potential client smart routes to take when working on the specified project, and then reassure the potential client that we are a good fit and want to schedule and introductory call about the potential of working on the project togther. 
    
    This should be a conversational response. It does not have to be very long to get the point across.

    This should look as if a human is writing this, not ai. dont have any crazy formatting. dont mention the timeline, nor, how much money.

    The response should consists of 3 main paragraphs. The intro about tmplogic/confident we can deliver the project, the response to the job listing, and then a closing paragraph that just contains writing about having an introduction call and potentially working on the project together

    The closing paragraph should only have 2-3 sentences. It should include how we went ahead and made them and customized flowchart for the project.

    it should start off with "Hey!"

    Do not include any names of people. Do not say "wheelhouse". Do not say we have directly done the same project before.

    Let them know that they will have a team of skilled developers on the project.
    """
    
    # Set up request headers and payload for Claude API
    headers = {
        "x-api-key": CLAUDE_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    
    payload = {
        "model": "claude-3-5-sonnet-20240620",
        "max_tokens": 1000,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    
    # Retry settings
    max_retries = 3
    retry_delay = 5  # seconds
    current_retry = 0
    
    while current_retry < max_retries:
        try:
            # Make the API call to Claude
            response = requests.post(url, headers=headers, json=payload)
            response_data = response.json()
            
            # Check for successful response
            if response.status_code == 200 and 'content' in response_data:
                proposal_text = response_data['content'][0]['text']
                logging.info("Successfully generated proposal with Claude")
                return proposal_text
            
            # Check specifically for overloaded error
            elif response_data.get('error', {}).get('type') == 'overloaded_error':
                current_retry += 1
                wait_time = retry_delay * current_retry
                logging.warning(f"Claude API overloaded. Retry {current_retry}/{max_retries} after {wait_time}s")
                time.sleep(wait_time)
                continue
            
            # Other errors - don't retry
            else:
                logging.error(f"Failed to generate proposal: {response_data}")
                return f"Unable to generate proposal due to API error. Please check logs."
                
        except Exception as e:
            logging.error(f"Exception calling Claude API: {str(e)}")
            return f"Error calling Claude API: {str(e)}"
    
    # If we've exhausted all retries
    return "Could not generate proposal after multiple attempts. Claude API may be experiencing high traffic."

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": False  # Allow link previews
    }
    try:
        response = requests.post(url, data=payload)
        result = response.json()
        if not result.get('ok'):
            logging.error(f"Telegram error: {result}")
        return result
    except Exception as e:
        logging.error(f"Exception sending Telegram message: {str(e)}")
        return {"ok": False, "error": str(e)}

def process_job():
    """
    Process the job using the global variables defined at the top of the script
    """
    logging.info(f"Processing job: {JOB_TITLE}")
    
    # Extract skills (this is a simple implementation - you can improve it)
    # This attempts to find skills mentioned in the job description
    common_skills = ["Python", "JavaScript", "React", "Node.js", "Django", "Machine Learning", 
                    "AI", "Data Analysis", "AWS", "Docker", "API", "Database", "SQL", 
                    "Full Stack", "Frontend", "Backend", "DevOps", "TensorFlow", "PyTorch"]
    
    skills = []
    for skill in common_skills:
        if skill.lower() in JOB_DESCRIPTION.lower():
            skills.append(skill)
    
    # Generate flowchart
    _, flowchart_url = generate_mermaid_flowchart(
        job_title=JOB_TITLE,
        job_description=JOB_DESCRIPTION,
        skills_list=skills
    )
    
    # Generate proposal
    proposal = generate_proposal_with_claude(
        job_title=JOB_TITLE,
        job_description=JOB_DESCRIPTION,
        skills_list=skills,
        budget=None,  # No budget needed
        flowchart_url=flowchart_url
    )
    
    # Format message for Telegram
    message = (
        f"<b>📋 MANUAL JOB PROCESSING</b>\n\n"
        f"<b>🔹 {JOB_TITLE}</b>\n\n"
        f"<b>📝 PROPOSAL:</b>\n{proposal}\n\n"
        f"<b>📝 FLOWCHART:</b>\n{flowchart_url}\n\n"
    )
    
    # Send to Telegram
    result = send_telegram_message(message)
    if result.get('ok'):
        logging.info("Sent results to Telegram successfully")
        return True
    else:
        logging.error("Failed to send results to Telegram")
        return False

if __name__ == "__main__":
    # Run the processor
    success = process_job()
    
    if success:
        print("✅ Job processed and sent to Telegram successfully!")
    else:
        print("❌ Failed to process job or send to Telegram. Check logs for details.")