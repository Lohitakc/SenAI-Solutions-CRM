# Escalation Matrix

# Purpose

This document defines the escalation rules, ownership, approval requirements, and AI behavior for customer communications requiring human intervention. The goal is to ensure critical issues are routed to the appropriate teams while preventing unsafe or unauthorized AI actions.

---

# Guiding Principles

* Customer safety and regulatory compliance take precedence over automation.
* AI recommendations are advisory unless explicitly approved for autonomous execution.
* Critical incidents must always receive human review.
* Every escalation must generate an audit log and reasoning trace.
* Escalations should include sufficient context for rapid resolution.

---

# Escalation Levels

| Level | Severity      | Description                                                     |
| ----- | ------------- | --------------------------------------------------------------- |
| L0    | Informational | Routine inquiries handled automatically                         |
| L1    | Low           | Standard support issue requiring follow-up                      |
| L2    | Medium        | Business-impacting issue requiring specialist review            |
| L3    | High          | Customer success or engineering leadership involvement          |
| L4    | Critical      | Legal, security, compliance, executive, or production emergency |

---

# Escalation Decision Matrix

| Scenario                  | Level | Owner                      | AI Auto Reply    |
| ------------------------- | ----- | -------------------------- | ---------------- |
| General FAQ               | L0    | AI                         | ✅ Allowed        |
| Pricing Inquiry           | L0    | AI                         | ✅ Allowed        |
| Invoice Correction        | L1    | Customer Success           | ✅ Draft          |
| Refund Request            | L2    | Customer Success           | ✅ Draft Only     |
| Duplicate Charge          | L2    | Finance + Customer Success | ✅ Draft Only     |
| Feature Request           | L1    | Product Team               | ✅ Allowed        |
| Bug Report                | L2    | Engineering                | ✅ Draft          |
| SLA Complaint             | L3    | Support Leadership         | ❌ Human Approval |
| Enterprise Contract Issue | L3    | Account Manager            | ❌ Human Approval |
| VIP Churn Risk            | L3    | Customer Success           | ❌ Human Approval |
| Executive Complaint       | L4    | Executive Team             | ❌ Never          |
| GDPR Request              | L4    | Privacy & Legal            | ❌ Never          |
| HIPAA Compliance Request  | L3    | Compliance                 | ❌ Human Approval |
| Data Breach Report        | L4    | Security                   | ❌ Never          |
| Credential Exposure       | L4    | Security                   | ❌ Never          |
| Ransomware Mention        | L4    | Security Incident Team     | ❌ Never          |
| Legal Threat              | L4    | Legal Counsel              | ❌ Never          |
| Public Review Threat      | L3    | Customer Success Manager   | ❌ Human Approval |
| Payment Chargeback        | L3    | Finance                    | ❌ Human Approval |
| Spam / Marketing          | L0    | Spam Filter                | ❌ No Reply       |

---

# Mandatory Human Escalation

The following scenarios must **never** be handled autonomously:

* Legal notices
* GDPR requests
* HIPAA disputes
* Security incidents
* Ransomware
* Data breaches
* Executive complaints
* Regulatory investigations
* Contract disputes
* Public litigation threats

The AI may generate:

* internal summary
* reasoning trace
* suggested reply
* execution plan

Final communication must be approved by a human.

---

# AI Escalation Workflow

```text
Incoming Email
        │
        ▼
Rule Engine
        │
        ▼
Spam Check
        │
 ┌──────┴──────┐
 │             │
 ▼             ▼
Spam        Continue
 │             │
 ▼             ▼
Stop      Retrieve Context
                │
                ▼
        CRM Profile
                │
                ▼
        Thread History
                │
                ▼
        Policy Retrieval
                │
                ▼
         AI Analysis
                │
                ▼
     Confidence Evaluation
                │
     ┌──────────┴──────────┐
     │                     │
     ▼                     ▼
 Safe                Critical / Low Confidence
     │                     │
     ▼                     ▼
Auto Draft         Human Escalation
```

---

# Confidence Thresholds

| Confidence | Action                          |
| ---------- | ------------------------------- |
| 95–100%    | Auto draft permitted            |
| 85–94%     | Draft with approval recommended |
| 70–84%     | Human review required           |
| Below 70%  | Escalate immediately            |

Confidence should never override legal or security policies.

---

# Dry Run Mode

The agent operates in Dry Run mode by default.

In Dry Run mode:

* no emails are sent
* no refunds are approved
* no customer records are modified
* recommendations are advisory only

Actions generated include:

* recommended owner
* priority
* execution plan
* suggested reply

---

# Tool Usage Rules

Maximum recommended tool invocations per analysis: **6**

Preferred sequence:

1. Retrieve thread history
2. Retrieve CRM profile
3. Retrieve account status
4. Search knowledge base
5. Generate classification
6. Generate reply and execution plan

Avoid redundant tool calls.

---

# VIP Customer Handling

VIP customers require elevated handling.

Indicators include:

* high ARR
* enterprise contract
* strategic account
* executive sponsor
* renewal within 90 days

Escalate to:

* Customer Success Manager
* Account Executive
* Account Manager

Do not auto-close VIP cases.

---

# Churn Risk Handling

Escalate when:

* churn risk > 80%
* three consecutive negative interactions
* refund request + cancellation intent
* competitor mention
* repeated SLA complaints
* executive dissatisfaction

Recommend retention strategy before refund where appropriate.

---

# Security Incidents

Immediately escalate:

* credential leaks
* suspicious login
* ransomware
* phishing
* API key exposure
* webhook replay attacks
* data exfiltration

Do not disclose investigation details to customers.

Generate acknowledgement only.

---

# Compliance Requests

Automatically escalate:

* GDPR Article 17
* GDPR Article 20
* HIPAA BAA
* DPA requests
* SOC2 evidence requests
* audit requests
* legal holds

Require Privacy or Legal review.

---

# Spam Handling

Spam indicators include:

* promotional bulk mail
* unsolicited marketing
* phishing
* malicious attachments
* suspicious domains
* repetitive advertisements

Spam should:

* be categorized as Spam
* generate no customer reply
* be excluded from analytics
* create an audit entry
* terminate processing

---

# Public Reputation Risk

Escalate if customer threatens:

* LinkedIn posts
* X/Twitter complaints
* Reddit exposure
* media outreach
* App Store reviews
* Gartner reviews

Customer Success should coordinate response.

AI should draft acknowledgement only.

---

# Agent Reasoning Requirements

Every escalation should persist:

* Thought
* Action
* Observation
* Decision
* Confidence
* Retrieved policies
* Tool calls
* Final recommendation

This reasoning must be visible in the Agent Inspector panel.

---

# Example Scenario

Customer:

> "Refund me today or my lawyer will contact you and I will post this publicly."

Recommended actions:

* Retrieve Refund Policy
* Retrieve Escalation Matrix
* Flag Legal
* Flag Customer Success
* Draft acknowledgement only
* Disable auto reply
* Require human approval

---

# Retrieval Keywords

escalation

legal

GDPR

HIPAA

security

ransomware

VIP

chargeback

refund

executive complaint

public review

lawsuit

compliance

privacy

critical incident

human approval

manual review

dry run

agent reasoning

tool execution

confidence threshold

spam

security incident

escalation matrix
