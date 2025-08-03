# Technical Assessment: MCP Server & LLM Client Implementation

## Overview

Build a two-service architecture demonstrating MCP (Model Context Protocol) integration with an LLM client.

| Component | Description | Time Allocation |
|-----------|-------------|-----------------|
| **Task A: MCP Server** | Service implementing a MCP with 3 tools | ≤ 2 hours |
| **Task B: LLM Client** | Service using the MCP to boost an LLM (e.g., OpenAI GPT-4, Claude, Llama, you choose!) | ≤ 2 hours |
| **Total Time** | Complete within ~4 hours effort 

---

## Data Backend

Your "database" consists of JSON files in the `/data` directory:
- `customers.json` - Customer records
- `orders.json` - Order transactions
- Additional files may be created as needed

---

## Task A: MCP Server

Here you'll build a server that will offer the tools that the LLM client will use.

### Requirements

1. **MCP Protocol Implementation**
   - Handle `tools/list` and `tools/call` endpoints (https://modelcontextprotocol.io/docs/concepts/tools)

2. **Tool Definitions**

You must implement exactly three tools:

#### Tool 1: `get_order_count_by_customer_and_month`
- **Description**: Count orders for one customer in a specific calendar month
- **Input Schema**:
  ```json
  {
    "customerName": "string",
    "isoMonth": "string" // Format: "YYYY-MM"
  }
  ```
- **Output Schema**:
  ```json
  {
    "count": "number"
  }
  ```

#### Tool 2: `list_recent_customers_by_country`
- **Description**: Fetch the newest N customers from a specific country
- **Input Schema**:
  ```json
  {
    "country": "string",
    "limit": "number?" // Optional, defaults to reasonable value
  }
  ```
- **Output Schema**:
  ```json
  {
    "customers": [
      {
        "id": "number",
        "name": "string",
        "joinedAt": "string", // ISO date
        "totalSpend": "number"
      }
    ]
  }
  ```

#### Tool 3: `get_customer_total_spend`
- **Description**: Calculate aggregate spending for multiple customers
- **Input Schema**:
  ```json
  {
    "customerIds": ["number"]
  }
  ```
- **Output Schema**:
  ```json
  {
    "totals": [
      {
        "customerId": "number",
        "spend": "number"
      }
    ]
  }
  ```

### Error Handling
- Validate all inputs against defined schemas
- Return MCP error with `status: "invalid_arguments"` for validation failures
- Log errors appropriately


### Using your MCP in Task B
For Task B (LLM integration), if you're using a cloud-based LLM, you will need to expose you MCP server in a public URL (can't do localhost:PORT) - you can do this by using localtunnel (https://localtunnel.me/), but you can use any tool you want - like ngrok, for example. If you decide to use localtunnel, you can run it with:
```bash
npx localtunnel --port 4000  # Replace 4000 with your server’s port  
```
Copy the generated public URL (e.g., https://your-subdomain.loca.lt) and use it in your LLM client.

---

## Task B: LLM Client
This is where the magic happens. You'll build a client that uses the tools you implemented in Task A.
This client will be a simple API that takes a question and returns an answer from the LLM - quesiton comes in, answer comes out.

### Requirements

1. **LLM Integration**
   - You are free to use any LLM provider you want (e.g., OpenAI, Claude, Llama, Mistral, etc.).
   - Handle tool/function calling capabilities

2. **API Endpoint**

   **POST** `/ask`
   
   Request body:
   ```json
   {
     "question": "string"
   }
   ```
   
   Response:
   ```json
   {
     "answer": "string with tool citations"
   }
   ```

### Notes
- Ensure your MCP server is running and accessible via the tunnel before testing.
___

### Acceptance Test Cases

| Test Prompt | Expected Behavior |
|-------------|-------------------|
| "How many orders did John Doe place in March 2025?" | - Calls `get_order_count_by_customer_and_month` with correct parameters<br>- Returns integer count with citation |
| "List the last 2 customers from Brazil and their total spend." | - Calls `list_recent_customers_by_country` with `country: "France", limit: 2`<br>- Returns formatted list of 2 customers |
| "What is the total spend for customers John Doe and Jane Smith?" | - Calls `get_customer_total_spend` with correct parameters<br>- Returns aggregate spend with citation 

---

## Submission Guidelines

1. **Documentation**
   - Include basic setup instructions
   - Document any assumptions made

2. **Testing (Bonus)**
   - Include unit tests for core functionality
   - Provide integration test examples
   - Document how to run tests

## Evaluation Criteria

- **Correctness**: Tools work as specified
- **Code Quality**: Clean, maintainable code
- **Error Handling**: Robust validation and error responses
- **Prioritization**: What you prioritized, what you did not have time for, and the reasons
- **Performance**: Efficient data processing and API calls

___


### CodeSubmit

Please organize, design, test, and document your code as if it were
going into production - then push your changes to the master branch.

Have fun coding! 🚀
