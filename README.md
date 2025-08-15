# Inventory & Orders Management API

## 📌 Overview
This project implements an **Inventory and Order Management System** built with **Django REST Framework**.  
It supports **product management, suppliers, categories, stock tracking, and order processing**, including status updates and inventory history.

---

## 🚀 Features Implemented

### ✅ Orders Management
- Ability to **create new orders** with multiple products.
- Orders can be **marked as Completed** or **Canceled**.
- When completed:
  - Automatically **deducts stock** from purchased products.
  - Registers an **inventory movement** for each product (`movement_type: salida`, `reason: venta`).
- When canceled:
  - Prevents completion and keeps stock unchanged.

### ✅ Inventory System
- **InventoryMovement model** to track all stock changes:
  - `entrada` (incoming stock).
  - `salida` (stock deducted).
  - `ajuste` (manual adjustments).
- Linked to each product via `related_name="movements"`.
- **History endpoint**: `/api/products/<id>/inventory/`  
  Shows complete stock movement history for a given product.

### ✅ Products & Categories
- CRUD for products, suppliers, and categories.
- Filtering products by **category**, **price**, and **stock**.
- SKU validation to ensure uniqueness.

---

## 📂 Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/categories/` | `GET`, `POST` | List or create categories |
| `/api/products/` | `GET`, `POST` | List or create products (admin only for create) |
| `/api/products/<id>/inventory/` | `GET` | Show full inventory movement history for a product |
| `/api/orders/` | `GET`, `POST` | List orders or create a new order |
| `/api/orders/<id>/complete/` | `PATCH` | Mark an order as completed (deduct stock) |
| `/api/orders/<id>/cancel/` | `PATCH` | Cancel an order |
| `/api/suppliers/low-stock/` | `GET` | List suppliers with products under 10 units |
| `/api/reports/stock-summary/` | `GET` | Inventory summary report |

---

## 🛠 Technical Notes
- **Stock deduction** is handled in `OrderSerializer.create()` using `F()` expressions to ensure atomic updates.
- **InventoryMovement** is automatically created when orders are completed.
- Custom **actions** (`@action`) are used in the `OrderViewSet` to handle order completion and cancellation.
- **Prefetch** is used in `ProductViewSet.inventory` to optimize history queries.

---

## 🧪 Testing Performed
- Created orders with multiple products to verify:
  - Stock deduction on completion.
  - Prevention of completion if stock is insufficient.
- Canceled orders to ensure stock remains unchanged.
- Viewed product inventory history to confirm all movements are logged.
- Checked low-stock supplier report.

---
