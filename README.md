# Salesforce MCP Server

A Model Context Protocol (MCP) server that provides tools for interacting with Salesforce CRM through its REST API. This server enables AI assistants to query data using SOQL and perform CRUD operations on Salesforce objects like Leads.

## Features

- **SOQL Query Execution**: Run Salesforce Object Query Language (SOQL) queries to fetch data from your Salesforce org
- **Lead Management**: Complete CRUD operations (Create, Read, Update, Delete) for Salesforce Lead objects
- **OAuth Authentication**: Secure authentication using OAuth 2.0 password grant flow
- **Custom Field Support**: Handle both standard and custom Salesforce fields

## Prerequisites

- Python >= 3.14
- Salesforce account with API access
- OAuth credentials (Client ID and Client Secret)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd salesforceMCP
```

2. Install dependencies using uv (recommended) or pip:
```bash
uv sync
```

3. Create a `.env` file in the root directory with your Salesforce credentials:
```env
URL=your-instance.my.salesforce.com
CLIENT_ID=your_client_id
CLIENT_SECRET=your_client_secret
USERNAME=your_username
PASSWORD=your_password
```

## Configuration

To use this MCP server with Claude Desktop or Cursor, you need to configure it in your MCP settings file.

### Claude Desktop

Add the following to your Claude Desktop configuration file:
- MacOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "salesforce": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/salesforceMCP",
        "run",
        "main.py"
      ],
      "env": {
        "URL": "your-instance.my.salesforce.com",
        "CLIENT_ID": "your_client_id",
        "CLIENT_SECRET": "your_client_secret",
        "USERNAME": "your_username",
        "PASSWORD": "your_password"
      }
    }
  }
}
```

### Cursor

Add the following to your Cursor MCP settings file (`~/.cursor/mcp.json` or similar):

```json
{
  "mcpServers": {
    "salesforce": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/salesforceMCP",
        "run",
        "main.py"
      ],
      "env": {
        "URL": "your-instance.my.salesforce.com",
        "CLIENT_ID": "your_client_id",
        "CLIENT_SECRET": "your_client_secret",
        "USERNAME": "your_username",
        "PASSWORD": "your_password"
      }
    }
  }
}
```

**Important:** Replace `/absolute/path/to/salesforceMCP` with the actual absolute path to your project directory, and fill in your Salesforce credentials.

After adding the configuration, restart Claude Desktop or Cursor for the changes to take effect.

## Available Tools

### 1. `run_soql`

Execute SOQL queries to fetch data from Salesforce.

**Parameters:**
- `query` (str): The SOQL query to execute

**Example:**
```python
query = "SELECT Id, Name, Email FROM Lead WHERE Status = 'Open' LIMIT 10"
```

**Note:** Custom objects and fields in Salesforce end with `__c`

### 2. `run_lead_operation`

Perform CRUD operations on Salesforce Lead objects.

**Operations:**
- `create`: Create a new Lead (requires `LastName` and `Company`)
- `update`: Update an existing Lead (requires `lead_id`)
- `delete`: Delete a Lead (requires `lead_id`)
- `get`: Fetch a Lead by ID (requires `lead_id`)

**Standard Fields:**
- `lead_id`: Salesforce Lead ID (required for update, delete, get)
- `last_name`: Lead's last name (required for create)
- `company`: Lead's company (required for create)
- `first_name`: Lead's first name
- `salutation`: Salutation (e.g., 'Mr.', 'Ms.', 'Dr.')
- `title`: Job title
- `email`: Email address
- `phone`: Phone number
- `mobile_phone`: Mobile phone number
- `fax`: Fax number
- `website`: Website URL
- `lead_source`: Lead source (e.g., 'Web', 'Phone Inquiry')
- `status`: Lead status (e.g., 'Open', 'Contacted', 'Qualified')
- `rating`: Lead rating (e.g., 'Hot', 'Warm', 'Cold')
- `industry`: Industry
- `annual_revenue`: Annual revenue (float)
- `number_of_employees`: Number of employees (int)
- `street`: Street address
- `city`: City
- `state`: State/Province
- `postal_code`: Postal/ZIP code
- `country`: Country
- `description`: Notes about the lead
- `owner_id`: Salesforce User ID of lead owner
- `is_converted`: Whether the lead has been converted (bool)
- `custom_fields`: Dictionary of custom fields (e.g., `{"My_Field__c": "value"}`)

## Project Structure

```
salesforceMCP/
├── main.py                          # Entry point for the MCP server
├── src/
│   └── salesforce_mcp/
│       ├── objects/                 # Salesforce object implementations
│       │   ├── SFObject.py         # Base object class
│       │   └── LeadObject.py       # Lead object operations
│       ├── services/                # Core services
│       │   └── SalesforceSession.py # Session and authentication handling
│       ├── types/                   # Type definitions
│       │   ├── SFRecord.py         # Base record type
│       │   └── LeadRecord.py       # Lead record type
│       └── utils/                   # Utility modules
│           ├── soql.py             # SOQL query execution
│           ├── credentials.py       # Credential management
│           └── dataClassMapper.py  # Data class mapping utilities
├── tests/                           # Test files
├── pyproject.toml                   # Project configuration
└── .env                            # Environment variables (not in repo)
```

## Development

### Running Tests

```bash
pytest
```

### Test Coverage

```bash
pytest --cov=src --cov-report=html
```

## Authentication

This server uses OAuth 2.0 password grant flow for authentication. Each request to Salesforce will:
1. Authenticate using the credentials from your `.env` file
2. Obtain an access token
3. Use the token for API requests

## Error Handling

The server includes comprehensive error logging. Errors are logged to stderr with timestamps and severity levels.

## Dependencies

- `fastmcp>=2.14.1` - FastMCP framework for building MCP servers
- `mcp[cli]>=1.25.0` - Model Context Protocol implementation
- `requests>=2.32.5` - HTTP library for API requests
- `pytest>=9.0.2` - Testing framework
- `pytest-cov>=7.0.0` - Test coverage plugin
- `pytest-mock>=3.15.1` - Mocking plugin for pytest

## Security Notes

- Never commit your `.env` file to version control
- Keep your OAuth credentials secure
- Use environment variables for sensitive configuration
- Validate domain names before making requests
