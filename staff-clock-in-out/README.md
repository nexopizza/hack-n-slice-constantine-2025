# ⏱️ Staff Clock-In & Out

## 🎯 Project Objective
Provide a simple, reliable timekeeping system for Nexo Pizza team members to clock in/out and track breaks. Automatically compute daily, weekly, and monthly hours with overtime rules, and export approved timesheets to the payroll module.

---

## 🧩 Functional Requirements

### 1. 👋 Clocking Actions
- Clock in, clock out, break start, break end
- Prevent duplicate/misordered punches; handle missed punches with supervisor correction + reason
- Kiosk-friendly web UI (PIN/QR), touch-first, fast feedback
- Optional device lock or geofencing; basic offline queue with automatic sync

### 2. 👥 Employee & Roles
- Create employees with role, site/location, base pay rate, and schedule
- Role-based permissions: employee, supervisor/manager, admin
- Minimal PII; store only necessary identifiers

### 3. 🧮 Timesheet Calculation
- Totals by day/week/pay period (regular, overtime, unpaid/paid breaks)
- Overtime rules (e.g., >8h/day or >40h/week), rounding (e.g., 5/10/15-min), grace periods
- Cross-midnight shifts, time zone consistency, partial-day handling

### 4. ✅ Review & Approval
- Supervisor review of edits and exceptions (missed punches, long breaks)
- Audit trail of manual adjustments (who, when, why)
- Lock approved periods to prevent further changes

### 5. 💸 Payroll Export
- Generate export for `payroll-module` (JSON) and optional CSV
- Include per-employee totals per period (regular, OT, breaks) with metadata

### 6. 📊 Dashboard & Reports
- Who’s currently on shift, late/missed punches, daily/weekly totals
- Filter by location/role/date; export to CSV

### 7. 🔐 Security & Compliance
- Authentication and role-based authorization
- Protect sensitive data; avoid storing raw biometric data
- Retain audit logs for changes and approvals

---

## 🛠️ Suggested Tech Stack

- Frontend: [React v19], [React Router v7], [MUI v7]
- Backend: [NestJS v11]
- Database: [MongoDB] with [Mongoose]
- Deployment: [Vercel]
- Authentication: [Firebase]
- Error tracking: [Sentry]

---

## 🧪 Sample Data Format

### Punch Event (MongoDB document)
```json
{
  "_id": "6793fca2ea7a02f9a40b1a11",
  "employee_id": "emp_00123",
  "site_id": "store_el_khroub",
  "device_id": "kiosk-01",
  "action": "clock_in",
  "timestamp": "2025-08-29T08:57:12Z",
  "source": "kiosk",
  "method": "pin",
  "geo": { "lat": 36.253, "lng": 6.693 },
  "notes": null,
  "created_by": "emp_00123",
  "verified": true,
  "version": 1
}
```

### Timesheet Summary (per day)
```json
{
  "employee_id": "emp_00123",
  "date": "2025-08-29",
  "site_id": "store_el_khroub",
  "punches": [
    { "in": "2025-08-29T09:00:00Z", "out": "2025-08-29T13:00:00Z" },
    { "in": "2025-08-29T14:00:00Z", "out": "2025-08-29T18:30:00Z" }
  ],
  "breaks": [
    { "start": "2025-08-29T13:00:00Z", "end": "2025-08-29T14:00:00Z", "paid": false }
  ],
  "totals": {
    "worked_hours": 8.5,
    "regular_hours": 8.0,
    "overtime_hours": 0.5,
    "unpaid_break_hours": 1.0
  },
  "exceptions": ["overtime"],
  "status": "pending_review"
}
```

### Payroll Export (per pay period)
```json
{
  "period": { "start": "2025-08-18", "end": "2025-08-31" },
  "site_id": "store_el_khroub",
  "generated_at": "2025-09-01T06:00:00Z",
  "employees": [
    {
      "employee_id": "emp_00123",
      "regular_hours": 72.0,
      "overtime_hours": 6.5,
      "unpaid_break_hours": 10.0,
      "notes": ["2 missed-punch corrections approved"],
      "locked": true
    }
  ]
}
```

---

## 🧠 Suggested Approach

### Step-by-Step Guide
1. Define data models: Punch, TimesheetDay, PayPeriod, Employee, Approval
2. Build API endpoints for punch create/list, timesheet compute, approve/lock, export
3. Implement kiosk UI: PIN/QR login, 1-tap punch, error/duplicate prevention
4. Add authentication/authorization and audit logging
5. Implement calculation engine: rounding, overtime, cross-midnight handling
6. Add exceptions workflow and supervisor approvals
7. Generate payroll exports and basic reports/dashboard

---

## 🎓 Learning Objectives
- Design and implement timekeeping workflows end-to-end
- Build a calculation engine with rounding and overtime rules
- Apply secure auth, RBAC, and audit trails
- Produce operational dashboards and compliant exports

---

## 💡 Optional Enhancements
- Face/QR verification, geofencing, and device binding
- Offline-first kiosk with background sync and conflict resolution
- Shift scheduling, tardiness alerts, and PTO/leave requests
- Multi-location rollups and anomaly detection (time theft, duplicate devices)

---

[React v19]: https://react.dev/
[React Router v7]: https://reactrouter.com/
[MUI v7]: https://mui.com/
[NestJS v11]: https://nestjs.com/
[MongoDB]: https://www.mongodb.com/
[Mongoose]: https://mongoosejs.com/
[Vercel]: https://vercel.com/
[Firebase]: https://firebase.google.com/
[Sentry]: https://sentry.io/
