import openai
import os
from dotenv import load_dotenv

load_dotenv()  # Load OPENAI_API_KEY from .env file

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_terraform(user_request):
    prompt = f"""
You are an AI DevOps Assistant. Based on the user request below, generate a complete Terraform configuration for provisioning infrastructure on DigitalOcean.
Ensure best practices in networking, security, and scalability.
Also include the following provider configuration:

terraform {{
  required_providers {{
    digitalocean = {{
      source  = "digitalocean/digitalocean"
      version = ">= 2.0.0"
    }}
  }}
}}

provider "digitalocean" {{
  token = "{'{'}{'}'}"   # Use the value from credentials.json (do_token)
}}

Additionally, generate a complete setup with no placeholders or manual actions.
Assume all required credentials (do_token and ssh_fingerprint) are stored in credentials.json.
Do not include variables or instructions like <path-to-your-public-ssh-key>; use the actual values from credentials.json.
Also, ensure that the generated configuration references the provider as "digitalocean/digitalocean" and not "hashicorp/digitalocean".

Important: Do not include any lifecycle attributes (such as prevent_destroy) that would prevent resource destruction.
Additionally, based on previous Terraform errors, please ensure:
- In the digitalocean_loadbalancer resource, remove unsupported arguments "interval" and "timeout".
- In the digitalocean_loadbalancer resource, remove unsupported arguments "healthy_thresh" and "unhealthy_thresh".
- In the digitalocean_loadbalancer resource, remove the unsupported argument "forward_rules" and use a "forwarding_rule" block instead.
- In the digitalocean_droplet resource, include the required "name" argument.
- Tags are not supported for load balancers; remove any "tags" argument from load balancer resources.
- Use ssh_keys = [...] instead of ssh_fingerprint in droplet resources.
- Do not include unsupported attributes; use supported arguments instead.
- Instead of resource type "digitalocean_product", use the supported type (e.g., "digitalocean_project") or omit if not applicable.
- To set up a load balancer, always use the following approach:

resource "digitalocean_loadbalancer" "web_lb" {{
  name               = "web-load-balancer"
  region             = "nyc1"
  size               = "lb-small"
  forwarding_rule {{
    entry_port     = 80
    entry_protocol = "http"
    target_port    = 80
    target_protocol = "http"
  }}
  
  droplet_ids      = digitalocean_droplet.web[*].id
}}

Also, do not wrap the output with language tags (do not include ```hcl at the beginning or end).

User request: "{user_request}"

Output only the complete Terraform code.
"""
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": prompt}],
    )
    return response.choices[0].message.content

def generate_ansible(user_request):
    prompt = f"""
You are an AI DevOps Assistant. Based on the user request below,
generate an Ansible playbook to configure the provisioned servers (e.g., install necessary packages, configure services).
Ensure that any placeholders (e.g., your-ssh-key-name, your.ip.address.here) are dynamically generated based on the rest of the configuration and not hardcoded.

User request: "{user_request}"

Output only the Ansible playbook in YAML format.
"""
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": prompt}],
    )
    return response.choices[0].message.content

def troubleshoot_logs(log_text):
    prompt = f"""
You are an AI DevOps Troubleshooter. Analyze the following logs and provide a root cause analysis along with a suggested fix (in Terraform or Ansible code) if applicable.

Logs:
{log_text}

Output your response as a clear, step-by-step analysis followed by your recommendation.
"""
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": prompt}],
    )
    return response.choices[0].message.content
