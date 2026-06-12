# API Integration & Developer Guide

# Purpose

This document provides the official integration guide for SenAI CRM APIs, authentication mechanisms, versioning strategy, event ingestion, webhook security, rate limiting, idempotency, error handling, and escalation procedures. It serves as the primary reference for developers, support engineers, AI agents, and customer success teams assisting API customers.

---

# Guiding Principles

- APIs should be secure by default.
- Authentication credentials must never be exposed.
- API integrations should be idempotent wherever possible.
- AI agents may explain APIs but must not invent undocumented behavior.
- Integration failures affecting production launches require priority handling.

---

# API Versions

SenAI currently supports:

- API Version 1 (Legacy)
- API Version 2 (Recommended)

New integrations should use Version 2 whenever possible.

Legacy integrations continue to be supported according to the published deprecation schedule.

---

# Authentication

Authentication is performed using scoped API Keys.

Every request must include:

Authorization:

Bearer YOUR_API_KEY

API keys are associated with:

- Workspace
- Organization
- Scope
- Environment

Never request or expose API keys over email.

If a customer accidentally shares a key, recommend immediate rotation.

---

# API Scopes

Supported scopes include:

- crm.read
- crm.write
- webhook.manage
- analytics.read
- contacts.read
- contacts.write
- events.write

Insufficient scopes may result in HTTP 403 responses.

---

# Version 2 Event Ingestion

Event ingestion requires:

- events.write scope
- webhook signing enabled
- valid timestamp
- signature verification
- correct workspace association

Missing any requirement may cause authorization failure.

---

# Event Flow

Client

↓

Authentication

↓

Signature Validation

↓

Workspace Validation

↓

Idempotency Check

↓

Event Processing

↓

Audit Log

↓

Response

---

# Webhook Security

Webhook requests should include:

- timestamp
- signature
- event id
- workspace id

Replay attacks should be rejected.

Expired signatures should not be accepted.

Webhook secrets should be rotated periodically.

---

# Signature Validation

Before accepting webhook events:

- validate timestamp
- validate signature
- validate workspace
- validate scope
- validate payload

Reject invalid requests.

Record audit logs.

---

# Idempotency

Every event should contain a unique identifier.

Duplicate event identifiers should not create duplicate records.

The server should return a successful response for already processed events without repeating business logic.

Idempotency protects against retries and webhook replay.

---

# Duplicate Event Handling

When duplicate event_id values are received:

- detect existing record
- skip processing
- return success response
- log duplicate event

Never create duplicate customer records.

---

# Rate Limiting

Rate limits vary by subscription.

## Starter

Standard throughput

## Growth

Burst capacity for imports

## Enterprise

Custom negotiated limits

AI should never promise increased rate limits.

Rate increases require approval.

---

# Pagination

Large collections support pagination.

Typical parameters:

page

page_size

cursor

next_token

Clients should avoid requesting excessively large result sets.

---

# Filtering

Supported filters may include:

status

created_after

updated_after

customer

priority

category

workspace

date range

Use indexed fields whenever possible.

---

# Sorting

Typical sort fields:

created_at

updated_at

priority

customer

status

subject

Ascending and descending order should be supported.

---

# Error Codes

## 200

Request successful.

---

## 201

Resource created.

---

## 400

Malformed request.

Verify payload structure.

---

## 401

Authentication failed.

Verify API key.

---

## 403

Permission denied.

Verify scopes.

Verify workspace.

Verify allowlist.

---

## 404

Requested resource not found.

---

## 409

Duplicate resource or idempotency conflict.

---

## 422

Validation failed.

Correct request fields.

---

## 429

Rate limit exceeded.

Retry after recommended delay.

---

## 500

Unexpected server error.

Escalate if persistent.

---

# Common 403 Causes

403 errors commonly occur because:

- missing events.write scope
- incorrect workspace
- expired credentials
- IP allowlist restrictions
- invalid signature
- disabled integration

Support should verify all conditions before escalation.

---

# Launch Critical Integrations

If:

- production go-live is within 72 hours
- integration is blocked
- customer cannot ingest events

Immediately escalate to Developer Support.

High-priority onboarding should not wait for standard queues.

---

# Retry Strategy

Recommended retry intervals:

Attempt 1

Immediate

Attempt 2

30 seconds

Attempt 3

2 minutes

Attempt 4

10 minutes

Attempt 5

30 minutes

Use exponential backoff.

Avoid retry storms.

---

# Timeout Recommendations

Client timeout:

30 seconds

Webhook acknowledgement:

Within 5 seconds

Long-running operations should be asynchronous.

---

# API Version Migration

When migrating from V1 to V2:

- update endpoints
- verify scopes
- enable webhook signing
- update payload schema
- test idempotency
- validate signatures

Migration should be completed before deprecation deadlines.

---

# Security Events

Immediately escalate:

- leaked API key
- suspicious authentication
- replay attacks
- brute-force attempts
- webhook abuse
- credential compromise
- unauthorized access

Do not disclose investigation details.

---

# AI Agent Guidance

Before answering integration questions, retrieve:

- API Guide
- CRM Profile
- Thread History
- Escalation Matrix

AI may:

- explain documented APIs
- explain authentication
- explain scopes
- explain rate limits

AI must never:

- invent undocumented endpoints
- expose secrets
- promise rate limit increases
- bypass authentication requirements

---

# Example Scenario 1

Customer:

> "Why do I receive HTTP 403 on /v2/events?"

Recommended Action:

- verify events.write scope
- verify workspace
- verify webhook signing
- verify timestamp
- verify signature
- verify IP allowlist

---

# Example Scenario 2

Customer:

> "Can you increase my API rate limit?"

Recommended Action:

- explain current plan
- explain Enterprise custom limits
- recommend Account Manager discussion

Do not promise approval.

---

# Example Scenario 3

Customer:

> "Our webhook keeps processing the same event twice."

Recommended Action:

- verify idempotency implementation
- verify event_id uniqueness
- inspect retry logic
- recommend duplicate detection

---

# Frequently Asked Questions

## Can AI create API keys?

No.

---

## Can AI rotate credentials?

No.

---

## Can AI explain authentication?

Yes.

---

## Can AI approve rate limit increases?

No.

---

## Can duplicate webhook events be ignored?

Yes.

If idempotency is correctly implemented.

---

## Should leaked API keys be rotated immediately?

Yes.

Treat credential exposure as a security incident.

---

# Retrieval Keywords

API

REST

authentication

Bearer token

API key

events.write

crm.read

crm.write

webhook

signature

idempotency

duplicate event

403

401

429

500

rate limit

pagination

filtering

sorting

retry

backoff

integration

developer support

migration

v2 events

webhook replay

security

credential leak

workspace

allowlist

event ingestion

audit log

developer onboarding

production integration

launch blocker