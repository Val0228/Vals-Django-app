# Email Setup Guide for Password Reset

## Overview
The password reset feature is already configured with email templates that include clickable reset links. This guide explains how to configure email sending.

## Current Status
✅ Email templates are created with reset links
✅ Password reset URLs are configured
✅ Email backend is configurable

## How to Send Real Emails

### Option 1: Gmail (Recommended for Testing)

1. **Enable App Password in Gmail:**
   - Go to your Google Account settings
   - Enable 2-Step Verification
   - Generate an App Password for "Mail"
   - Copy the 16-character password

2. **Set Environment Variables in PowerShell:**
   ```powershell
   $env:EMAIL_HOST = "smtp.gmail.com"
   $env:EMAIL_PORT = "587"
   $env:EMAIL_USE_TLS = "True"
   $env:EMAIL_HOST_USER = "your-email@gmail.com"
   $env:EMAIL_HOST_PASSWORD = "your-app-password"
   $env:DEFAULT_FROM_EMAIL = "your-email@gmail.com"
   $env:SITE_DOMAIN = "localhost:8000"  # For local testing
   ```

3. **Restart the Django server:**
   ```powershell
   cd "C:\Users\valer\OneDrive\Desktop\Cloud App\Vals-Django-app\itapps"
   python manage.py runserver
   ```

### Option 2: Other SMTP Providers

**For Outlook/Office 365:**
```powershell
$env:EMAIL_HOST = "smtp.office365.com"
$env:EMAIL_PORT = "587"
$env:EMAIL_USE_TLS = "True"
$env:EMAIL_HOST_USER = "your-email@outlook.com"
$env:EMAIL_HOST_PASSWORD = "your-password"
```

**For Yahoo:**
```powershell
$env:EMAIL_HOST = "smtp.mail.yahoo.com"
$env:EMAIL_PORT = "587"
$env:EMAIL_USE_TLS = "True"
$env:EMAIL_HOST_USER = "your-email@yahoo.com"
$env:EMAIL_HOST_PASSWORD = "your-app-password"
```

### Option 3: Console Backend (Default - For Testing)

If you don't set email credentials, emails will be printed to the console/terminal. This is useful for testing:

1. Request a password reset
2. Check the terminal/console output
3. Copy the reset link from the console
4. Paste it in your browser

## Email Template

The email includes:
- A personalized greeting
- A clickable password reset link
- Instructions for manual copy/paste
- Security notice

**Example email link format:**
```
http://localhost:8000/password-reset-confirm/MQ/abc123xyz-token-here/
```

## Testing the Password Reset

1. Go to the login page: `http://localhost:8000/login/`
2. Click "Reset Password"
3. Enter a registered email address
4. Check your email (or console if using console backend)
5. Click the reset link in the email
6. Enter your new password
7. Login with the new password

## Production Setup

For production (Azure deployment), set these environment variables in Azure:

- `EMAIL_HOST` - Your SMTP server
- `EMAIL_PORT` - SMTP port (usually 587)
- `EMAIL_USE_TLS` - "True" or "False"
- `EMAIL_HOST_USER` - Your email address
- `EMAIL_HOST_PASSWORD` - Your email password or app password
- `DEFAULT_FROM_EMAIL` - Sender email address
- `SITE_DOMAIN` - Your production domain (e.g., `yourapp.azurewebsites.net`)

## Troubleshooting

**Email not sending:**
- Check that environment variables are set correctly
- Verify SMTP credentials are correct
- Check firewall/network settings
- For Gmail, ensure you're using an App Password, not your regular password

**Link not working:**
- Ensure `SITE_DOMAIN` matches your actual domain
- Check that `ALLOWED_HOSTS` includes your domain
- Verify the token hasn't expired (links expire after 1 day by default)

**Console backend not showing emails:**
- Make sure no email credentials are set
- Check the terminal where `runserver` is running
- Look for email output in the console

