

# Payroll Module

## Overview
This Payroll Module is designedto automate salary calculations. It receives attendance data for each employee from the [staff clock-in-out module](https://github.com/nexopizza/hack-n-slice-constantine-2025/tree/main/staff-clock-in-out) and computes salaries based on multiple factors including salary rate, hours worked, employee loans, and salary advances.

---

## Features
- Integration with clock-in module for attendance tracking
- Salary calculation based on:
  - Hourly rate
  - Total hours worked
  - Employee loans
  - Salary advances
  - Staff meal deduction
- Modular and scalable design
- Easy to integrate with other HR systems

---

## Inputs
- Attendance data from clock-in module
- Employee salary rate
- Employee loan details
- Salary advances
- Staff meal deduction

### Sample
```json
{
  "period": { "start": "2025-08-01", "end": "2025-08-31" },
  "employees": [
    { "employee_id": "0001", "total_hours": 80.0 },
    { "employee_id": "0002", "total_hoiurs": 56.30}
  ]
}
```

## Outputs
- Calculated salary for each employee
- Salary breakdown report
- Loan and advance deductions
- Net salary for each employee

### Sample
```json

[
    {
        "employee_id": "0001",
        "name": "Abbass",
        "total_hours": 208,
        "hourly_rate": 145,
        "gross_salary": 30000,
        "deductions": {
            "loan": 5000,
            "advance": 800,
            "meal_consumption": 200
        },
        "net_salary": 24000
    },
    {
        "employee_id": "0002",
        "name": "Faris",
        "total_hours": 190,
        "hourly_rate": 200,
        "gross_salary": 30000,
        "deductions": {
            "loan": 1000,
            "advance": 3000,
            "meal_consumption": 1000
        },
        "net_salary": 22550
    }
]
```




