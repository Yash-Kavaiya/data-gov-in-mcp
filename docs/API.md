# API Documentation

## Overview

The data.gov.in MCP Server provides a set of tools to interact with India's national open data portal through the Model Context Protocol.

## Available Tools

### 1. get_dataset

Retrieve data from a specific dataset/resource on data.gov.in.

**Parameters:**
- `resource_id` (string, required): The unique identifier for the dataset resource
- `limit` (integer, optional): Maximum number of records to return (default: 10, max: 100)
- `offset` (integer, optional): Number of records to skip for pagination (default: 0)
- `filters` (string, optional): JSON string of filters to apply

**Returns:**
JSON string containing:
- `resource_id`: The requested resource ID
- `total_records`: Total number of records available
- `offset`: Current offset
- `limit`: Current limit
- `records`: Array of data records
- `fields`: Array of field definitions

**Example Request:**
```json
{
  "resource_id": "9ef84268-d588-465a-a308-a864a43d0070",
  "limit": 5,
  "offset": 0
}
```

**Example Response:**
```json
{
  "resource_id": "9ef84268-d588-465a-a308-a864a43d0070",
  "total_records": 1000,
  "offset": 0,
  "limit": 5,
  "records": [
    {
      "id": "1",
      "name": "Example Record",
      "value": "123"
    }
  ],
  "fields": [
    {
      "id": "id",
      "type": "text"
    },
    {
      "id": "name",
      "type": "text"
    }
  ]
}
```

---

### 2. get_dataset_fields

Get field information and schema for a dataset.

**Parameters:**
- `resource_id` (string, required): The unique identifier for the dataset resource

**Returns:**
JSON string containing:
- `resource_id`: The requested resource ID
- `field_count`: Number of fields in the dataset
- `fields`: Array of field definitions with IDs and types

**Example Request:**
```json
{
  "resource_id": "9ef84268-d588-465a-a308-a864a43d0070"
}
```

**Example Response:**
```json
{
  "resource_id": "9ef84268-d588-465a-a308-a864a43d0070",
  "field_count": 5,
  "fields": [
    {
      "id": "state",
      "type": "text"
    },
    {
      "id": "population",
      "type": "number"
    }
  ]
}
```

---

### 3. paginate_dataset

Retrieve a specific page of data from a dataset.

**Parameters:**
- `resource_id` (string, required): The unique identifier for the dataset resource
- `page` (integer, optional): Page number to retrieve (starting from 1, default: 1)
- `page_size` (integer, optional): Number of records per page (default: 10, max: 100)

**Returns:**
JSON string containing:
- `resource_id`: The requested resource ID
- `pagination`: Pagination metadata
  - `current_page`: Current page number
  - `page_size`: Records per page
  - `total_records`: Total number of records
  - `total_pages`: Total number of pages
  - `has_next`: Whether there's a next page
  - `has_previous`: Whether there's a previous page
- `records`: Array of data records for the current page

**Example Request:**
```json
{
  "resource_id": "9ef84268-d588-465a-a308-a864a43d0070",
  "page": 2,
  "page_size": 20
}
```

**Example Response:**
```json
{
  "resource_id": "9ef84268-d588-465a-a308-a864a43d0070",
  "pagination": {
    "current_page": 2,
    "page_size": 20,
    "total_records": 100,
    "total_pages": 5,
    "has_next": true,
    "has_previous": true
  },
  "records": [...]
}
```

---

### 4. get_dataset_summary

Get a summary of a dataset including record count and field information.

**Parameters:**
- `resource_id` (string, required): The unique identifier for the dataset resource

**Returns:**
JSON string containing:
- `resource_id`: The requested resource ID
- `total_records`: Total number of records in the dataset
- `field_count`: Number of fields
- `fields`: List of field names
- `sample_record`: A sample record from the dataset

**Example Request:**
```json
{
  "resource_id": "9ef84268-d588-465a-a308-a864a43d0070"
}
```

**Example Response:**
```json
{
  "resource_id": "9ef84268-d588-465a-a308-a864a43d0070",
  "total_records": 1000,
  "field_count": 5,
  "fields": ["state", "district", "population", "area", "density"],
  "sample_record": {
    "state": "Maharashtra",
    "district": "Mumbai",
    "population": "12442373"
  }
}
```

---

### 5. filter_dataset

Filter dataset records by a specific field value.

**Parameters:**
- `resource_id` (string, required): The unique identifier for the dataset resource
- `field` (string, required): The field name to filter on
- `value` (string, required): The value to filter for
- `limit` (integer, optional): Maximum number of matching records to return (default: 10)

**Returns:**
JSON string containing:
- `resource_id`: The requested resource ID
- `filter`: The applied filter
- `matched_records`: Number of matching records returned
- `records`: Array of matching data records

**Example Request:**
```json
{
  "resource_id": "9ef84268-d588-465a-a308-a864a43d0070",
  "field": "state",
  "value": "Maharashtra",
  "limit": 5
}
```

**Example Response:**
```json
{
  "resource_id": "9ef84268-d588-465a-a308-a864a43d0070",
  "filter": {
    "state": "Maharashtra"
  },
  "matched_records": 5,
  "records": [...]
}
```

---

### 6. get_cache_statistics

Get statistics about the API response cache.

**Parameters:**
None

**Returns:**
JSON string containing:
- `cache_enabled`: Whether caching is enabled
- `size`: Current number of cached entries
- `max_size`: Maximum cache size
- `hits`: Number of cache hits
- `misses`: Number of cache misses
- `hit_rate`: Cache hit rate percentage

**Example Request:**
```json
{}
```

**Example Response:**
```json
{
  "cache_enabled": true,
  "size": 45,
  "max_size": 1000,
  "hits": 120,
  "misses": 30,
  "hit_rate": "80.00%"
}
```

---

### 7. clear_cache

Clear all cached API responses.

**Parameters:**
None

**Returns:**
JSON string containing:
- `success`: Whether the operation was successful
- `message`: Confirmation message

**Example Request:**
```json
{}
```

**Example Response:**
```json
{
  "success": true,
  "message": "Cache cleared successfully"
}
```

---

### 8. get_server_info

Get information about the MCP server and its configuration.

**Parameters:**
None

**Returns:**
JSON string containing:
- `server`: Server name
- `version`: Server version
- `configuration`: Current configuration settings
- `api_key_configured`: Whether API key is set

**Example Request:**
```json
{}
```

**Example Response:**
```json
{
  "server": "data.gov.in MCP Server",
  "version": "1.0.0",
  "configuration": {
    "api_base_url": "https://api.data.gov.in",
    "cache_enabled": true,
    "cache_ttl": 3600,
    "rate_limit": "100 calls per 60s",
    "timeout": "30s",
    "default_limit": 10,
    "max_limit": 100
  },
  "api_key_configured": true
}
```

---

## Error Handling

All tools return error information in a consistent format:

```json
{
  "error": "Description of the error"
}
```

### Common Errors

1. **APIKeyMissingError**
   - Message: "API key is required. Set DATA_GOV_IN_API_KEY environment variable."
   - Solution: Configure your API key

2. **ResourceNotFoundError**
   - Message: "Resource '{resource_id}' not found"
   - Solution: Verify the resource ID

3. **RateLimitError**
   - Message: "Rate limit exceeded. Please try again later."
   - Solution: Wait for the rate limit window to reset

4. **InvalidParameterError**
   - Message: "Invalid parameter '{param}': {details}"
   - Solution: Check parameter values

## Rate Limiting

The server implements automatic rate limiting to comply with data.gov.in API limits:

- Default: 100 calls per 60 seconds
- Configurable via environment variables
- Automatic backoff when limit is approached
- Transparent to the user

## Caching

Response caching improves performance:

- Default TTL: 1 hour (3600 seconds)
- LRU eviction policy
- Configurable size and TTL
- Per-request cache bypass available

## Best Practices

1. **Use pagination for large datasets**
   ```json
   {
     "resource_id": "xxx",
     "page": 1,
     "page_size": 50
   }
   ```

2. **Check dataset schema first**
   ```json
   {
     "resource_id": "xxx"
   }
   ```
   Use `get_dataset_fields` before querying data.

3. **Use filters to reduce data transfer**
   ```json
   {
     "resource_id": "xxx",
     "field": "state",
     "value": "Maharashtra"
   }
   ```

4. **Monitor cache performance**
   ```json
   {}
   ```
   Use `get_cache_statistics` to optimize caching.

## Examples

### Example 1: Exploring a New Dataset

```javascript
// Step 1: Get dataset summary
get_dataset_summary({ resource_id: "xxx" })

// Step 2: Get field definitions
get_dataset_fields({ resource_id: "xxx" })

// Step 3: Retrieve sample data
get_dataset({ resource_id: "xxx", limit: 5 })
```

### Example 2: Paginating Through All Records

```javascript
// Get first page
paginate_dataset({ resource_id: "xxx", page: 1, page_size: 50 })

// Get second page
paginate_dataset({ resource_id: "xxx", page: 2, page_size: 50 })

// Continue until has_next is false
```

### Example 3: Filtering and Analysis

```javascript
// Filter by state
filter_dataset({
  resource_id: "xxx",
  field: "state",
  value: "Maharashtra",
  limit: 100
})

// Get all fields for analysis
get_dataset_fields({ resource_id: "xxx" })
```

## Support

For API issues or questions:
- GitHub Issues: https://github.com/Yash-Kavaiya/data-gov-in-mcp/issues
- Email: yash.kavaiya3@gmail.com
