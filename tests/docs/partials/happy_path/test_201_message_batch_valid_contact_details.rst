Scenario: An API consumer creating a batch of messages with valid contact details receives a 201 response
=========================================================================================================

| **Given** the API consumer provides valid contact details for a recipient in their new message batch
| **When** the request is submitted
| **Then** the response is a 201 success

**Asserts**
- Response returns a 201 status code
- Response contains routingPlanId
- Response contains messageBatchReference
- Response contains a messages array with expected message references and ids
