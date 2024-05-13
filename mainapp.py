import openai
import requests
import json

# Set up OpenAI API credentials
openai.api_key = "your_openai_api_key"

# Set up Mailgun API credentials
mailgun_api_key = "your_mailgun_api_key"
mailgun_domain = "your_mailgun_domain"

# Email template
email_template = """
Subject: Personalized Email for {{first_name}}

Dear {{first_name}},

<LLM Editable>
We hope this email finds you well. We wanted to reach out and offer a personalized message just for you.
</LLM Editable>

Thank you for being a valued customer.

Best regards,
The Team
"""

# Function to retrieve user data (replace with your own data source)
def get_user_data(user_id):
    # Replace this with your own logic to fetch user data based on the user_id
    user_data = {
        "user_id": user_id,
        "first_name": "John",
        "last_name": "Doe",
        "email": f"{user_id}@example.com",
        # Add more user data fields as needed
    }
    return user_data

# Function to generate personalized email content using OpenAI
def generate_email_content(user_data, email_template):
    prompt = f"Given the following user data: {user_data}\n\nAnd the email template:\n{email_template}\n\nPlease fill in the content within the <LLM Editable> tag to create a personalized email body for the user."
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=200,
        n=1,
        stop=None,
        temperature=0.7,
    )
    email_body = response.choices[0].text.strip()
    return email_body

# Function to send personalized email using Mailgun API
def send_email(user_data, email_content):
    endpoint = f"https://api.mailgun.net/v3/{mailgun_domain}/messages"
    auth = ("api", mailgun_api_key)
    data = {
        "from": "Your Name <youremail@yourdomain.com>",
        "to": [user_data["email"]],
        "subject": email_content.split("\n")[0].replace("Subject: ", ""),
        "text": email_content.split("\n", 1)[1].strip(),
    }
    response = requests.post(endpoint, auth=auth, data=data)
    return response.status_code

# Main function to orchestrate the process
def main():
    # List of user IDs to generate personalized emails for
    user_ids = ["user_id_1", "user_id_2", "user_id_3"]

    for user_id in user_ids:
        # Retrieve user data
        user_data = get_user_data(user_id)

        # Generate personalized email content using OpenAI
        email_content = generate_email_content(user_data, email_template)

        # Replace template variables with user data
        email_content = email_content.replace("{{first_name}}", user_data["first_name"])

        # Send personalized email using Mailgun API
        status_code = send_email(user_data, email_content)
        print(f"Email sent to user {user_id} with status code {status_code}")

if __name__ == "__main__":
    main()
