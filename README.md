# 🛍️ UsedShop - Multi-Vendor E-commerce Platform

**UsedShop** is a full-stack multi-vendor e-commerce platform where multiple sellers can register, list their used products, and buyers can browse/filter available items. The project is built with **Django (Backend)** and **React (Frontend)**, and deployed on **Render**.

---

## 🚀 Features

### 👥 User Roles
- **Sellers**: Can register, login, edit their profile, and manage their own products.
- **Admins**: Can register and manage seller accounts and oversee product listings.

### 📦 Products
- Sellers can:
  - Add new products with multiple images
  - Edit or delete their own products
- Products are displayed by:
  - Category
  - Seller-specific listings
  - Search & filter

### 🔐 Authentication
- Custom login system for sellers and admins
- JWT-based protection for APIs
- Session-based navigation between user roles

### 🌐 Deployment
- Backend: Render + Gunicorn
- Frontend: React (Vite or CRA) hosted on Render Static Site
- Media: Supports image upload (with support for future Cloudinary integration)

---

## 🧱 Tech Stack

| Layer     | Technology          |
|-----------|---------------------|
| Frontend  | React, Axios        |
| Backend   | Django, DRF, JWT    |
| Database  | postgresql          |
| Hosting   | Render              |
| Media     | Local + Cloud-ready |
| Auth      | Custom (JWT-based)  |



