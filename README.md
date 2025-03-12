## Currently Only Works With Digital Ocean

# CloudAI Project

## Overview
CloudAI is a cloud-based AI DevOps assistant that uses Terraform and Ansible to provision and configure digital infrastructure automatically. It leverages OpenAI to generate configurations based on user-provided requests, ensuring best practices in cloud deployment.

## Features
- Generate Terraform configurations based on user input.
- Generate Ansible playbooks for post-provisioning server configurations.
- Versioning of configuration files.
- Automated deployment and destruction of infrastructure.

## Setup and Installation
1. Clone the repository:
   ```
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```
   cd cloudai
   ```
3. Install dependencies:
   - For Python projects:
     ```
     pip install -r requirements.txt
     ```
4. Configure environment:
   - Create a `.env` file in the project root with your OpenAI API key:
     ```
     OPENAI_API_KEY=your_api_key_here
     ```
   - Update `credentials.json` or use the credentials page in the app to save your DigitalOcean token and SSH fingerprint.

## Usage
- Start the Flask application:
  ```
  python app.py
  ```
- Access the application in your browser at `http://127.0.0.1:5000/`.
- Use the UI to:
  - Save credentials.
  - Generate and deploy Terraform configurations.
  - Apply or destroy Terraform-managed resources.
  - Troubleshoot issues with generated logs.

## Contributing
Contributions are welcome. Please check the contributing guidelines for details on how to submit PRs.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
