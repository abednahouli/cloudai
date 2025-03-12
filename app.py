# app.py

from flask import Flask, render_template, request, redirect, url_for, flash
import subprocess
import os

from credentials import store_credentials, get_credentials
from ai_agent import generate_terraform, generate_ansible, troubleshoot_logs
from versioning import (
    save_versioned_file,
    list_versions,
    restore_version,
    get_newest_terraform_file
)

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Replace with a secure key

TERRAFORM_DIR = "terraform_versions"
ANSIBLE_DIR = "ansible_versions"

@app.route("/")
def index():
    creds = get_credentials()
    return render_template("index.html", credentials_set=creds is not None)

@app.route("/credentials", methods=["GET", "POST"])
def credentials():
    if request.method == "POST":
        do_token = request.form.get("do_token")
        ssh_fingerprint = request.form.get("ssh_fingerprint")
        if do_token and ssh_fingerprint:
            store_credentials(do_token, ssh_fingerprint)
            flash("Credentials saved successfully.", "success")
            return redirect(url_for("index"))
        else:
            flash("Please provide both the API token and SSH fingerprint.", "danger")
    return render_template("credentials.html")

@app.route("/deploy", methods=["GET", "POST"])
def deploy():
    if request.method == "POST":
        user_request = request.form.get("user_request")
        if user_request:
            terraform_code = generate_terraform(user_request)
            ansible_code = generate_ansible(user_request)
            tf_file = save_versioned_file(TERRAFORM_DIR, "terraform", terraform_code, "tf")
            ansible_file = save_versioned_file(ANSIBLE_DIR, "ansible", ansible_code, "yml")
            flash("Configurations generated and saved.", "success")
            return render_template("deploy.html", terraform=terraform_code, ansible=ansible_code,
                                   tf_file=tf_file, ansible_file=ansible_file)
        else:
            flash("Please enter your infrastructure request.", "danger")
    return render_template("deploy.html")

@app.route("/troubleshoot", methods=["GET", "POST"])
def troubleshoot():
    if request.method == "POST":
        log_text = request.form.get("log_text")
        if log_text:
            analysis = troubleshoot_logs(log_text)
            return render_template("troubleshoot.html", analysis=analysis, log_text=log_text)
        else:
            flash("Please enter log text.", "danger")
    return render_template("troubleshoot.html")

@app.route("/versions")
def versions():
    tf_versions = list_versions(TERRAFORM_DIR)
    ansible_versions = list_versions(ANSIBLE_DIR)
    return render_template("versions.html", tf_versions=tf_versions, ansible_versions=ansible_versions)

@app.route("/restore", methods=["GET", "POST"])
def restore():
    content = None
    version_name = None
    if request.method == "POST":
        file_type = request.form.get("file_type")
        index = int(request.form.get("index"))
        directory = TERRAFORM_DIR if file_type == "terraform" else ANSIBLE_DIR
        result = restore_version(directory, index)
        if result:
            content, version_name = result
        else:
            flash("Invalid version index.", "danger")
    return render_template("restore.html", content=content, version_name=version_name)

# NEW ROUTE: Apply the newest Terraform file
@app.route("/apply_newest", methods=["POST"])
def apply_newest():
    newest_tf = get_newest_terraform_file(TERRAFORM_DIR)
    if not newest_tf:
        flash("No Terraform files found. Please generate a configuration first.", "danger")
        return redirect(url_for("index"))

    # Copy newest file to 'main.tf' so Terraform can detect it
    try:
        if os.path.exists("main.tf"):
            os.remove("main.tf")  # optional, remove old main.tf
        subprocess.run(["cp", newest_tf, "main.tf"], check=True)

        # Initialize and apply
        subprocess.run(["terraform", "init"], check=True)
        subprocess.run(["terraform", "plan"], check=True)
        subprocess.run(["terraform", "apply", "-auto-approve"], check=True)

        flash(f"✅ Successfully deployed using {newest_tf}", "success")
    except subprocess.CalledProcessError as e:
        flash(f"Terraform deployment failed: {e}", "danger")

    return redirect(url_for("index"))

# NEW ROUTE: Destroy Terraform Resources
@app.route("/destroy", methods=["POST"])
def destroy():
    try:
        subprocess.run(["terraform", "destroy", "-auto-approve"], check=True)
        flash("Terraform resources destroyed successfully.", "success")
    except subprocess.CalledProcessError as e:
        flash(f"Terraform destroy failed: {e}", "danger")
    return redirect(url_for("index"))

if __name__ == "__main__":
    os.makedirs(TERRAFORM_DIR, exist_ok=True)
    os.makedirs(ANSIBLE_DIR, exist_ok=True)
    app.run(debug=True)
