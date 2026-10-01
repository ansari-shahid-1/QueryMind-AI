# QueryMind AI — Database Schema

## 1. Overview

QueryMind AI uses PostgreSQL to store and analyze the Brazilian E-Commerce Public Dataset by Olist.

The database is organized into two schemas:

* `raw`: Original dataset records imported without modifying their values.
* `analytics`: Cleaned and typed tables prepared for analytical queries.

The raw data is preserved to maintain data lineage and support future validation.

## 2. Analytics Tables

### customers

Stores customer information.

| Column                   | Data Type | Key         |
| ------------------------ | --------- | ----------- |
| customer_id              | TEXT      | Primary Key |
| customer_unique_id       | TEXT      |             |
| customer_zip_code_prefix | TEXT      |             |
| customer_city            | TEXT      |             |
| customer_state           | TEXT      |             |

### orders

Stores order details and timestamps.

| Column                        | Data Type | Key         |
| ----------------------------- | --------- | ----------- |
| order_id                      | TEXT      | Primary Key |
| customer_id                   | TEXT      | Foreign Key |
| order_status                  | TEXT      |             |
| order_purchase_timestamp      | TIMESTAMP |             |
| order_approved_at             | TIMESTAMP |             |
| order_delivered_carrier_date  | TIMESTAMP |             |
| order_delivered_customer_date | TIMESTAMP |             |
| order_estimated_delivery_date | TIMESTAMP |             |

### order_items

Stores products included in each order.

| Column              | Data Type     | Key                                |
| ------------------- | ------------- | ---------------------------------- |
| order_id            | TEXT          | Composite Primary Key, Foreign Key |
| order_item_id       | INTEGER       | Composite Primary Key              |
| product_id          | TEXT          | Foreign Key                        |
| seller_id           | TEXT          | Foreign Key                        |
| shipping_limit_date | TIMESTAMP     |                                    |
| price               | NUMERIC(12,2) |                                    |
| freight_value       | NUMERIC(12,2) |                                    |

### payments

Stores payment information for orders.

| Column               | Data Type     | Key                                |
| -------------------- | ------------- | ---------------------------------- |
| order_id             | TEXT          | Composite Primary Key, Foreign Key |
| payment_sequential   | INTEGER       | Composite Primary Key              |
| payment_type         | TEXT          |                                    |
| payment_installments | INTEGER       |                                    |
| payment_value        | NUMERIC(12,2) |                                    |

### order_reviews

Stores customer review records.

| Column                  | Data Type | Key         |
| ----------------------- | --------- | ----------- |
| review_record_id        | BIGINT    | Primary Key |
| review_id               | TEXT      |             |
| order_id                | TEXT      | Foreign Key |
| review_score            | INTEGER   |             |
| review_comment_title    | TEXT      |             |
| review_comment_message  | TEXT      |             |
| review_creation_date    | TIMESTAMP |             |
| review_answer_timestamp | TIMESTAMP |             |

**Important:** `review_record_id` is a generated surrogate key. The original `review_id` is not unique across all records, so review records must not be deduplicated using `review_id` alone.

### products

Stores product attributes.

| Column                     | Data Type | Key         |
| -------------------------- | --------- | ----------- |
| product_id                 | TEXT      | Primary Key |
| product_category_name      | TEXT      |             |
| product_name_lenght        | INTEGER   |             |
| product_description_lenght | INTEGER   |             |
| product_photos_qty         | INTEGER   |             |
| product_weight_g           | INTEGER   |             |
| product_length_cm          | INTEGER   |             |
| product_height_cm          | INTEGER   |             |
| product_width_cm           | INTEGER   |             |

### sellers

Stores seller information.

| Column                 | Data Type | Key         |
| ---------------------- | --------- | ----------- |
| seller_id              | TEXT      | Primary Key |
| seller_zip_code_prefix | TEXT      |             |
| seller_city            | TEXT      |             |
| seller_state           | TEXT      |             |

### geolocation

Stores geographic coordinates associated with ZIP code prefixes.

| Column                      | Data Type     | Key |
| --------------------------- | ------------- | --- |
| geolocation_zip_code_prefix | TEXT          |     |
| geolocation_lat             | NUMERIC(12,8) |     |
| geolocation_lng             | NUMERIC(12,8) |     |
| geolocation_city            | TEXT          |     |
| geolocation_state           | TEXT          |     |

**Important:** ZIP code prefixes are repeated. Do not assume that a ZIP code prefix identifies exactly one geographic record.

### category_translation

Maps Portuguese product category names to English translations.

| Column                        | Data Type | Key         |
| ----------------------------- | --------- | ----------- |
| product_category_name         | TEXT      | Primary Key |
| product_category_name_english | TEXT      |             |

## 3. Relationships

| Child Table   | Column      | Parent Table | Referenced Column |
| ------------- | ----------- | ------------ | ----------------- |
| orders        | customer_id | customers    | customer_id       |
| order_items   | order_id    | orders       | order_id          |
| order_items   | product_id  | products     | product_id        |
| order_items   | seller_id   | sellers      | seller_id         |
| payments      | order_id    | orders       | order_id          |
| order_reviews | order_id    | orders       | order_id          |

## 4. Analytical Considerations

1. **Order value:** Product value and freight charges are stored separately in `order_items`. Avoid double-counting when joining to payments.
2. **One-to-many relationships:** An order can contain multiple items, payments, and review records. Joining these tables directly can multiply rows and inflate aggregate metrics.
3. **Customer identity:** `customer_id` identifies a customer record associated with an order, while `customer_unique_id` represents the unique customer identity across records.
4. **Missing values:** Some timestamps, review comments, and product attributes are missing. Missing values should be handled explicitly in analytical queries.
5. **Review records:** Preserve all review records and use `review_record_id` as the unique row identifier.
6. **Geolocation:** ZIP code prefixes are not unique and should not be treated as primary keys.
7. **Raw data preservation:** Analytical transformations must not modify the original raw tables.

## 5. Data Preparation Status

* [x] Raw data imported
* [x] Data profiling completed
* [x] Data quality checks completed
* [x] Analytics tables created
* [x] Data types converted
* [x] Row counts reconciled
* [x] Primary keys added
* [x] Foreign keys added
* [x] Database schema documented
