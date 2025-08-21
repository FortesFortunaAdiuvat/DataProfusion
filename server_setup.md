# Server Setup

This guide covers initial deployment of the Economy Charts application on an Ubuntu server and making it accessible from your local network. After completing these steps, continue with [domain_setup.md](domain_setup.md) to configure a public domain and HTTPS.

## 1. Prepare the Ubuntu Server
1. **Update the system and install dependencies:**
   ```bash
   sudo apt update && sudo apt upgrade -y
   sudo apt install python3 python3-venv python3-pip git -y
   ```
2. **(Optional) Enable the firewall and allow SSH:**
   ```bash
   sudo ufw allow OpenSSH
   sudo ufw enable
   ```

## 2. Obtain the Application
1. **Clone the repository and enter the directory:**
   ```bash
   git clone <repository-url>
   cd DataProfusion
   ```
2. **Create a virtual environment and install Python packages:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
3. **Configure API keys and settings:**
   ```bash
   python setup_config.py
   ```
   Follow the prompts or see [CONFIG_SETUP.md](CONFIG_SETUP.md) for details.

## 3. Run the Application
1. **Allow inbound traffic on the application port (example uses 8000):**
   ```bash
   sudo ufw allow 8000/tcp
   ```
2. **Start the application with Gunicorn so it listens on all interfaces:**
   ```bash
   pip install gunicorn
   gunicorn "app:create_app()" --bind 0.0.0.0:8000
   ```
   - Browse to `http://<SERVER_LOCAL_IP>:8000/dash/` from another device on the network to verify.
   - Replace `<SERVER_LOCAL_IP>` with the server's IP address, e.g. `192.168.1.50`.

## 4. Router Port Forwarding (Optional)
If you want to expose the application outside your local network before setting up a domain:

1. **Find the server's local IP address:**
   ```bash
   ip addr show
   ```
2. **Log into your router's admin interface** (often `http://192.168.0.1` or `http://192.168.1.1`).
3. **Create a port forwarding rule** that maps an external port (e.g. `8000` or `80`) to the server's local IP and port `8000`.
4. **Apply or save the settings** and restart the router if required.
5. **Verify from an external network** by visiting `http://<YOUR_PUBLIC_IP>:<FORWARDED_PORT>/dash/`.

## 5. Next Steps
With the application running and reachable on your network, proceed to [domain_setup.md](domain_setup.md) for instructions on pointing a domain to your server and securing it with HTTPS.
