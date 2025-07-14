from messaging import build_connection_message
from llm import generate_followup
# Note: send_connection function doesn't exist in phantom module

# 1. Define the contact entry
contact_entry = {
    "linkedin_url": "www.linkedin.com/in/kon-anagn",
    "firstName": "Konstantinos",
    "company": "",    # Optional: Fill in if you know it!
    "jobTitle": "",   # Optional: Fill in if you know it!
    "variant": 0
}

# 2. Build the connection message
connection_message = build_connection_message(contact_entry)
print("Connection Message to Send:")
print(connection_message)

# 3. Send the connection via PhantomBuster (optional)
# Note: Use the main automation system instead of direct send_connection
result = send_connection(contact_entry["linkedin_url"], connection_message)
print("PhantomBuster Response:", result)

# 4. Generate the follow-up message using DeepSeek LLM
followup_msg = generate_followup(
    contact_entry["firstName"],
    contact_entry["company"],
    contact_entry["jobTitle"]
)
print("\nLLM-generated Follow-up Message:")
print(followup_msg)
