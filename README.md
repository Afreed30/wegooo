🚍 WEGOOO – Smart Bus Booking System

A modern full-stack bus reservation platform with seat selection, secure payments, booking history, authentication, and premium UI.

<p align="center"> <img src="https://img.shields.io/badge/WEGOOO%20BUS-v1.0-blue?style=for-the-badge"/> <img src="https://img.shields.io/badge/React-Frontend-61DBFB?style=for-the-badge&logo=react&logoColor=black"/> <img src="https://img.shields.io/badge/Django%20REST-Backend-092E20?style=for-the-badge&logo=django&logoColor=white"/> <img src="https://img.shields.io/badge/Razorpay-Payments-4C4CFF?style=for-the-badge&logo=razorpay&logoColor=white"/> </p>
✨ About WEGOOO

WEGOOO is a complete bus ticket reservation system featuring:

✔ Bus Search
✔ Seat Selection
✔ User Authentication
✔ Razorpay Payment Gateway
✔ Ticket PDF Generation
✔ Booking Management
✔ Fully Responsive UI

Ideal for learning, academic projects, or production-level development.

🌟 Features
🧑‍💼 Authentication

Register, Login, Logout

Token-based Authentication

Protected Routes

🚌 Bus Search

Search by source, destination, travel date

View bus details, price, availability

💺 Seat Selection

Real-time seat map

Occupied vs Available seats

Visual UI with animations

💳 Payments (Razorpay)

Order creation

Razorpay checkout

Payment verification

Secure backend confirmation

🎫 Bookings & Tickets

View booking history

Ticket ID, bus details, seat number, passenger details

Download Ticket PDF

🎨 Modern UI

Attractive Login / Register

Smooth Animations

Vite + React + Custom CSS

🖼 Screenshots

(Replace with your own screenshots)

🔐 Login Page

🚍 Bus Search

💺 Seat Selection

🧾 Booking Summary

🛠 Tech Stack
Frontend

React.js

Vite

React Router

Tailwind / Pure CSS

Razorpay Checkout.js

Backend

Django

Django REST Framework

Token Authentication

Razorpay Orders API

Database

SQLite / MySQL / PostgreSQL

⚙️ Installation Guide
📌 Clone Project
git clone https://github.com/YOUR_USERNAME/wegooo-bus.git
cd wegooo-bus

🔧 Backend Setup (Django)
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver


Configure Razorpay in settings.py:

RAZORPAY_KEY_ID = "your_key"
RAZORPAY_KEY_SECRET = "your_secret"


Add CORS:

INSTALLED_APPS += ["corsheaders"]

MIDDLEWARE = ["corsheaders.middleware.CorsMiddleware", *MIDDLEWARE]

CORS_ALLOW_ALL_ORIGINS = True

💻 Frontend Setup (React)
cd frontend
npm install
npm run dev


Configure API Base URL:

Create .env:

VITE_API_BASE_URL=http://127.0.0.1:8000/api


Use in code:

export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

🔌 API Endpoints
Auth Endpoints
Method	URL	Description
POST	/api/register/	Create account
POST	/api/login/	Login user
POST	/api/logout/	Logout
Bus Search

| GET | /api/search-buses/?origin=A&destination=B&travel_date=2025-03-10 |

Seats

| GET | /api/schedules/:id/seats/ |

Bookings

| GET | /api/bookings/ |
| POST | /api/bookings/ |

Payments

| POST | /api/create-payment-order/ |
| POST | /api/verify-payment/ |

🗂 Folder Structure
WEGOOO/
│
├── backend/
│   ├── api/
│   ├── bus/
│   ├── settings.py
│   └── manage.py
│
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   ├── components/
│   │   ├── api.js
│   │   └── App.jsx
│   ├── index.html
│   └── vite.config.js
│
└── README.md

🚀 Deployment Guide
🟩 Deploy Backend (Django) on Render
1️⃣ Create Web Service

Login to https://render.com

New → Web Service

Connect GitHub repo

Select backend folder

2️⃣ Build Command
pip install -r requirements.txt

3️⃣ Start Command
gunicorn backend.wsgi:application

4️⃣ Environment Variables

Add in Render → Environment:

SECRET_KEY=your_secret
DEBUG=False
ALLOWED_HOSTS=yourapp.onrender.com
RAZORPAY_KEY_ID=
RAZORPAY_KEY_SECRET=
CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app

🟦 Deploy Frontend (React) on Vercel
1️⃣ Push frontend to GitHub
2️⃣ Import Project in Vercel

Vercel auto detects Vite.

Build Settings:
Build Command: npm run build
Output Directory: dist

3️⃣ Add Environment Variable:
VITE_API_BASE_URL=https://your-backend.onrender.com/api

🟧 Razorpay Production Setup
Replace test keys with live keys:

Backend:

RAZORPAY_KEY_ID=live_key
RAZORPAY_KEY_SECRET=live_secret


Frontend:

key: "LIVE_KEY_ID"


Enable Allowed Origins in Razorpay Dashboard:

https://your-frontend.vercel.app

❗ Common Deployment Issues
🔥 CORS error

Fix with:

CORS_ALLOWED_ORIGINS = [
    "https://your-frontend.vercel.app"
]

🔥 500 Internal Server Error

Missing Razorpay keys.

🔥 404 API Not Found

Check VITE_API_BASE_URL.

🔥 White screen on Vercel

Wrong build paths → ensure output directory is dist.

❤️ Credits

Developed by:

Afreed Shaik

💼 Full Stack Python Developer
🌐 GitHub: https://github.com/Afreed30
