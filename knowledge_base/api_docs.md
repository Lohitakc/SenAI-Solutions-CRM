# API Integration Guide

SenAI customers authenticate with scoped API keys. Version 1 endpoints use the `crm.read`, `crm.write`, and `webhook.manage` scopes. Version 2 event ingestion requires the additional `events.write` scope and webhook signing enabled in the admin console.

For `403` responses on `/v2/events`, verify that the key belongs to the correct workspace, the integration has `events.write`, the sender IP is allowlisted when enterprise network controls are enabled, and the request includes a valid timestamped signature. Launch-blocking integration issues should be escalated to developer support when the customer has an active go-live date inside 72 hours.

Rate limits are plan-specific. Team plans receive standard limits, Growth plans receive burst capacity for imports, and Enterprise plans may have custom high-throughput limits. Do not promise limit increases in a customer reply without account manager approval.

Security alerts involving suspicious login, credential exposure, ransomware, webhook replay attacks, or data exfiltration must be routed to security immediately. Customer-facing replies should acknowledge receipt and confirm escalation without disclosing internal investigation details.
