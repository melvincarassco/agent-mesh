# 01. Creating a Google Cloud Platform (GCP) Account

This guide walks you through setting up a Google Cloud Platform account, activating the free tier, and configuring budget alerts to ensure cost safety.

## 1. Prerequisites

- A valid Google account (Gmail or Google Workspace).
- A credit card or debit card (required by Google for identity verification; no charges are made during the trial).

## 2. Sign Up for GCP

1. Navigate to the [Google Cloud Console](https://console.cloud.google.com/).
2. Click **Get Started for Free**.
3. Select your country and accept the Terms of Service.
4. Complete the payment profile verification.

> **Free Tier Benefits:**
> - $300 free credits for the first 90 days.
> - Always Free tier limits for Cloud Run (2 million requests/month), Cloud Storage (5 GB), and Google Cloud Build.

## 3. Set Up Budget & Billing Alerts

To avoid unexpected charges:

1. Open the GCP Console and search for **Billing**.
2. Go to **Budgets & alerts** > **Create Budget**.
3. Set the target budget (e.g., $1.00 or $10.00).
4. Set threshold rules (50%, 90%, and 100% of budget).
5. Add your email address to receive real-time alert notifications.

## 4. Next Steps

Proceed to [02-install-gcloud-cli.md](02-install-gcloud-cli.md) to install and configure the Google Cloud SDK.
