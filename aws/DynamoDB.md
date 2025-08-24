# Amazon DynamoDB: A Deep Dive

Amazon DynamoDB is a fully managed, serverless, key-value, and document NoSQL database service offered by Amazon Web Services (AWS). It's designed for single-digit millisecond performance at any scale, making it ideal for high-performance, high-scale applications.

## Table of Contents

1.  [What is DynamoDB?](#what-is-dynamodb)
2.  [Key Concepts and Features](#key-concepts-and-features)
    *   [Tables, Items, and Attributes](#tables-items-and-attributes)
    *   [Primary Keys](#primary-keys)
    *   [Data Types](#data-types)
    *   [Read/Write Capacity Modes](#readwrite-capacity-modes)
    *   [Secondary Indexes (GSI & LSI)](#secondary-indexes-gsi--lsi)
    *   [DynamoDB Streams](#dynamodb-streams)
    *   [Time-to-Live (TTL)](#time-to-live-ttl)
    *   [Transactions](#transactions)
    *   [Backup and Restore](#backup-and-restore)
    *   [Encryption at Rest](#encryption-at-rest)
3.  [Common Use Cases](#common-use-cases)
4.  [Detailed Examples (with AWS CLI)](#detailed-examples-with-aws-cli)
    *   [Setup AWS CLI](#setup-aws-cli)
    *   [Example 1: Create a Table](#example-1-create-a-table)
    *   [Example 2: Put an Item](#example-2-put-an-item)
    *   [Example 3: Get an Item (by Primary Key)](#example-3-get-an-item-by-primary-key)
    *   [Example 4: Query Items (by Partition Key and Sort Key)](#example-4-query-items-by-partition-key-and-sort-key)
    *   [Example 5: Scan Items (Full Table Scan)](#example-5-scan-items-full-table-scan)
    *   [Example 6: Update an Item](#example-6-update-an-item)
    *   [Example 7: Delete an Item](#example-7-delete-an-item)
    *   [Example 8: Add a Global Secondary Index (GSI)](#example-8-add-a-global-secondary-index-gsi)
    *   [Example 9: Query a GSI](#example-9-query-a-gsi)
    *   [Example 10: Delete a Table](#example-10-delete-a-table)
5.  [Best Practices and Considerations](#best-practices-and-considerations)
6.  [Conclusion](#conclusion)

---

## 1. What is DynamoDB?

DynamoDB is a fully managed NoSQL database service that provides fast and predictable performance with seamless scalability. It's built for scale, offering high availability, durability, and a flexible data model. As a serverless service, you don't manage any servers; AWS handles all the underlying infrastructure, patching, and backups.

**Key characteristics:**

*   **NoSQL:** Supports key-value and document data models, offering flexibility over traditional relational databases.
*   **Fully Managed:** AWS manages all the operational aspects.
*   **Serverless:** Pay only for what you use, without provisioning or managing servers.
*   **High Performance:** Consistent single-digit millisecond latency at any scale.
*   **Scalable:** Automatically scales to handle petabytes of data and millions of requests per second.
*   **Highly Available & Durable:** Data is replicated across multiple Availability Zones, offering high availability and durability.

## 2. Key Concepts and Features

### Tables, Items, and Attributes

*   **Table:** A collection of items. Similar to a table in a relational database.
*   **Item:** A group of attributes that is uniquely identifiable among all other items. Similar to a row in a relational database.
*   **Attribute:** A fundamental data element. Similar to a column in a relational database, but DynamoDB is schema-less, meaning items in the same table can have different attributes.

### Primary Keys

Every table must have a primary key that uniquely identifies each item. DynamoDB supports two types of primary keys:

1.  **Partition Key (Hash Attribute):** A simple primary key composed of one attribute. DynamoDB uses this key's value as input to an internal hash function to determine the partition (physical storage) where the item will be stored.
    *   **Example:** `UserId`
2.  **Partition Key and Sort Key (Hash and Range Attribute):** A composite primary key composed of two attributes. The first attribute is the partition key, and the second is the sort key. All items with the same partition key are stored together, and then sorted by the sort key value. This allows for efficient range queries.
    *   **Example:** `(UserId, OrderId)` or `(ProductId, Sku)`

### Data Types

DynamoDB supports three types of attributes:

1.  **Scalar Types:** Represent a single value.
    *   `Number` (N), `String` (S), `Binary` (B), `Boolean` (BOOL), `Null` (NULL)
2.  **Document Types:** Can contain other attributes.
    *   `List` (L), `Map` (M)
3.  **Set Types:** Collections of unique scalar values.
    *   `Number Set` (NS), `String Set` (SS), `Binary Set` (BS)

### Read/Write Capacity Modes

You determine how you pay for read and write throughput and how your table accommodates them:

1.  **On-Demand:**
    *   DynamoDB instantly accommodates your workloads as they ramp up or down.
    *   You pay per request for reads and writes, making it suitable for unpredictable traffic.
    *   No capacity planning needed.
2.  **Provisioned:**
    *   You specify the number of Read Capacity Units (RCUs) and Write Capacity Units (WCUs) your application needs per second.
    *   Suitable for predictable workloads.
    *   Can be more cost-effective for consistent, high-traffic tables.
    *   Includes Auto Scaling to automatically adjust provisioned capacity based on traffic.

### Secondary Indexes (GSI & LSI)

Secondary indexes allow you to query data using attributes other than the primary key.

1.  **Global Secondary Index (GSI):**
    *   Has a primary key that is different from the table's primary key.
    *   Can have a different partition key and a different sort key.
    *   Always "global," meaning it spans all partitions of the base table.
    *   Is considered a separate table in DynamoDB's internal implementation, so it has its own provisioned throughput settings and is eventually consistent with the base table.
2.  **Local Secondary Index (LSI):**
    *   Has the *same* partition key as the base table, but a *different* sort key.
    *   The index is "local" to a particular partition key value.
    *   Is strongly consistent with the base table.

### DynamoDB Streams

DynamoDB Streams capture a time-ordered sequence of item-level modifications (create, update, delete) in a DynamoDB table. You can use these streams for:

*   **Real-time analytics:** Integrate with AWS Lambda to process changes.
*   **Data replication:** Replicate data to another table or data store.
*   **Auditing:** Maintain a log of all data changes.

### Time-to-Live (TTL)

TTL allows you to define a specific attribute in your table as a timestamp. Items with an expired timestamp will be automatically deleted from the table by DynamoDB, typically within 24-48 hours. This is useful for managing data that expires, like session data or temporary logs.

### Transactions

DynamoDB transactions provide atomicity, consistency, isolation, and durability (ACID) for multiple item operations within and across tables. This ensures that a set of operations either all succeed or all fail, preventing data inconsistencies.

### Backup and Restore

DynamoDB offers two backup options:

1.  **On-Demand Backup:** Allows you to create full backups of your tables at any time.
2.  **Point-in-Time Recovery (PITR):** Enables continuous backups of your table data, allowing you to restore to any point in time within the last 35 days, down to the second.

### Encryption at Rest

All user data stored in DynamoDB is encrypted at rest by default using encryption keys stored in AWS Key Management Service (AWS KMS).

## 3. Common Use Cases

DynamoDB's characteristics make it suitable for a wide range of applications:

*   **Gaming:** User profiles, session data, leaderboards, game state.
*   **Ad Tech:** Real-time bidding, user profiles, campaign data.
*   **IoT:** Device sensor data, device metadata, command & control.
*   **User Profiles & Personalization:** Storing user preferences, history, and personalized content.
*   **E-commerce:** Product catalogs, shopping carts, order history.
*   **Microservices:** Backend data store for various microservices.
*   **Serverless Architectures:** Often used with AWS Lambda for event-driven applications.

## 4. Detailed Examples (with AWS CLI)

We'll use the AWS Command Line Interface (CLI) to demonstrate common DynamoDB operations.

**Scenario:** We'll manage a `Products` table.

*   **Primary Key:** `ProductId` (Partition Key)
*   **Attributes:** `ProductName`, `Category`, `Price`, `StockQuantity`, `Description`
*   **GSI:** `CategoryIndex` (Partition Key: `Category`, Sort Key: `Price`) to query products by category and sort them by price.

### Setup AWS CLI

Before proceeding, ensure you have the AWS CLI installed and configured with appropriate credentials and a default region.

```bash
# Install AWS CLI (if not already installed)
pip install awscli

# Configure AWS CLI
aws configure
# AWS Access Key ID [****************ZAXA]: YOUR_ACCESS_KEY_ID
# AWS Secret Access Key [****************w6C5]: YOUR_SECRET_ACCESS_KEY
# Default region name [us-east-1]: us-east-1
# Default output format [json]: json
```

### Example 1: Create a Table

Let's create a table named `Products` with `ProductId` as its partition key. We'll use On-Demand capacity for simplicity.

**Input (aws cli command):**

```bash
aws dynamodb create-table \
    --table-name Products \
    --attribute-definitions \
        AttributeName=ProductId,AttributeType=S \
    --key-schema \
        AttributeName=ProductId,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST
```

**Output (JSON response):**

```json
{
    "TableDescription": {
        "AttributeDefinitions": [
            {
                "AttributeName": "ProductId",
                "AttributeType": "S"
            }
        ],
        "TableName": "Products",
        "KeySchema": [
            {
                "AttributeName": "ProductId",
                "KeyType": "HASH"
            }
        ],
        "TableStatus": "CREATING",
        "CreationDateTime": "2023-10-27T10:00:00.000Z",
        "ProvisionedThroughput": {
            "NumberOfDecreasesToday": 0,
            "ReadCapacityUnits": 0,
            "WriteCapacityUnits": 0
        },
        "TableSizeBytes": 0,
        "ItemCount": 0,
        "TableArn": "arn:aws:dynamodb:us-east-1:123456789012:table/Products",
        "TableId": "abc123def456ghi789jkl012mno345pqr",
        "BillingModeSummary": {
            "BillingMode": "PAY_PER_REQUEST"
        },
        "DeletionProtectionEnabled": false
    }
}
```
*(Note: `TableStatus` will eventually become `ACTIVE`.)*

### Example 2: Put an Item

Add a new product to the `Products` table.

**Input (aws cli command):**

```bash
aws dynamodb put-item \
    --table-name Products \
    --item '{
        "ProductId": {"S": "PROD001"},
        "ProductName": {"S": "Laptop Pro X"},
        "Category": {"S": "Electronics"},
        "Price": {"N": "1200.00"},
        "StockQuantity": {"N": "50"},
        "Description": {"S": "High-performance laptop for professionals."}
    }'
```

**Output (JSON response):**

(No output by default for `put-item` unless `ReturnValues` parameter is used, e.g., `ReturnValues=ALL_OLD`)

```json
{}
```

Let's add a few more items for better query examples:

```bash
aws dynamodb put-item --table-name Products --item '{ "ProductId": {"S": "PROD002"}, "ProductName": {"S": "Wireless Mouse"}, "Category": {"S": "Accessories"}, "Price": {"N": "25.99"}, "StockQuantity": {"N": "200"} }'
aws dynamodb put-item --table-name Products --item '{ "ProductId": {"S": "PROD003"}, "ProductName": {"S": "4K Monitor"}, "Category": {"S": "Electronics"}, "Price": {"N": "450.00"}, "StockQuantity": {"N": "30"} }'
aws dynamodb put-item --table-name Products --item '{ "ProductId": {"S": "PROD004"}, "ProductName": {"S": "Ergonomic Keyboard"}, "Category": {"S": "Accessories"}, "Price": {"N": "75.00"}, "StockQuantity": {"N": "100"} }'
aws dynamodb put-item --table-name Products --item '{ "ProductId": {"S": "PROD005"}, "ProductName": {"S": "Gaming Headset"}, "Category": {"S": "Electronics"}, "Price": {"N": "99.99"}, "StockQuantity": {"N": "75"} }'
```

### Example 3: Get an Item (by Primary Key)

Retrieve a specific item using its `ProductId`.

**Input (aws cli command):**

```bash
aws dynamodb get-item \
    --table-name Products \
    --key '{
        "ProductId": {"S": "PROD001"}
    }'
```

**Output (JSON response):**

```json
{
    "Item": {
        "Description": {
            "S": "High-performance laptop for professionals."
        },
        "Price": {
            "N": "1200.00"
        },
        "Category": {
            "S": "Electronics"
        },
        "ProductId": {
            "S": "PROD001"
        },
        "ProductName": {
            "S": "Laptop Pro X"
        },
        "StockQuantity": {
            "N": "50"
        }
    }
}
```

### Example 4: Query Items (by Partition Key and Sort Key)

This example requires a GSI or LSI if you want to query by something other than the primary key. For the base table, `query` only works on the primary key. Since our `Products` table only has `ProductId` as the partition key, we can only query by `ProductId`.

*Let's imagine our primary key was `(Category, ProductId)` for this example's query capabilities. For the current table design, querying needs a GSI, which we'll add later.*

If the primary key was `(Category, ProductId)`, you could query as follows:

```bash
# This would work if (Category, ProductId) was the primary key
# Query products in 'Electronics' category
aws dynamodb query \
    --table-name Products \
    --key-condition-expression "Category = :c" \
    --expression-attribute-values '{":c": {"S": "Electronics"}}'
```
*Since our current table only has `ProductId` as the partition key, this query will fail.*

**Actual Query for current table:** A `query` operation always needs the full partition key. If we had a sort key, we could query within that partition. Since we only have `ProductId` as the PK, a `query` on the base table is essentially a `get-item` with some additional options, or a filtered scan.

### Example 5: Scan Items (Full Table Scan)

Scan retrieves all items from a table. It's generally inefficient for large tables as it reads every item and filters them on the client side, consuming a lot of Read Capacity Units. Use `query` whenever possible.

**Input (aws cli command):**

```bash
aws dynamodb scan \
    --table-name Products \
    --filter-expression "Price > :p" \
    --expression-attribute-values '{":p": {"N": "100"}}'
```

**Output (JSON response):**

```json
{
    "Items": [
        {
            "Description": {
                "S": "High-performance laptop for professionals."
            },
            "Price": {
                "N": "1200.00"
            },
            "Category": {
                "S": "Electronics"
            },
            "ProductId": {
                "S": "PROD001"
            },
            "ProductName": {
                "S": "Laptop Pro X"
            },
            "StockQuantity": {
                "N": "50"
            }
        },
        {
            "Price": {
                "N": "450.00"
            },
            "Category": {
                "S": "Electronics"
            },
            "ProductId": {
                "S": "PROD003"
            },
            "ProductName": {
                "S": "4K Monitor"
            },
            "StockQuantity": {
                "N": "30"
            }
        },
        {
            "Price": {
                "N": "99.99"
            },
            "Category": {
                "S": "Electronics"
            },
            "ProductId": {
                "S": "PROD005"
            },
            "ProductName": {
                "S": "Gaming Headset"
            },
            "StockQuantity": {
                "N": "75"
            }
        }
    ],
    "Count": 3,
    "ScannedCount": 5,
    "ConsumedCapacity": null
}
```
*Note: `Gaming Headset` (99.99) is not included because it's not `> 100`.*
*(Oops, my filter was `> 100` and I included `Gaming Headset` in my mental thought process. The output correctly excludes it. Let's make the filter `> 70` to include it for demo purposes, or just acknowledge the current output is correct).* The current output for `> 100` is correct. Let's use `> 70` instead to include the headset.

**Corrected Input for Scan (to include more items):**

```bash
aws dynamodb scan \
    --table-name Products \
    --filter-expression "Price > :p" \
    --expression-attribute-values '{":p": {"N": "70"}}'
```

**Corrected Output (JSON response for `Price > 70`):**

```json
{
    "Items": [
        {
            "Description": {
                "S": "High-performance laptop for professionals."
            },
            "Price": {
                "N": "1200.00"
            },
            "Category": {
                "S": "Electronics"
            },
            "ProductId": {
                "S": "PROD001"
            },
            "ProductName": {
                "S": "Laptop Pro X"
            },
            "StockQuantity": {
                "N": "50"
            }
        },
        {
            "Price": {
                "N": "450.00"
            },
            "Category": {
                "S": "Electronics"
            },
            "ProductId": {
                "S": "PROD003"
            },
            "ProductName": {
                "S": "4K Monitor"
            },
            "StockQuantity": {
                "N": "30"
            }
        },
        {
            "Price": {
                "N": "99.99"
            },
            "Category": {
                "S": "Electronics"
            },
            "ProductId": {
                "S": "PROD005"
            },
            "ProductName": {
                "S": "Gaming Headset"
            },
            "StockQuantity": {
                "N": "75"
            }
        },
        {
            "Price": {
                "N": "75.00"
            },
            "Category": {
                "S": "Accessories"
            },
            "ProductId": {
                "S": "PROD004"
            "ProductName": {
                "S": "Ergonomic Keyboard"
            },
            "StockQuantity": {
                "N": "100"
            }
        }
    ],
    "Count": 4,
    "ScannedCount": 5,
    "ConsumedCapacity": null
}
```

### Example 6: Update an Item

Update the `StockQuantity` and add a `LastUpdated` timestamp for a product.

**Input (aws cli command):**

```bash
aws dynamodb update-item \
    --table-name Products \
    --key '{
        "ProductId": {"S": "PROD001"}
    }' \
    --update-expression "SET StockQuantity = :sq, LastUpdated = :lu" \
    --expression-attribute-values '{
        ":sq": {"N": "45"},
        ":lu": {"S": "2023-10-27T10:30:00Z"}
    }' \
    --return-values ALL_NEW
```

**Output (JSON response):**

```json
{
    "Attributes": {
        "Description": {
            "S": "High-performance laptop for professionals."
        },
        "Price": {
            "N": "1200.00"
        },
        "LastUpdated": {
            "S": "2023-10-27T10:30:00Z"
        },
        "Category": {
            "S": "Electronics"
        },
        "ProductId": {
            "S": "PROD001"
        },
        "ProductName": {
            "S": "Laptop Pro X"
        },
        "StockQuantity": {
            "N": "45"
        }
    }
}
```

### Example 7: Delete an Item

Remove a product from the table.

**Input (aws cli command):**

```bash
aws dynamodb delete-item \
    --table-name Products \
    --key '{
        "ProductId": {"S": "PROD002"}
    }' \
    --return-values ALL_OLD
```

**Output (JSON response):**

```json
{
    "Attributes": {
        "Price": {
            "N": "25.99"
        },
        "Category": {
            "S": "Accessories"
        },
        "ProductId": {
            "S": "PROD002"
        },
        "ProductName": {
            "S": "Wireless Mouse"
        },
        "StockQuantity": {
            "N": "200"
        }
    }
}
```
*(No output if `ReturnValues` is not specified.)*

### Example 8: Add a Global Secondary Index (GSI)

Let's add `CategoryIndex` to the `Products` table. This GSI will allow us to query products by `Category` and optionally sort by `Price`.

**Input (aws cli command):**

```bash
aws dynamodb update-table \
    --table-name Products \
    --attribute-definitions \
        AttributeName=Category,AttributeType=S \
        AttributeName=Price,AttributeType=N \
    --global-secondary-index-updates \
        '[
            {
                "Create": {
                    "IndexName": "CategoryIndex",
                    "KeySchema": [
                        {"AttributeName": "Category", "KeyType": "HASH"},
                        {"AttributeName": "Price", "KeyType": "RANGE"}
                    ],
                    "Projection": {
                        "ProjectionType": "ALL"
                    },
                    "ProvisionedThroughput": {
                        "ReadCapacityUnits": 1,
                        "WriteCapacityUnits": 1
                    }
                }
            }
        ]' \
    --billing-mode PAY_PER_REQUEST
```
*Note: When using `PAY_PER_REQUEST` (On-Demand), the `ProvisionedThroughput` for GSI is ignored, but the CLI might still require it. For On-Demand tables, GSIs automatically scale.*

**Output (JSON response):**

```json
{
    "TableDescription": {
        "AttributeDefinitions": [
            {
                "AttributeName": "Category",
                "AttributeType": "S"
            },
            {
                "AttributeName": "ProductId",
                "AttributeType": "S"
            },
            {
                "AttributeName": "Price",
                "AttributeType": "N"
            }
        ],
        "TableName": "Products",
        "KeySchema": [
            {
                "AttributeName": "ProductId",
                "KeyType": "HASH"
            }
        ],
        "TableStatus": "UPDATING",
        "CreationDateTime": "2023-10-27T10:00:00.000Z",
        "ProvisionedThroughput": {
            "NumberOfDecreasesToday": 0,
            "ReadCapacityUnits": 0,
            "WriteCapacityUnits": 0
        },
        "TableSizeBytes": 0,
        "ItemCount": 4, # Items after deleting PROD002
        "TableArn": "arn:aws:dynamodb:us-east-1:123456789012:table/Products",
        "TableId": "abc123def456ghi789jkl012mno345pqr",
        "GlobalSecondaryIndexes": [
            {
                "IndexName": "CategoryIndex",
                "KeySchema": [
                    {
                        "AttributeName": "Category",
                        "KeyType": "HASH"
                    },
                    {
                        "AttributeName": "Price",
                        "KeyType": "RANGE"
                    }
                ],
                "Projection": {
                    "ProjectionType": "ALL"
                },
                "IndexStatus": "CREATING",
                "ProvisionedThroughput": {
                    "NumberOfDecreasesToday": 0,
                    "ReadCapacityUnits": 0,
                    "WriteCapacityUnits": 0
                },
                "IndexSizeBytes": 0,
                "ItemCount": 0,
                "IndexArn": "arn:aws:dynamodb:us-east-1:123456789012:table/Products/index/CategoryIndex"
            }
        ],
        "BillingModeSummary": {
            "BillingMode": "PAY_PER_REQUEST"
        },
        "DeletionProtectionEnabled": false
    }
}
```
*(Note: `TableStatus` and `IndexStatus` will eventually become `ACTIVE`.)*

### Example 9: Query a GSI

Now that `CategoryIndex` is active, we can query products by `Category` and sort by `Price`.

**Input (aws cli command):**

```bash
aws dynamodb query \
    --table-name Products \
    --index-name CategoryIndex \
    --key-condition-expression "Category = :c" \
    --expression-attribute-values '{":c": {"S": "Electronics"}}' \
    --scan-index-forward false # Sort by Price in descending order
```

**Output (JSON response):**

```json
{
    "Items": [
        {
            "Description": {
                "S": "High-performance laptop for professionals."
            },
            "Price": {
                "N": "1200.00"
            },
            "Category": {
                "S": "Electronics"
            },
            "ProductId": {
                "S": "PROD001"
            },
            "ProductName": {
                "S": "Laptop Pro X"
            },
            "StockQuantity": {
                "N": "45"
            },
            "LastUpdated": {
                "S": "2023-10-27T10:30:00Z"
            }
        },
        {
            "Price": {
                "N": "450.00"
            },
            "Category": {
                "S": "Electronics"
            },
            "ProductId": {
                "S": "PROD003"
            },
            "ProductName": {
                "S": "4K Monitor"
            },
            "StockQuantity": {
                "N": "30"
            }
        },
        {
            "Price": {
                "N": "99.99"
            },
            "Category": {
                "S": "Electronics"
            },
            "ProductId": {
                "S": "PROD005"
            },
            "ProductName": {
                "S": "Gaming Headset"
            },
            "StockQuantity": {
                "N": "75"
            }
        }
    ],
    "Count": 3,
    "ScannedCount": 3,
    "ConsumedCapacity": null
}
```
*(Note: Items are sorted by `Price` in descending order due to `scan-index-forward false`.)*

### Example 10: Delete a Table

Clean up the table after demonstrating the examples.

**Input (aws cli command):**

```bash
aws dynamodb delete-table \
    --table-name Products
```

**Output (JSON response):**

```json
{
    "TableDescription": {
        "AttributeDefinitions": [
            {
                "AttributeName": "Category",
                "AttributeType": "S"
            },
            {
                "AttributeName": "ProductId",
                "AttributeType": "S"
            },
            {
                "AttributeName": "Price",
                "AttributeType": "N"
            }
        ],
        "TableName": "Products",
        "KeySchema": [
            {
                "AttributeName": "ProductId",
                "KeyType": "HASH"
            }
        ],
        "TableStatus": "DELETING",
        "CreationDateTime": "2023-10-27T10:00:00.000Z",
        "ProvisionedThroughput": {
            "NumberOfDecreasesToday": 0,
            "ReadCapacityUnits": 0,
            "WriteCapacityUnits": 0
        },
        "TableSizeBytes": 0,
        "ItemCount": 3,
        "TableArn": "arn:aws:dynamodb:us-east-1:123456789012:table/Products",
        "TableId": "abc123def456ghi789jkl012mno345pqr",
        "GlobalSecondaryIndexes": [
            {
                "IndexName": "CategoryIndex",
                "KeySchema": [
                    {
                        "AttributeName": "Category",
                        "KeyType": "HASH"
                    },
                    {
                        "AttributeName": "Price",
                        "KeyType": "RANGE"
                    }
                ],
                "Projection": {
                    "ProjectionType": "ALL"
                },
                "IndexStatus": "DELETING",
                "ProvisionedThroughput": {
                    "NumberOfDecreasesToday": 0,
                    "ReadCapacityUnits": 0,
                    "WriteCapacityUnits": 0
                },
                "IndexSizeBytes": 0,
                "ItemCount": 0,
                "IndexArn": "arn:aws:dynamodb:us-east-1:123456789012:table/Products/index/CategoryIndex"
            }
        ],
        "BillingModeSummary": {
            "BillingMode": "PAY_PER_REQUEST"
        },
        "DeletionProtectionEnabled": false
    }
}
```
*(The table and its associated GSIs will be deleted asynchronously.)*

## 5. Best Practices and Considerations

*   **Schema Design:** The most critical aspect. Carefully choose your primary key (partition key and sort key) to ensure even data distribution and efficient access patterns.
    *   **High Cardinality Partition Key:** Choose a partition key with many distinct values to avoid "hot partitions" (a single partition receiving a disproportionate amount of traffic).
    *   **Avoid Large Items:** DynamoDB has an item size limit (400KB).
*   **Query vs. Scan:** Always prefer `Query` over `Scan`. `Query` is efficient as it uses the primary key or a secondary index. `Scan` reads the entire table and can be very expensive and slow.
*   **Capacity Planning:**
    *   For unpredictable workloads, use **On-Demand** capacity.
    *   For predictable workloads, use **Provisioned** capacity with Auto Scaling.
*   **Secondary Indexes:** Design GSIs and LSIs carefully to support your query patterns. Remember that GSIs have their own capacity settings and are eventually consistent.
*   **Error Handling and Retries:** Implement exponential backoff and retry mechanisms in your application code for transient errors.
*   **Cost Optimization:** Use TTL for expiring data, monitor capacity usage, and choose the appropriate capacity mode.
*   **Global Tables:** For multi-region, active-active applications, consider Global Tables for automatic replication across AWS regions.

## 6. Conclusion

Amazon DynamoDB is a powerful, highly scalable, and fully managed NoSQL database service perfect for applications requiring high performance and availability. Its serverless nature simplifies operations, allowing developers to focus on building features rather than managing infrastructure. By understanding its core concepts and applying best practices, you can leverage DynamoDB to build robust, high-performance applications that can scale to meet virtually any demand.