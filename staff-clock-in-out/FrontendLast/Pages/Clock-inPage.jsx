import '../App.css'
import Header from "../Components/Header"
import Content from "../Components/Content"
import TextField from "../Components/TextField"
import Animation3d from "../Components/The3dDesign"
import { useState, useEffect } from "react";
import { employeesApi } from "../services/employeesAPI";
//import ClockInPage from '../../../../Planning/src/Pages/Clock-inPage'

function ClockInPage() {
  const [employees, setEmployees] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [currentDate, setCurrentDate] = useState(''); 

  // GET CURRENT DATE ON COMPONENT MOUNT
  useEffect(() => {
    const now = new Date();
    const today = now.toISOString().split('T')[0]; // Format YYYY-MM-DD
    setCurrentDate(today);
  }, []);

  // FETCH EMPLOYEES FROM DATABASE
  useEffect(() => {
    const fetchEmployees = async () => {
      try {
        setLoading(true);
        const employeesData = await employeesApi.getEmployees();
        
        // Transform database data to match your component expectations
        const transformedEmployees = employeesData.map(emp => ({
          num: emp.emp_id || emp.id,
          name: emp.name,
          clockIn: "00:00",
          clockOut: "00:00",
          shift: 0,
          delay: "00:00",
          overtime: "00:00",
          hours: "00:00"
        }));
        
        setEmployees(transformedEmployees);
      } catch (err) {
        console.error('Error fetching employees:', err);
        setError('Failed to load employees');
        
        // Fallback to hardcoded data if API fails
        setEmployees([
          {
            num: 1,
            name: "Akram Dib",
            clockIn: "08:00",
            clockOut: "16:00",
            shift: 0,
            delay: "00:00",
            overtime: "00:00",
            hours: "00:00",
          },
          {
            num: 2,
            name: "Alaa krem",
            clockIn: "09:00",
            clockOut: "17:00",
            shift: 0,
            delay: "00:00",
            overtime: "00:00",
            hours: "00:00",
          },
        ]);
      } finally {
        setLoading(false);
      }
    };

    fetchEmployees();
  }, []);

  // ADD NEW EMPLOYEE FUNCTION
  const addNewEmployee = async () => {
    const name = prompt("Enter new employee name:");
    if (!name) return;

    try {
      const newEmployee = await employeesApi.addEmployee({ name });
      
      // Add the new employee to the state
      setEmployees(prev => [...prev, {
        num: newEmployee.id,
        name: name,
        clockIn: "00:00",
        clockOut: "00:00",
        shift: 0,
        delay: "00:00",
        overtime: "00:00",
        hours: "00:00"
      }]);
      
      alert(`Employee "${name}" added successfully!`);
    } catch (err) {
      alert('Error adding employee: ' + err.message);
    }
  };

  // DELETE EMPLOYEE FUNCTION
  const handleEmployeeDeleted = async (employeeId) => {
    try {
      await employeesApi.deleteEmployee(employeeId);
      
      // Remove employee from state
      setEmployees(prev => prev.filter(emp => emp.num !== employeeId));
      
      alert("Employee deleted successfully!");
    } catch (err) {
      alert('Error deleting employee: ' + err.message);
    }
  };

  // SAVE ALL FUNCTION (if needed)
  const saveAll = () => {
    alert('Save functionality would go here');
  };

  if (loading) {
    return <div>Loading employees...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <>
      <Header />
      {/* <Animation3d /> */}
      <TextField 
        label="Date" 
        value={currentDate} // PASSEZ LA DATE ACTUELLE
        readOnly //  RENDU LECTURE SEULE
      />
      <Content 
        employees={employees} 
        onEmployeeDeleted={handleEmployeeDeleted}
      />
      <div className='cntbtns'>
         <button className='cntbtn' onClick={addNewEmployee}>New Employee</button>
         <button className='cntbtn' onClick={saveAll}>Save</button>
      </div>
    </>
  );
}

export default ClockInPage;