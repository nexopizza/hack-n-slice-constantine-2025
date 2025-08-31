# ⏱️ Staff Clock-In & Out (Lite)

## 🎯 Project Objective
A minimal time tracker for team members to clock in/out and compute basic daily/weekly/monthly hours, with a simple export for payroll.

---

## 🧩 Minimal Features

- Clock in and clock out
- See today’s status and totals (day/week/month)
- Send data to [payroll module](https://github.com/nexopizza/hack-n-slice-constantine-2025/tree/main/payroll-module)

---

## 🧪 Sample Data

### Punch Event
```json
{
    "employee_id":"E001",
    "name":"Alice",
    "date":"2025-08-25",
    "clock_in":"09:00",
    "clock_out":"18:00",
    "total_hours":9.0
},
```

### Daily Summary
```json
{
  "employee_id": "emp_00123",
  "date": "2025-08-29",
  "punches": [
    { "in": "2025-08-29T09:00:00Z", "out": "2025-08-29T13:00:00Z" },
    { "in": "2025-08-29T14:00:00Z", "out": "2025-08-29T18:00:00Z" }
  ],
  "break": { "start": "2025-08-29T13:00:00Z", "end": "2025-08-29T14:00:00Z" },
  "worked_hours": 8.0
}
```

### Payroll Export (very simple)
```json
{
  "period": { "start": "2025-08-01", "end": "2025-08-31" },
  "employees": [
    { "employee_id": "0001", "total_hours": 80.0 },
    { "employee_id": "0002", "total_hoiurs": 56.30}
  ]
}
```

---

## 🧠 Suggested Approach (Lite)

1. Data model: Punch, DailySummary, PayPeriodTotals
2. Endpoints: create punch, list punches, compute summaries, export totals
3. UI: simple page with one button (in/out toggle) and an optional break button
4. Keep times in UTC; assume shifts end the same day

---

## 🛠️ Suggested Tech Stack

- Language: [TypeScript]
- Frontend: [React v19], [React Router v7], [MUI v7]
- Backend: [NestJS v11]
- Database: [MongoDB] with [Mongoose]
- Deployment: [Vercel]

---

[React v19]: https://react.dev/
[React Router v7]: https://reactrouter.com/
[MUI v7]: https://mui.com/
[NestJS v11]: https://nestjs.com/
[MongoDB]: https://www.mongodb.com/
[Mongoose]: https://mongoosejs.com/
[Vercel]: https://vercel.com/
[TypeScript]: https://www.typescriptlang.org/
