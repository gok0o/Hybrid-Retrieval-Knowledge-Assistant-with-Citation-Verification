---
product: "FlowDesk"
version: "3.2"
access_level: "public"
document_id: "API-001"
source_name: "Bearer Token Authentication"
section_heading: "Bearer Token Authentication"
last_updated: "2026-07-15"
document_type: "api"
---

# API Authentication
## Bearer tokens
FlowDesk API requests require a Bearer token in the Authorization header.

Example:
Authorization: Bearer <API_TOKEN>

Tokens should be treated as secrets and must not be exposed in client-side code.
