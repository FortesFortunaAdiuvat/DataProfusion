# Domain Setup

## DNS: Point Squarespace to your server
1. Sign in to Squarespace and navigate to **Settings → Domains → [your domain] → DNS settings**.
2. Delete any existing A or AAAA records Squarespace created by default.
3. Add new records pointing to your server:
   - **A record**: `@` (or leave Host blank) → `YOUR_IPV4_ADDRESS`
   - **AAAA record** (if your server has IPv6): `@` → `YOUR_IPV6_ADDRESS`
4. Save the changes and allow DNS propagation (often 15–30 minutes, sometimes longer).
5. Verify from a terminal on another network:
   ```bash
   dig +short yourdomain.com
   dig +short AAAA yourdomain.com   # if using IPv6
   ```

## TLS certificates with Let’s Encrypt (Certbot)
1. SSH into your server.
2. Install Certbot and the Nginx plugin (Ubuntu example):
   ```bash
   sudo apt update
   sudo apt install certbot python3-certbot-nginx
   ```
3. Obtain certificates and automatically configure Nginx:
   ```bash
   sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
   ```
   - Follow the prompts to supply an email and agree to the terms of service.
   - Certbot edits your Nginx configuration to use the new certificate.
4. Certbot installs a systemd timer or cron job by default for auto-renewal. Confirm:
   ```bash
   systemctl list-timers | grep certbot
   ```
   If not, create a cron entry:
   ```bash
   sudo crontab -e
   # Add:
   0 3 * * * /usr/bin/certbot renew --quiet
   ```

## Nginx: Redirect HTTP → HTTPS and serve site
1. Edit your Nginx server block for the domain, typically in `/etc/nginx/sites-available/yourdomain.com`:
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com www.yourdomain.com;
       return 301 https://$host$request_uri;
   }

   server {
       listen 443 ssl;
       server_name yourdomain.com www.yourdomain.com;

       ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
       ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

       root /var/www/your-site;
       index index.html index.htm;

       # other configuration, proxy_pass, etc.
   }
   ```
2. Test the configuration:
   ```bash
   sudo nginx -t
   ```
3. Reload Nginx:
   ```bash
   sudo systemctl reload nginx
   ```
4. Visit `https://yourdomain.com` in a browser to confirm HTTPS and redirect.

## Ongoing
- Certbot’s renewal timer will attempt to renew certificates automatically. After renewal, Nginx reloads to pick up new certificates.
- Monitor renewal logs:
  ```bash
  sudo journalctl -u certbot.service
  ```
- To test renewal manually:
  ```bash
  sudo certbot renew --dry-run
  ```

