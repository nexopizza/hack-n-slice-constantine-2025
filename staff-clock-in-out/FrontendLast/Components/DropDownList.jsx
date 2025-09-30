import { useState, useEffect } from "react";

export default function DropDownList({ employees, onSelect, selectedEmployee }) {
    const [selectedEmployeeName, setSelectedEmployeeName] = useState("");

    // Update selected employee when prop changes
    useEffect(() => {
        if (selectedEmployee) {
            setSelectedEmployeeName(selectedEmployee.name);
        } else {
            setSelectedEmployeeName("");
        }
    }, [selectedEmployee]);

    const handleChange = (e) => {
        const selectedName = e.target.value;
        setSelectedEmployeeName(selectedName);
        
        const employee = employees.find(emp => emp.name === selectedName);
        
        // Call the onSelect callback with the employee data
        if (onSelect) {
            onSelect(employee);
        }
    };

    return (
        <select value={selectedEmployeeName} onChange={handleChange}>
            <option value="">Select Employee</option>
            {employees.map((employee, index) => (
                <option key={index} value={employee.name}>
                    {employee.name}
                </option>
            ))}
        </select>
    );
}