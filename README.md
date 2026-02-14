# 💰 AI Financial Advisor for Rural India

> An AI‑powered financial literacy and planning platform designed specifically for rural India — providing bilingual guidance, government scheme discovery, and simple budget planning without requiring digital literacy.

---

## 🌐 Live Demo

👉 [https://nimble-snickerdoodle-47acf2.netlify.app/](https://nimble-snickerdoodle-47acf2.netlify.app/)

---

## 🎯 Purpose

Millions of rural households in India lack access to financial advisors and struggle to understand government schemes, savings strategies, and loan decisions.

This project solves that by providing a **simple, mobile‑friendly, Hindi‑first financial assistant** that works even on slow internet and low‑end devices.

---

## ✨ Key Features

### 🧠 Smart Financial Analysis

* Financial Health Score (0–100)
* Debt‑to‑Income evaluation
* Emergency fund readiness
* Savings ratio calculation

### 🪙 Personalized Advice

* Priority‑based recommendations (High / Medium / Low)
* Tailored to occupation (farmer, laborer, small business, etc.)
* Rural‑friendly budgeting system

### 🏛️ Government Scheme Discovery

* PM Jan Dhan Yojana
* PM Jeevan Jyoti Bima Yojana (₹330/year)
* PM Suraksha Bima Yojana (₹12/year)
* Atal Pension Yojana
* Kisan Credit Card
* MUDRA Loan

### 📊 Budget Planning

Modified rural budgeting rule:

* Needs → 60%
* Wants → 20%
* Savings → 20%

### 🤖 AI Chatbot

Ask financial questions in Hindi or English:

* Loan guidance
* Insurance advice
* Savings suggestions
* Scheme eligibility

### 🌍 Accessibility

* Hindi + English bilingual interface
* Works offline (fallback calculations)
* Mobile‑first responsive design
* Optimized for 2G/3G networks
* No login required

---

## 👥 Target Users

* Farmers
* Daily wage workers
* Small shop owners
* Self‑employed individuals
* Rural families
* First‑time bank users

---

## 📥 User Input Parameters

| Field            | Description                 |
| ---------------- | --------------------------- |
| Monthly Income   | Total monthly earnings (₹)  |
| Monthly Expenses | Household monthly spending  |
| Savings          | Current stored money        |
| Debt             | Outstanding loans           |
| Family Size      | Dependents count            |
| Age              | User age                    |
| Occupation       | Farmer / Laborer / Business |
| Bank Account     | Yes / No                    |

---

## 📤 System Output

### 1. Financial Health Score

| Score  | Meaning   |
| ------ | --------- |
| 0–40   | High Risk |
| 40–70  | Moderate  |
| 70–100 | Healthy   |

### 2. Recommendations

* Critical actions (bank account, debt reduction)
* Insurance suggestions
* Long‑term investment ideas

### 3. Savings Goals

* Emergency fund (6 months expenses)
* Education fund (~₹2 lakh)
* Retirement (~₹5 lakh)

---

## 🏗️ Tech Stack

### Backend

* Python Flask
* Flask‑CORS
* Gunicorn

### Frontend

* HTML5
* CSS3 (responsive Indian theme)
* Vanilla JavaScript
* Font Awesome

### Architecture Highlights

* No database required
* Privacy‑first (no personal data stored)
* Client‑side fallback calculations
* REST API based design

---

## 📂 Project Structure

```
AI-Financial-Advisor-Rural-India/
│
├── backend/
│   ├── app.py
│   └── requirements.txt
│
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── script.js
│
├── data/
│   └── schemes.json
│
├── Procfile
├── README.md
└── .gitignore
```

---

## 🔌 API Endpoints

### Health Check

```
GET /api/health
```

### Financial Analysis

```
POST /api/analyze
Content-Type: application/json
```

Example Request:

```
{
  "monthly_income": 15000,
  "monthly_expenses": 10000,
  "savings": 5000,
  "debt": 0,
  "family_size": 4,
  "age": 35,
  "occupation": "farmer",
  "has_bank_account": true
}
```

### Chatbot

```
POST /api/chat
```

Example:

```
{
  "message": "मुझे loan चाहिए"
}
```

---

## 🚀 Deployment Guide

### Option 1 — Instant Frontend Deploy (Recommended)

1. Go to Netlify Drop
2. Drag `frontend` folder
3. Done 🎉

Works even without backend using fallback calculations.

---

### Option 2 — Full Stack Deploy (Render)

1. Push project to GitHub
2. Connect backend to Render
3. Update API URL in `script.js`
4. Deploy frontend on Netlify

---

### Option 3 — Heroku

```
git push heroku main
```

---

## 🔐 Privacy & Security

* No user registration
* No personal data stored
* No tracking
* Offline capable calculations
* HTTPS recommended in production

---

## 📚 Educational Concepts Explained

* Emergency Fund
* Savings Rate
* Debt‑to‑Income Ratio
* Basic Insurance Planning
* Pension Awareness

---

## 🧪 Sample Output Scenarios

### Farmer

Income ₹10,000 | Expenses ₹8,000
→ Score: 65
→ Suggestion: Kisan Credit Card

### Worker with Debt

Income ₹12,000 | Debt ₹50,000
→ Score: 35
→ Suggestion: Debt repayment + PM Jan Dhan

---

## 🛣️ Future Improvements (Roadmap)

* Voice input for illiterate users
* Regional language expansion (Bengali, Marathi, Tamil)
* Offline PWA installable app
* WhatsApp bot integration
* Crop‑based income prediction

---

## 🤝 Contributing

1. Fork repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Open Pull Request

---

## 📄 License

MIT License — free for personal & commercial use

---

## 👨‍💻 Author
**Rupam Mukherjee**
- GitHub: [@Rupam179](https://github.com/Rupam179)
- LinkedIn: [Rupam Mukherjee](https://www.linkedin.com/in/rupam-mukherjee-647a092b0/)
- Email: mukherjeerupam14@gmail.com

---

## ❤️ Mission

Empowering financial literacy for Bharat’s villages using simple AI.

**Made in India**
