# RAG Evaluation Report

## Evaluation Overview

- **Number of questions**: 50
- **Date/time**: 2026-09-24 13:07:00
- **Strategy**: HYBRID

## Overall Metrics

| Metric | HYBRID |
|---|---|
| Hit@1 | 92.31% | 
| Hit@3 | 97.44% | 
| Hit@5 | 100.00% | 
| Hit@10 | 100.00% | 
| Recall@5 | 99.15% | 
| Recall@10 | 99.15% | 
| MRR | 0.96 | 
| Reference Answer Similarity | 81.36% | 
| Citation Support Rate | 96.79% | 
| Refusal Correctness | 100.00% | 

## Question Results

### Q001

**Question**:
How do I authenticate an API request?

**Question type**:
None

**Expected answer**:
API requests require an Authorization header containing a valid API token.

**Generated answer**:
To authenticate an API request, you need to create an API token with the required scope and include it as a Bearer token in the Authorization header of your request. The format for this header is:

```
Authorization: Bearer <API_TOKEN>
```

It is important to treat tokens as secrets and not expose them in client-side code [API-001-chunk-000][ONB-004-chunk-000].

**Expected chunks**:
['API-001']

**Retrieved chunks**:
['API-001', 'ONB-004', 'REL-001', 'ONB-006', 'API-010', 'API-008', 'TRB-003', 'TRB-001', 'TRB-002', 'API-004']

**Retrieval metrics**:
Hit@1: 1, Hit@5: 1, Recall@5: 1.00, MRR: 1.00

**Reference answer similarity**: 83.51%

**Citation support rate**: 100.00%

**Refusal correctness**: N/A


---

### Q002

**Question**:
What does an HTTP 401 error indicate?

**Question type**:
None

**Expected answer**:
An HTTP 401 error indicates an authentication failure, commonly caused by a missing, expired, or invalid credential.

**Generated answer**:
An HTTP 401 error indicates an authentication failure. This usually means that the request is missing a valid authentication credential, which can happen due to a missing Authorization header, an expired token, or an invalid token [API-008-chunk-000][TRB-001-chunk-001].

**Expected chunks**:
['API-008', 'TRB-001']

**Retrieved chunks**:
['API-008', 'TRB-001', 'TRB-001', 'TRB-002', 'TRB-003', 'FAQ-008', 'API-006', 'TRB-005', 'TRB-003', 'TRB-004']

**Retrieval metrics**:
Hit@1: 1, Hit@5: 1, Recall@5: 1.00, MRR: 1.00

**Reference answer similarity**: 94.32%

**Citation support rate**: 50.00%

**Refusal correctness**: N/A

❌ Unsupported citation

---

### Q003

**Question**:
What is the difference between HTTP 401 and 403 errors?

**Question type**:
None

**Expected answer**:
A 401 error indicates an authentication failure, while a 403 error indicates that the request is authenticated but does not have permission to access the requested resource.

**Generated answer**:
The difference between HTTP 401 and 403 errors is as follows:

- A 401 error indicates that there is a failure in authentication, which usually means the request is missing a valid authentication credential. Common causes include a missing Authorization header, an expired token, or an invalid token [TRB-001-chunk-001].

- A 403 error signifies an authorization failure. This occurs when the server understands the request, the client is authenticated, but does not have permission to perform the requested operation. For example, an API token can be valid but still receive a 403 response if it does not possess the required scope [API-002-chunk-000].

In summary, 401 is about authentication issues, while 403 is about authorization issues.

**Expected chunks**:
['API-008', 'TRB-002']

**Retrieved chunks**:
['API-008', 'TRB-002', 'TRB-001', 'API-002', 'TRB-001', 'TRB-003', 'FAQ-008', 'API-006', 'TRB-005', 'API-005']

**Retrieval metrics**:
Hit@1: 1, Hit@5: 1, Recall@5: 1.00, MRR: 1.00

**Reference answer similarity**: 91.68%

**Citation support rate**: 100.00%

**Refusal correctness**: N/A


---

### Q004

**Question**:
What does an HTTP 429 error mean?

**Question type**:
None

**Expected answer**:
An HTTP 429 error indicates that the API rate limit has been exceeded.

**Generated answer**:
An HTTP 429 error means that a client has exceeded the applicable API rate limit. When this happens, the service returns this error code, and clients are advised to retry after the documented delay, especially if a "Retry-After" header is provided [API-008-chunk-000][API-006-chunk-000][TRB-003-chunk-001].

**Expected chunks**:
['TRB-003', 'API-006', 'REL-001']

**Retrieved chunks**:
['TRB-003', 'API-008', 'FAQ-008', 'API-006', 'TRB-002', 'TRB-001', 'TRB-001', 'TRB-007', 'TRB-003', 'TRB-005']

**Retrieval metrics**:
Hit@1: 1, Hit@5: 1, Recall@5: 0.67, MRR: 1.00

**Reference answer similarity**: 91.46%

**Citation support rate**: 100.00%

**Refusal correctness**: N/A


---

### Q005

**Question**:
How do scoped API tokens work?

**Question type**:
None

**Expected answer**:
Scoped API tokens restrict access by allowing specific permissions or scopes instead of granting unrestricted access.

**Generated answer**:
Scoped API tokens are designed to limit the operations that can be performed with them. Even if a valid token is issued, it must have the required scope for specific operations; otherwise, the API will return an HTTP 403 response if the token is used for unauthorized actions [API-002-chunk-000]. To use a scoped API token, it must be created with the necessary scope, and then included as a Bearer token in the Authorization header when making an API request [ONB-004-chunk-000]. 

It is also important to note that existing unscoped tokens are still supported alongside the new scoped tokens [REL-001-chunk-000]. 

By securely handling these tokens and following best practices, you can ensure proper usage and maintain security [API-001-chunk-000][POL-001-chunk-000]. 

WHAT I COULD NOT VERIFY:
- Specific examples of scopes that can be assigned to tokens or detailed information about potential actions limited by scopes.

**Expected chunks**:
['API-002', 'REL-001']

**Retrieved chunks**:
['API-002', 'ONB-004', 'REL-001', 'API-004', 'REL-004', 'POL-001', 'API-001', 'ONB-006', 'TRB-002', 'API-003']

**Retrieval metrics**:
Hit@1: 1, Hit@5: 1, Recall@5: 1.00, MRR: 1.00

**Reference answer similarity**: 79.39%

**Citation support rate**: 100.00%

**Refusal correctness**: N/A


---

### Q006

**Question**:
How does pagination work in API v2?

**Question type**:
None

**Expected answer**:
API v2 uses cursor-based pagination rather than the older page-number pagination approach.

**Generated answer**:
Pagination in API v2 used page-number pagination. However, it is important to note that this documentation is historical and not suitable for current API behavior, as the API has transitioned to version 3 and introduced cursor-based pagination for list endpoints instead. In version 3, clients should follow the pagination cursor returned by the API rather than assuming a fixed page size [REL-004-chunk-000], [API-007-chunk-000]. 

WHAT I COULD NOT VERIFY:
- Specifics on how page-number pagination functioned in detail (e.g., parameters, response format).

**Expected chunks**:
['REL-004', 'API-007']

**Retrieved chunks**:
['REL-004', 'REL-003', 'API-007', 'API-010', 'ONB-004', 'API-004', 'API-003', 'API-001', 'FAQ-008', 'TRB-003']

**Retrieval metrics**:
Hit@1: 1, Hit@5: 1, Recall@5: 1.00, MRR: 1.00

**Reference answer similarity**: 86.50%

**Citation support rate**: 100.00%

**Refusal correctness**: N/A


---

### Q007

**Question**:
What is FlowDesk?

**Question type**:
None

**Expected answer**:
FlowDesk is a customer-support workflow platform used to manage tickets, teams, automations, and customer conversations

**Generated answer**:
FlowDesk is a customer-support workflow platform used to manage tickets, teams, automations, and customer conversations [FAQ-001-chunk-000]. 

WHAT I COULD NOT VERIFY:
- None.

**Expected chunks**:
['FAQ-001']

**Retrieved chunks**:
['FAQ-001', 'FAQ-003', 'FAQ-006', 'TRB-004', 'FAQ-008', 'API-001', 'API-009', 'TRB-008', 'TRB-003', 'TRB-007']

**Retrieval metrics**:
Hit@1: 1, Hit@5: 1, Recall@5: 1.00, MRR: 1.00

**Reference answer similarity**: 99.58%

**Citation support rate**: 100.00%

**Refusal correctness**: N/A


---

### Q008

**Question**:
Can users disable security alerts?

**Question type**:
None

**Expected answer**:
Security alerts are configurable according to the workspace security settings and applicable policy.

**Generated answer**:
No, users cannot disable security alerts. Security-related alerts are mandatory notifications for selected security events and cannot be disabled by individual users [POL-004-chunk-000].

**Expected chunks**:
['FAQ-005', 'POL-004']

**Retrieved chunks**:
['POL-004', 'FAQ-005', 'FAQ-005', 'POL-006', 'POL-001', 'ONB-006', 'TRB-005', 'REL-008', 'API-004', 'FAQ-002']

**Retrieval metrics**:
Hit@1: 1, Hit@5: 1, Recall@5: 1.00, MRR: 1.00

**Reference answer similarity**: 63.12%

**Citation support rate**: 100.00%

**Refusal correctness**: N/A


---

### Q009

**Question**:
What should I do if a webhook endpoint is unavailable?

**Question type**:
None

**Expected answer**:
Check the webhook endpoint configuration and troubleshoot the failed delivery using the documented webhook troubleshooting steps.

**Generated answer**:
If a webhook endpoint is unavailable, you should verify the endpoint URL, check the TLS configuration, review the response status, and ensure network accessibility. Additionally, note that FlowDesk retries some failed deliveries, so your endpoint may receive a retry attempt after a failure [TRB-004-chunk-001].

**Expected chunks**:
['TRB-004', 'API-005']

**Retrieved chunks**:
['API-005', 'ONB-005', 'FAQ-006', 'REL-002', 'TRB-004', 'TRB-004', 'TRB-010', 'TRB-004', 'API-006', 'FAQ-006']

**Retrieval metrics**:
Hit@1: 1, Hit@5: 1, Recall@5: 1.00, MRR: 1.00

**Reference answer similarity**: 82.42%

**Citation support rate**: 100.00%

**Refusal correctness**: N/A


---

### Q010

**Question**:
What should I do before making my first API request?

**Question type**:
None

**Expected answer**:
Before making the first API request, obtain the required API credentials and authenticate the request correctly.

**Generated answer**:
Before making your first API request, you should create an API token with the required scope. This token needs to be included as a Bearer token in the Authorization header when you call an endpoint available to that token. The format for including the Bearer token is as follows: `Authorization: Bearer <API_TOKEN>` [ONB-004-chunk-000][API-001-chunk-000]. 

Additionally, ensure that you treat tokens as secrets and do not expose them in client-side code [API-001-chunk-000][ONB-006-chunk-000].

**Expected chunks**:
['ONB-004', 'API-001']

**Retrieved chunks**:
['ONB-004', 'API-010', 'API-006', 'API-001', 'FAQ-008', 'TRB-003', 'TRB-001', 'FAQ-008', 'API-008', 'ONB-006']

**Retrieval metrics**:
Hit@1: 1, Hit@5: 1, Recall@5: 1.00, MRR: 1.00

**Reference answer similarity**: 76.88%

**Citation support rate**: 100.00%

**Refusal correctness**: N/A


---

### Q011

**Question**:
Can I share my API token with another user?

**Question type**:
None

**Expected answer**:
API tokens should not be shared with other users; users should use their own appropriate credentials.

**Generated answer**:
No, you should not share your API token with another user. API tokens are credentials that must be protected, and users must not share tokens between people [POL-001-chunk-000].

**Expected chunks**:
['POL-001', 'ONB-006']

**Retrieved chunks**:
['POL-001', 'ONB-006', 'ONB-004', 'API-002', 'API-004', 'REL-001', 'API-001', 'REL-004', 'TRB-002', 'FAQ-001']

**Retrieval metrics**:
Hit@1: 1, Hit@5: 1, Recall@5: 1.00, MRR: 1.00

**Reference answer similarity**: 87.18%

**Citation support rate**: 100.00%

**Refusal correctness**: N/A


---

### Q012

**Question**:
What is the maximum number of API requests a workspace can make per second?

**Question type**:
None

**Expected answer**:


**Generated answer**:
NO_ANSWER_FOUND

WHAT I COULD NOT VERIFY:
- The maximum number of API requests a workspace can make per second.

**Expected chunks**:
[]

**Retrieved chunks**:
['API-006', 'FAQ-008', 'API-008', 'API-004', 'TRB-003', 'FAQ-008', 'TRB-003', 'TRB-008', 'FAQ-001', 'TRB-001']

**Retrieval metrics**:
Hit@1: 0, Hit@5: 0, Recall@5: 0.00, MRR: 0.00

**Reference answer similarity**: 0.00%

**Citation support rate**: 0.00%

**Refusal correctness**: 1


---

### Q013

**Question**:
How can I invite a user to the workspace?

**Question type**:
None

**Expected answer**:
Users can be invited to the workspace through the documented workspace invitation process.

**Generated answer**:
To invite a user to the workspace, Admins and Owners can invite users by email and select a role during the invitation. If the invitation expires, it must be resent [ONB-002-chunk-000]. 

WHAT I COULD NOT VERIFY:
- None.

**Expected chunks**:
['ONB-002']

**Retrieved chunks**:
['ONB-002', 'FAQ-001', 'TRB-005', 'API-004', 'POL-003', 'ONB-001', 'FAQ-002', 'FAQ-003', 'TRB-002', 'TRB-008']

**Retrieval metrics**:
Hit@1: 1, Hit@5: 1, Recall@5: 1.00, MRR: 1.00

**Reference answer similarity**: 77.36%

**Citation support rate**: 100.00%

**Refusal correctness**: N/A


---

### Q014

**Question**:
What roles are available in the workspace?

**Question type**:
None

**Expected answer**:
The workspace provides different roles with different levels of permissions, including the documented Agent and other workspace roles.

**Generated answer**:
FlowDesk provides the following roles in the workspace: Owner, Admin, Agent, and Viewer [FAQ-003-chunk-000]. 

WHAT I COULD NOT VERIFY:
- Information on the specific permissions associated with each role.

**Expected chunks**:
['FAQ-003']

**Retrieved chunks**:
['FAQ-003', 'ONB-001', 'POL-003', 'API-004', 'FAQ-001', 'TRB-005', 'ONB-006', 'TRB-008', 'FAQ-003', 'FAQ-002']

**Retrieval metrics**:
Hit@1: 1, Hit@5: 1, Recall@5: 1.00, MRR: 1.00

**Reference answer similarity**: 74.30%

**Citation support rate**: 100.00%

**Refusal correctness**: N/A


---

### Q015

**Question**:
Can a Viewer download every field from an export?

**Question type**:
None

**Expected answer**:
Viewer access does not necessarily provide access to every export field; export availability depends on the documented permissions and restrictions.

**Generated answer**:
No, a Viewer cannot download every field from an export. Exportable fields depend on the object type and the user's permissions, and since Viewers have limited permissions, they may not have access to all fields [FAQ-007-chunk-001]. 

WHAT I COULD NOT VERIFY:
- Specific permissions associated with the Viewer role that limit access to certain fields during export.

**Expected chunks**:
['FAQ-007', 'TRB-010']

**Retrieved chunks**:
['FAQ-007', 'REL-007', 'FAQ-007', 'TRB-010', 'TRB-007', 'FAQ-002', 'TRB-007', 'FAQ-003', 'REL-002', 'API-003']

**Retrieval metrics**:
Hit@1: 1, Hit@5: 1, Recall@5: 1.00, MRR: 1.00

**Reference answer similarity**: 73.99%

**Citation support rate**: 100.00%

**Refusal correctness**: N/A


---

### Q016

**Question**:
Which header should I use to authenticate an API request?

**Question type**:
None

**Expected answer**:
Use the Authorization header with a valid API token to authenticate the API request.

**Generated answer**:
To authenticate an API request, you should use a Bearer token in the Authorization header. The format should be as follows:

Authorization: Bearer <API_TOKEN> 

Tokens should be treated as secrets and must not be exposed in client-side code [API-001-chunk-000].

**Expected chunks**:
['API-001']

**Retrieved chunks**:
['API-001', 'ONB-004', 'API-006', 'REL-001', 'ONB-006', 'API-010', 'TRB-003', 'TRB-002', 'API-008', 'TRB-001']

**Retrieval metrics**:
Hit@1: 1, Hit@5: 1, Recall@5: 1.00, MRR: 1.00

**Reference answer similarity**: 87.98%

**Citation support rate**: 100.00%

**Refusal correctness**: N/A


---

### Q017

**Question**:
What are common causes of an HTTP 401 error?

**Question type**:
None

**Expected answer**:
Common causes include a missing Authorization header, an expired token, or an invalid token.

**Generated answer**:
Common causes of an HTTP 401 error include a missing Authorization header, an expired token, or an invalid token, which indicates that the request is missing a valid authentication credential [TRB-001-chunk-001].

**Expected chunks**:
['TRB-001']

**Retrieved chunks**:
['TRB-001', 'API-008', 'TRB-001', 'TRB-002', 'TRB-003', 'TRB-003', 'FAQ-008', 'API-006', 'TRB-007', 'TRB-004']

**Retrieval metrics**:
Hit@1: 1, Hit@5: 1, Recall@5: 1.00, MRR: 1.00

**Reference answer similarity**: 90.20%

**Citation support rate**: 100.00%

**Refusal correctness**: N/A


---

### Q018

**Question**:
What are common causes of an HTTP 403 error?

**Question type**:
None

**Expected answer**:
A 403 error occurs when the request is authenticated but the user or token does not have sufficient permission to access the resource.

**Generated answer**:
A common cause of an HTTP 403 error is an authorization failure, which can occur even when authentication succeeds. This means the request has been received and understood, but the server is refusing to fulfill it due to insufficient permissions for the authenticated user. [API-008-chunk-000] [TRB-002-chunk-000]

WHAT I COULD NOT VERIFY:
- Specific scenarios or examples that lead to authorization failures resulting in a 403 error.

**Expected chunks**:
['TRB-002']

**Retrieved chunks**:
['API-008', 'TRB-002', 'TRB-001', 'TRB-001', 'TRB-003', 'TRB-003', 'FAQ-008', 'API-006', 'TRB-007', 'TRB-004']

**Retrieval metrics**:
Hit@1: 0, Hit@5: 1, Recall@5: 1.00, MRR: 0.50

**Reference answer similarity**: 85.69%

**Citation support rate**: 100.00%

**Refusal correctness**: N/A


---

### Q019

**Question**:
What does HTTP 429 mean for API requests?

**Question type**:
None

**Expected answer**:
HTTP 429 means the API rate limit has been exceeded.

**Generated answer**:
HTTP 429 indicates that the API requests are being rate limited. Specifically, when a client exceeds the allowable rate limits on an endpoint or workspace, the service responds with this status code. Clients are advised to honor the "Retry-After" header when it is provided by the API to determine how long they should wait before making another request [API-006-chunk-000][FAQ-008-chunk-001].

**Expected chunks**:
['TRB-003']

**Retrieved chunks**:
['API-006', 'TRB-003', 'API-008', 'FAQ-008', 'TRB-001', 'ONB-004', 'API-002', 'API-001', 'TRB-002', 'API-005']

**Retrieval metrics**:
Hit@1: 0, Hit@5: 1, Recall@5: 1.00, MRR: 0.50

**Reference answer similarity**: 85.46%

**Citation support rate**: 100.00%

**Refusal correctness**: N/A


---

### Q020

**Question**:
How does API rate limiting work?

**Question type**:
None

**Expected answer**:
API rate limiting restricts the number or frequency of requests allowed within a specified period.

**Generated answer**:
API rate limiting works by applying limits to the number of requests that can be made to certain endpoints or within specific workspaces. If a client exceeds these limits, the service will return HTTP status code 429 to indicate that the rate limit has been exceeded. Clients should then respect the "Retry-After" header when provided, which indicates when they can attempt to send a request again without hitting the limit [API-006-chunk-000], [FAQ-008-chunk-001], [REL-001-chunk-001].

**Expected chunks**:
['API-006', 'TRB-003']

**Retrieved chunks**:
['API-006', 'FAQ-008', 'TRB-003', 'REL-001', 'API-008', 'FAQ-008', 'API-002', 'API-003', 'API-010', 'API-004']

**Retrieval metrics**:
Hit@1: 1, Hit@5: 1, Recall@5: 1.00, MRR: 1.00

**Reference answer similarity**: 76.28%

**Citation support rate**: 100.00%

**Refusal correctness**: N/A


---

### Q021

**Question**:
What permissions can be assigned to a scoped API token?

**Question type**:
None

**Expected answer**:
A scoped API token can be restricted to specific permissions or scopes defined by the API.

**Generated answer**:
Scoped API tokens can be assigned with scopes that limit the operations they can perform. A valid token without the required scope can receive an HTTP 403 error if it tries to access unauthorized resources [API-002-chunk-000]. 

WHAT I COULD NOT VERIFY:
- Specific permissions that can be assigned to a scoped API token.

**Expected chunks**:
['API-002']

**Retrieved chunks**:
['API-002', 'API-004', 'ONB-004', 'REL-001', 'API-001', 'TRB-002', 'REL-004', 'POL-001', 'ONB-006', 'TRB-008']

**Retrieval metrics**:
Hit@1: 1, Hit@5: 1, Recall@5: 1.00, MRR: 1.00

**Reference answer similarity**: 83.74%

**Citation support rate**: 100.00%

**Refusal correctness**: N/A


---

### Q022

**Question**:
Are unscoped API tokens still supported?

**Question type**:
None

**Expected answer**:
The release documentation describes the current status of unscoped API tokens and the changes related to scoped tokens.

**Generated answer**:
Yes, unscoped API tokens are still supported. Existing unscoped tokens remain supported despite the introduction of scoped API tokens [REL-001-chunk-000].

**Expected chunks**:
['REL-001']

**Retrieved chunks**:
['REL-001', 'API-002', 'REL-004', 'POL-001', 'ONB-004', 'API-001', 'API-004', 'TRB-001', 'TRB-002', 'API-009']

**Retrieval metrics**:
Hit@1: 1, Hit@5: 1, Recall@5: 1.00, MRR: 1.00

**Reference answer similarity**: 76.72%

**Citation support rate**: 100.00%

**Refusal correctness**: N/A


---

### Q023

**Question**:
How does pagination work for the current list API endpoint?

**Question type**:
None

**Expected answer**:
The current list API endpoint uses the documented pagination mechanism for retrieving results across multiple pages.

**Generated answer**:
Pagination for the current list API endpoints uses cursor-based pagination. Clients are advised to follow the pagination cursor returned by the API instead of assuming a fixed page size [API-007-chunk-000][REL-003-chunk-000]. 

WHAT I COULD NOT VERIFY:
- Specific details on how to use the pagination cursor.

**Expected chunks**:
['API-007']

**Retrieved chunks**:
['API-007', 'REL-003', 'REL-004', 'ONB-004', 'API-010', 'API-005', 'API-006', 'TRB-004', 'API-003', 'REL-002']

**Retrieval metrics**:
Hit@1: 1, Hit@5: 1, Recall@5: 1.00, MRR: 1.00

**Reference answer similarity**: 84.08%

**Citation support rate**: 100.00%

**Refusal correctness**: N/A


---

### Q024

**Question**:
What pagination method does API v2 use?

**Question type**:
None

**Expected answer**:
API v2 uses cursor-based pagination.

**Generated answer**:
API v2 uses page-number pagination [REL-004-chunk-000].

**Expected chunks**:
['REL-004']

**Retrieved chunks**:
['REL-004', 'REL-003', 'API-007', 'API-003', 'API-004', 'API-010', 'ONB-006', 'REL-001', 'FAQ-008', 'FAQ-008']

**Retrieval metrics**:
Hit@1: 1, Hit@5: 1, Recall@5: 1.00, MRR: 1.00

**Reference answer similarity**: 87.20%

**Citation support rate**: 100.00%

**Refusal correctness**: N/A


---

### Q025

**Question**:
What is the current API version?

**Question type**:
None

**Expected answer**:
The documentation identifies the current API version and its corresponding integration guidance.

**Generated answer**:
The current API version is 3.2 [API-010-chunk-000]. 

WHAT I COULD NOT VERIFY:
- There is no missing information.

**Expected chunks**:
['API-010']

**Retrieved chunks**:
['API-010', 'REL-003', 'REL-004', 'REL-001', 'API-003', 'API-004', 'ONB-004', 'TRB-002', 'API-008', 'FAQ-008']

**Retrieval metrics**:
Hit@1: 1, Hit@5: 1, Recall@5: 1.00, MRR: 1.00

**Reference answer similarity**: 77.42%

**Citation support rate**: 100.00%

**Refusal correctness**: N/A


---

### Q026

**Question**:
How quickly are webhook events delivered?

**Question type**:
None

**Expected answer**:
Webhook delivery timing is described in the webhook documentation, but delivery should be understood according to the documented timing expectations rather than as an absolute guarantee.

**Generated answer**:
Webhook events are normally delivered within seconds, but delivery timing is not guaranteed [FAQ-006-chunk-001]. Additionally, it is noted that webhook delivery is not guaranteed to be instantaneous [TRB-004-chunk-002].

**Expected chunks**:
['FAQ-006']

**Retrieved chunks**:
['FAQ-006', 'TRB-004', 'API-005', 'ONB-005', 'REL-002', 'FAQ-006', 'TRB-004', 'FAQ-008', 'POL-004', 'TRB-003']

**Retrieval metrics**:
Hit@1: 1, Hit@5: 1, Recall@5: 1.00, MRR: 1.00

**Reference answer similarity**: 78.02%

**Citation support rate**: 100.00%

**Refusal correctness**: N/A


---

### Q027

**Question**:
How can I troubleshoot a failed webhook?

**Question type**:
None

**Expected answer**:
Check the webhook endpoint and delivery configuration, then follow the documented troubleshooting steps for failed webhook deliveries.

**Generated answer**:
To troubleshoot a failed webhook, you should consider the following steps:

1. **Check If the Webhook Is Configured Correctly**: Ensure that you have provided a reachable HTTPS endpoint when setting up the webhook subscription [ONB-005-chunk-000].

2. **Inspect the Webhook Delivery Log**: Utilize the webhook delivery log to verify if there are any reported issues or response statuses from the destination endpoint [REL-002-chunk-001].

3. **Review Delivery Policies**: Be aware that failed deliveries may be retried according to the delivery policy, so even a failure might not be the end of the notifications [API-005-chunk-000].

4. **Look for Symptoms of Incorrect Setup**: Ensure that the webhook is, in fact, configured and check if the endpoint is reachable [TRB-004-chunk-000].

By following these steps, you can systematically identify and resolve issues related to failed webhooks. 

WHAT I COULD NOT VERIFY:
- Specific methods for diagnosing the reason a webhook failed (e.g., timeouts, response errors).
- Detailed steps on how to fix common issues related to the webhook not reaching the destination.

**Expected chunks**:
['TRB-004', 'API-005']

**Retrieved chunks**:
['TRB-004', 'API-005', 'TRB-002', 'ONB-005', 'TRB-009', 'FAQ-006', 'TRB-004', 'TRB-003', 'REL-002', 'TRB-005']

**Retrieval metrics**:
Hit@1: 1, Hit@5: 1, Recall@5: 1.00, MRR: 1.00

**Reference answer similarity**: 89.34%

**Citation support rate**: 100.00%

**Refusal correctness**: N/A


---

### Q028

**Question**:
Is there a guaranteed delivery time for webhooks?

**Question type**:
None

**Expected answer**:
The documentation describes webhook delivery timing but does not necessarily provide an absolute delivery-time guarantee.

**Generated answer**:
Webhook delivery timing is not guaranteed, and while events are normally delivered within seconds, there is no guarantee of instantaneous delivery [FAQ-006-chunk-001][TRB-004-chunk-002].

**Expected chunks**:
['FAQ-006']

**Retrieved chunks**:
['FAQ-006', 'TRB-004', 'API-005', 'ONB-005', 'REL-002', 'FAQ-006', 'TRB-004', 'TRB-004', 'FAQ-008', 'TRB-010']

**Retrieval metrics**:
Hit@1: 1, Hit@5: 1, Recall@5: 1.00, MRR: 1.00

**Reference answer similarity**: 79.91%

**Citation support rate**: 100.00%

**Refusal correctness**: N/A


---

### Q029

**Question**:
What should I do if API search is slow?

**Question type**:
None

**Expected answer**:
Follow the documented troubleshooting guidance for slow search performance.

**Generated answer**:
If the API search is slow, consider narrowing your query to reduce the search scope. You can achieve this by using a ticket ID, an exact phrase, or a date filter, which can help improve search performance, especially if you are dealing with a large workspace or complex queries [TRB-009-chunk-000]. 

Additionally, ensure that you are not exceeding the rate limits set by the API, as exceeding these limits will result in error responses, specifically HTTP 429, which indicates that clients should retry after a specific delay [API-006-chunk-000].

WHAT I COULD NOT VERIFY:
- Suggestions for optimizing API search speed beyond narrowing queries.
- Specific performance metrics or recommendations for expected API response times.

**Expected chunks**:
['TRB-009']

**Retrieved chunks**:
['FAQ-008', 'API-010', 'API-006', 'TRB-009', 'TRB-003', 'TRB-002', 'API-008', 'FAQ-008', 'TRB-001', 'TRB-003']

**Retrieval metrics**:
Hit@1: 0, Hit@5: 1, Recall@5: 1.00, MRR: 0.25

**Reference answer similarity**: 74.56%

**Citation support rate**: 100.00%

**Refusal correctness**: N/A


---

### Q030

**Question**:
Can I search for tickets by ID?

**Question type**:
None

**Expected answer**:
The documentation describes how tickets can be searched using their identifiers.

**Generated answer**:
Yes. Enter the ticket ID in the global search field. [FAQ-004-chunk-000]

**Expected chunks**:
['FAQ-004']

**Retrieved chunks**:
['FAQ-004', 'API-003', 'TRB-009', 'FAQ-007', 'FAQ-001', 'FAQ-002', 'TRB-006', 'REL-002', 'POL-004', 'ONB-002']

**Retrieval metrics**:
Hit@1: 1, Hit@5: 1, Recall@5: 1.00, MRR: 1.00

**Reference answer similarity**: 75.27%

**Citation support rate**: 100.00%

**Refusal correctness**: N/A


---

### Q031

**Question**:
Who can invite users to the workspace?

**Question type**:
None

**Expected answer**:
The ability to invite users depends on the workspace role and permissions described in the onboarding documentation.

**Generated answer**:
Admins and Owners can invite users by email and select a role during the invitation process [ONB-002-chunk-000]. 

WHAT I COULD NOT VERIFY:
- No missing information.

**Expected chunks**:
['ONB-002']

**Retrieved chunks**:
['ONB-002', 'FAQ-001', 'TRB-005', 'POL-003', 'API-004', 'FAQ-002', 'FAQ-007', 'TRB-002', 'ONB-001', 'FAQ-003']

**Retrieval metrics**:
Hit@1: 1, Hit@5: 1, Recall@5: 1.00, MRR: 1.00

**Reference answer similarity**: 75.81%

**Citation support rate**: 100.00%

**Refusal correctness**: N/A


---

### Q032

**Question**:
What happens if a workspace invitation expires?

**Question type**:
None

**Expected answer**:
An expired workspace invitation must be handled according to the documented invitation process.

**Generated answer**:
If a workspace invitation expires, it must be resent by an administrator [TRB-006-chunk-001].

**Expected chunks**:
['ONB-002']

**Retrieved chunks**:
['ONB-002', 'TRB-006', 'API-006', 'TRB-005', 'TRB-001', 'TRB-008', 'POL-002', 'POL-003', 'TRB-006', 'TRB-002']

**Retrieval metrics**:
Hit@1: 1, Hit@5: 1, Recall@5: 1.00, MRR: 1.00

**Reference answer similarity**: 83.30%

**Citation support rate**: 100.00%

**Refusal correctness**: N/A


---

### Q033

**Question**:
What workspace roles are available?

**Question type**:
None

**Expected answer**:
The workspace provides multiple roles with different permissions.

**Generated answer**:
FlowDesk provides four workspace roles: Owner, Admin, Agent, and Viewer [FAQ-003-chunk-000]. 

WHAT I COULD NOT VERIFY:
- None.

**Expected chunks**:
['FAQ-003']

**Retrieved chunks**:
['FAQ-003', 'ONB-001', 'POL-003', 'FAQ-001', 'TRB-005', 'FAQ-003', 'TRB-008', 'REL-007', 'TRB-002', 'TRB-001']

**Retrieval metrics**:
Hit@1: 1, Hit@5: 1, Recall@5: 1.00, MRR: 1.00

**Reference answer similarity**: 74.94%

**Citation support rate**: 100.00%

**Refusal correctness**: N/A


---

### Q034

**Question**:
What permissions does the Agent role have?

**Question type**:
None

**Expected answer**:
The Agent role has the permissions described for that role in the workspace role and permissions documentation.

**Generated answer**:
The Agent role does not have the permission to change workspace settings, as this requires Admin or Owner permissions [POL-003-chunk-000]. Agents are intended to receive only the permissions necessary for support work, but the specific permissions granted to Agents are not detailed in the documentation [POL-003-chunk-000].

WHAT I COULD NOT VERIFY:
- The specific permissions assigned to the Agent role.

**Expected chunks**:
['FAQ-003', 'POL-003']

**Retrieved chunks**:
['FAQ-003', 'POL-003', 'FAQ-003', 'TRB-008', 'API-004', 'POL-005', 'ONB-006', 'TRB-002', 'FAQ-002', 'ONB-002']

**Retrieval metrics**:
Hit@1: 1, Hit@5: 1, Recall@5: 1.00, MRR: 1.00

**Reference answer similarity**: 77.99%

**Citation support rate**: 50.00%

**Refusal correctness**: N/A

❌ Unsupported citation

---

### Q035

**Question**:
What should I do if an API token is exposed?

**Question type**:
None

**Expected answer**:
An exposed API token should be handled according to the documented API credential security procedures.

**Generated answer**:
If an API token is exposed, you should treat it as a credential that must be protected. You must revoke the exposed token immediately and create a new one to prevent unauthorized access. Tokens should not be shared, committed to source control, or embedded in public client-side applications to mitigate the risk of exposure [API-001-chunk-000][POL-001-chunk-000]. 

WHAT I COULD NOT VERIFY:
- Steps on how to revoke an API token or create a new one.

**Expected chunks**:
['API-001', 'POL-001']

**Retrieved chunks**:
['API-001', 'POL-001', 'API-004', 'ONB-004', 'API-002', 'ONB-006', 'REL-001', 'REL-004', 'FAQ-008', 'API-010']

**Retrieval metrics**:
Hit@1: 1, Hit@5: 1, Recall@5: 1.00, MRR: 1.00

**Reference answer similarity**: 80.51%

**Citation support rate**: 100.00%

**Refusal correctness**: N/A


---

### Q036

**Question**:
Are security alerts optional?

**Question type**:
None

**Expected answer**:
The documentation describes whether security alerts can be configured or disabled according to the applicable workspace settings and policy.

**Generated answer**:
Security alerts are mandatory notifications for selected security events and cannot be disabled by individual users [POL-004-chunk-000].

**Expected chunks**:
['FAQ-005', 'POL-004']

**Retrieved chunks**:
['FAQ-005', 'POL-004', 'POL-006', 'REL-008', 'ONB-006', 'POL-001', 'ONB-003', 'TRB-005', 'FAQ-005', 'TRB-008']

**Retrieval metrics**:
Hit@1: 1, Hit@5: 1, Recall@5: 1.00, MRR: 1.00

**Reference answer similarity**: 63.41%

**Citation support rate**: 100.00%

**Refusal correctness**: N/A


---

### Q037

**Question**:
Should I use the API v2 documentation for a current integration?

**Question type**:
None

**Expected answer**:
The API v2 release and current API documentation provide the relevant guidance for integrations using API v2.

**Generated answer**:
No, you should not use the API v2 documentation for a current integration as it is considered historical and should not be used as the primary source for current API behavior. The current documentation describes version 3.2, which includes important updates such as scoped API tokens and cursor-based pagination for list endpoints [REL-004-chunk-000][API Versioning][REL-003-chunk-000][REL-001-chunk-000]. 

WHAT I COULD NOT VERIFY:
- Specific features or changes implemented in version 3.2 compared to version 2.

**Expected chunks**:
['REL-004', 'API-010']

**Retrieved chunks**:
['REL-004', 'API-010', 'POL-005', 'FAQ-008', 'API-004', 'REL-003', 'REL-001', 'API-003', 'ONB-004', 'API-001']

**Retrieval metrics**:
Hit@1: 1, Hit@5: 1, Recall@5: 1.00, MRR: 1.00

**Reference answer similarity**: 77.94%

**Citation support rate**: 75.00%

**Refusal correctness**: N/A

❌ Unsupported citation

---

### Q038

**Question**:
What authentication changes were introduced in Release 3.2?

**Question type**:
None

**Expected answer**:
Release 3.2 introduced the documented authentication changes, including changes related to API token handling.

**Generated answer**:
In Release 3.2, scoped API tokens are now supported for API authentication, while existing unscoped tokens remain supported as well [REL-001-chunk-000]. 

WHAT I COULD NOT VERIFY:
- There is no information about any additional changes made to authentication in Release 3.2 beyond the introduction of scoped API tokens.

**Expected chunks**:
['REL-001']

**Retrieved chunks**:
['REL-001', 'REL-003', 'API-010', 'REL-002', 'TRB-005', 'TRB-002', 'REL-005', 'ONB-006', 'REL-008', 'API-001']

**Retrieval metrics**:
Hit@1: 1, Hit@5: 1, Recall@5: 1.00, MRR: 1.00

**Reference answer similarity**: 81.95%

**Citation support rate**: 100.00%

**Refusal correctness**: N/A


---

### Q039

**Question**:
Why would an authenticated API request return HTTP 403?

**Question type**:
None

**Expected answer**:
A 403 response indicates that the request is authenticated but the credentials do not have the required permission to access the requested resource.

**Generated answer**:
An authenticated API request may return HTTP 403 for several reasons:

1. **Authorization Failure**: The HTTP 403 status code indicates that while authentication has succeeded, the user does not have the necessary permissions to access the requested resource or perform the desired action [API-008-chunk-000].

2. **Scoped API Tokens**: If an API token is issued with specific scopes, it may limit the operations that can be performed with that token. Even a valid token can return HTTP 403 if the required scope for the operation is not granted [API-002-chunk-000].

Therefore, if you receive a 403 response despite successful authentication, it likely stems from insufficient authorization or scope limitations associated with your API token.

**Expected chunks**:
['TRB-002', 'API-002']

**Retrieved chunks**:
['TRB-002', 'API-008', 'API-002', 'TRB-001', 'API-006', 'TRB-003', 'FAQ-008', 'API-001', 'ONB-004', 'TRB-001']

**Retrieval metrics**:
Hit@1: 1, Hit@5: 1, Recall@5: 1.00, MRR: 1.00

**Reference answer similarity**: 81.86%

**Citation support rate**: 100.00%

**Refusal correctness**: N/A


---

### Q040

**Question**:
How can I verify whether my token has the required permissions after receiving a 403?

**Question type**:
None

**Expected answer**:
Check the permissions or scopes assigned to the token and verify that they allow access to the requested resource.

**Generated answer**:
To verify whether your token has the required permissions after receiving a 403 status code, you should check the token scope and the user's workspace permissions [TRB-002-chunk-002]. A valid token might still receive a 403 error if it lacks the required scope [API-002-chunk-000].

**Expected chunks**:
['TRB-002', 'API-002']

**Retrieved chunks**:
['API-002', 'TRB-002', 'API-008', 'TRB-001', 'API-001', 'TRB-010', 'TRB-002', 'TRB-001', 'API-004', 'ONB-004']

**Retrieval metrics**:
Hit@1: 1, Hit@5: 1, Recall@5: 1.00, MRR: 1.00

**Reference answer similarity**: 81.63%

**Citation support rate**: 100.00%

**Refusal correctness**: N/A


---

### Q041

**Question**:
Who is the President of India?

**Question type**:
None

**Expected answer**:


**Generated answer**:
NO_ANSWER_FOUND

WHAT I COULD NOT VERIFY:
- The name of the current President of India.

**Expected chunks**:
[]

**Retrieved chunks**:
['FAQ-001', 'TRB-001', 'POL-004', 'TRB-002', 'TRB-006', 'TRB-002', 'POL-002', 'TRB-008', 'REL-001', 'ONB-006']

**Retrieval metrics**:
Hit@1: 0, Hit@5: 0, Recall@5: 0.00, MRR: 0.00

**Reference answer similarity**: 0.00%

**Citation support rate**: 0.00%

**Refusal correctness**: 1


---

### Q042

**Question**:
What is the capital of India?

**Question type**:
None

**Expected answer**:


**Generated answer**:
NO_ANSWER_FOUND

WHAT I COULD NOT VERIFY:
- The capital of India.

**Expected chunks**:
[]

**Retrieved chunks**:
['FAQ-001', 'TRB-001', 'POL-004', 'TRB-006', 'ONB-004', 'POL-001', 'FAQ-006', 'FAQ-003', 'ONB-001', 'ONB-006']

**Retrieval metrics**:
Hit@1: 0, Hit@5: 0, Recall@5: 0.00, MRR: 0.00

**Reference answer similarity**: 0.00%

**Citation support rate**: 0.00%

**Refusal correctness**: 1


---

### Q043

**Question**:
Who won the 2022 FIFA World Cup?

**Question type**:
None

**Expected answer**:


**Generated answer**:
NO_ANSWER_FOUND

WHAT I COULD NOT VERIFY:
- The winner of the 2022 FIFA World Cup.

**Expected chunks**:
[]

**Retrieved chunks**:
['FAQ-004', 'REL-002', 'TRB-002', 'TRB-002', 'TRB-005', 'REL-003', 'REL-002', 'TRB-003', 'TRB-001', 'REL-007']

**Retrieval metrics**:
Hit@1: 0, Hit@5: 0, Recall@5: 0.00, MRR: 0.00

**Reference answer similarity**: 0.00%

**Citation support rate**: 0.00%

**Refusal correctness**: 1


---

### Q044

**Question**:
What is the current population of India?

**Question type**:
None

**Expected answer**:


**Generated answer**:
NO_ANSWER_FOUND

WHAT I COULD NOT VERIFY:
- Current population of India.

**Expected chunks**:
[]

**Retrieved chunks**:
['FAQ-001', 'API-008', 'ONB-006', 'API-010', 'TRB-008', 'REL-004', 'REL-003', 'FAQ-003', 'FAQ-008', 'API-006']

**Retrieval metrics**:
Hit@1: 0, Hit@5: 0, Recall@5: 0.00, MRR: 0.00

**Reference answer similarity**: 0.00%

**Citation support rate**: 0.00%

**Refusal correctness**: 1


---

### Q045

**Question**:
How do Python list comprehensions work?

**Question type**:
None

**Expected answer**:


**Generated answer**:
NO_ANSWER_FOUND

WHAT I COULD NOT VERIFY:
- Information about Python list comprehensions.

**Expected chunks**:
[]

**Retrieved chunks**:
['REL-003', 'API-007', 'TRB-009', 'TRB-007', 'API-003', 'API-004', 'REL-002', 'API-009', 'API-002', 'API-001']

**Retrieval metrics**:
Hit@1: 0, Hit@5: 0, Recall@5: 0.00, MRR: 0.00

**Reference answer similarity**: 0.00%

**Citation support rate**: 0.00%

**Refusal correctness**: 1


---

### Q046

**Question**:
What is the latest version of Python?

**Question type**:
None

**Expected answer**:


**Generated answer**:
NO_ANSWER_FOUND

WHAT I COULD NOT VERIFY:
- The latest version of Python.

**Expected chunks**:
[]

**Retrieved chunks**:
['API-010', 'REL-003', 'REL-001', 'REL-002', 'FAQ-007', 'REL-004', 'FAQ-001', 'REL-007', 'FAQ-006', 'FAQ-003']

**Retrieval metrics**:
Hit@1: 0, Hit@5: 0, Recall@5: 0.00, MRR: 0.00

**Reference answer similarity**: 0.00%

**Citation support rate**: 0.00%

**Refusal correctness**: 1


---

### Q047

**Question**:
What is a Docker container?

**Question type**:
None

**Expected answer**:


**Generated answer**:
NO_ANSWER_FOUND

WHAT I COULD NOT VERIFY:
- Definition and details about what a Docker container is.

**Expected chunks**:
[]

**Retrieved chunks**:
['FAQ-001', 'FAQ-006', 'TRB-001', 'POL-002', 'TRB-008', 'TRB-001', 'TRB-004', 'FAQ-007', 'ONB-001', 'TRB-010']

**Retrieval metrics**:
Hit@1: 0, Hit@5: 0, Recall@5: 0.00, MRR: 0.00

**Reference answer similarity**: 0.00%

**Citation support rate**: 0.00%

**Refusal correctness**: 1


---

### Q048

**Question**:
What is the weather in Kerala today?

**Question type**:
None

**Expected answer**:


**Generated answer**:
NO_ANSWER_FOUND

WHAT I COULD NOT VERIFY:
- Today's weather in Kerala.

**Expected chunks**:
[]

**Retrieved chunks**:
['FAQ-001', 'TRB-003', 'ONB-004', 'TRB-004', 'TRB-003', 'POL-006', 'FAQ-005', 'REL-003', 'FAQ-008', 'API-001']

**Retrieval metrics**:
Hit@1: 0, Hit@5: 0, Recall@5: 0.00, MRR: 0.00

**Reference answer similarity**: 0.00%

**Citation support rate**: 0.00%

**Refusal correctness**: 1


---

### Q049

**Question**:
Who is the CEO of Google?

**Question type**:
None

**Expected answer**:


**Generated answer**:
NO_ANSWER_FOUND

WHAT I COULD NOT VERIFY:
- The name of the current CEO of Google.

**Expected chunks**:
[]

**Retrieved chunks**:
['REL-002', 'FAQ-001', 'TRB-004', 'FAQ-003', 'TRB-003', 'TRB-006', 'TRB-008', 'TRB-002', 'TRB-005', 'ONB-006']

**Retrieval metrics**:
Hit@1: 0, Hit@5: 0, Recall@5: 0.00, MRR: 0.00

**Reference answer similarity**: 0.00%

**Citation support rate**: 0.00%

**Refusal correctness**: 1


---

### Q050

**Question**:
What is the difference between machine learning and deep learning?

**Question type**:
None

**Expected answer**:


**Generated answer**:
NO_ANSWER_FOUND

WHAT I COULD NOT VERIFY:
- The definitions and distinctions between machine learning and deep learning.

**Expected chunks**:
[]

**Retrieved chunks**:
['FAQ-001', 'POL-002', 'POL-001', 'TRB-008', 'ONB-006', 'REL-002', 'API-009', 'TRB-010', 'TRB-007', 'FAQ-007']

**Retrieval metrics**:
Hit@1: 0, Hit@5: 0, Recall@5: 0.00, MRR: 0.00

**Reference answer similarity**: 0.00%

**Citation support rate**: 0.00%

**Refusal correctness**: 1


---

