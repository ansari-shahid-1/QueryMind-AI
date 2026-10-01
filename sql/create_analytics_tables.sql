CREATE TABLE IF NOT EXISTS analytics.orders AS
SELECT
    order_id,
    customer_id,
    order_status,

    NULLIF(BTRIM(order_purchase_timestamp), '')::TIMESTAMP
        AS order_purchase_timestamp,

    NULLIF(BTRIM(order_approved_at), '')::TIMESTAMP
        AS order_approved_at,

    NULLIF(BTRIM(order_delivered_carrier_date), '')::TIMESTAMP
        AS order_delivered_carrier_date,

    NULLIF(BTRIM(order_delivered_customer_date), '')::TIMESTAMP
        AS order_delivered_customer_date,

    NULLIF(BTRIM(order_estimated_delivery_date), '')::TIMESTAMP
        AS order_estimated_delivery_date

FROM raw.orders;

CREATE TABLE IF NOT EXISTS analytics.order_items AS
SELECT
    order_id,
    order_item_id::INTEGER AS order_item_id,
    product_id,
    seller_id,

    NULLIF(BTRIM(shipping_limit_date), '')::TIMESTAMP
        AS shipping_limit_date,

    price::NUMERIC(12,2) AS price,
    freight_value::NUMERIC(12,2) AS freight_value

FROM raw.order_items;

CREATE TABLE IF NOT EXISTS analytics.payments AS
SELECT
    order_id,
    payment_sequential::INTEGER AS payment_sequential,
    payment_type,
    payment_installments::INTEGER AS payment_installments,
    payment_value::NUMERIC(12,2) AS payment_value
FROM raw.payments;

CREATE TABLE IF NOT EXISTS analytics.products AS
SELECT
    product_id,
    product_category_name,

    NULLIF(BTRIM(product_name_lenght), '')::INTEGER
        AS product_name_lenght,

    NULLIF(BTRIM(product_description_lenght), '')::INTEGER
        AS product_description_lenght,

    NULLIF(BTRIM(product_photos_qty), '')::INTEGER
        AS product_photos_qty,

    NULLIF(BTRIM(product_weight_g), '')::INTEGER
        AS product_weight_g,

    NULLIF(BTRIM(product_length_cm), '')::INTEGER
        AS product_length_cm,

    NULLIF(BTRIM(product_height_cm), '')::INTEGER
        AS product_height_cm,

    NULLIF(BTRIM(product_width_cm), '')::INTEGER
        AS product_width_cm

FROM raw.products;

CREATE TABLE IF NOT EXISTS analytics.sellers AS
SELECT
    seller_id,
    seller_zip_code_prefix,
    seller_city,
    seller_state
FROM raw.sellers;

CREATE TABLE IF NOT EXISTS analytics.customers AS
SELECT
    customer_id,
    customer_unique_id,
    customer_zip_code_prefix,
    customer_city,
    customer_state
FROM raw.customers;

CREATE TABLE IF NOT EXISTS analytics.order_reviews AS
SELECT
    ROW_NUMBER() OVER (
        ORDER BY review_id, order_id
    ) AS review_record_id,

    review_id,
    order_id,
    review_score::INTEGER AS review_score,
    review_comment_title,
    review_comment_message,

    NULLIF(BTRIM(review_creation_date), '')::TIMESTAMP
        AS review_creation_date,

    NULLIF(BTRIM(review_answer_timestamp), '')::TIMESTAMP
        AS review_answer_timestamp

FROM raw.order_reviews;

CREATE TABLE IF NOT EXISTS analytics.geolocation AS
SELECT
    geolocation_zip_code_prefix,
    geolocation_lat::NUMERIC(12,8) AS geolocation_lat,
    geolocation_lng::NUMERIC(12,8) AS geolocation_lng,
    geolocation_city,
    geolocation_state
FROM raw.geolocation;

CREATE TABLE IF NOT EXISTS analytics.category_translation AS
SELECT
    product_category_name,
    product_category_name_english
FROM raw.category_translation;

ALTER TABLE analytics.customers
ADD CONSTRAINT pk_analytics_customers
PRIMARY KEY (customer_id);

ALTER TABLE analytics.orders
ADD CONSTRAINT pk_analytics_orders
PRIMARY KEY (order_id);

ALTER TABLE analytics.products
ADD CONSTRAINT pk_analytics_products
PRIMARY KEY (product_id);

ALTER TABLE analytics.sellers
ADD CONSTRAINT pk_analytics_sellers
PRIMARY KEY (seller_id);

ALTER TABLE analytics.category_translation
ADD CONSTRAINT pk_analytics_category_translation
PRIMARY KEY (product_category_name);

ALTER TABLE analytics.order_items
ADD CONSTRAINT pk_analytics_order_items
PRIMARY KEY (order_id, order_item_id);

ALTER TABLE analytics.payments
ADD CONSTRAINT pk_analytics_payments
PRIMARY KEY (order_id, payment_sequential);

ALTER TABLE analytics.order_reviews
ADD CONSTRAINT pk_analytics_order_reviews
PRIMARY KEY (review_record_id);

ALTER TABLE analytics.orders
ADD CONSTRAINT fk_orders_customers
FOREIGN KEY (customer_id)
REFERENCES analytics.customers (customer_id);

ALTER TABLE analytics.order_items
ADD CONSTRAINT fk_order_items_orders
FOREIGN KEY (order_id)
REFERENCES analytics.orders (order_id);

ALTER TABLE analytics.order_items
ADD CONSTRAINT fk_order_items_products
FOREIGN KEY (product_id)
REFERENCES analytics.products (product_id);

ALTER TABLE analytics.order_items
ADD CONSTRAINT fk_order_items_sellers
FOREIGN KEY (seller_id)
REFERENCES analytics.sellers (seller_id);

ALTER TABLE analytics.payments
ADD CONSTRAINT fk_payments_orders
FOREIGN KEY (order_id)
REFERENCES analytics.orders (order_id);

ALTER TABLE analytics.order_reviews
ADD CONSTRAINT fk_order_reviews_orders
FOREIGN KEY (order_id)
REFERENCES analytics.orders (order_id);