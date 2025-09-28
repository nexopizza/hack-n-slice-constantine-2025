import { useState, useEffect } from "react";
import Header from "../Components/Header"
import TextField from "../Components/TextField"
import ReportingContent from "../Components/ReportingContent"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPrint } from "@fortawesome/free-solid-svg-icons";
import { worktimeApi } from "../services/worktimeAPI";
import { employeesApi } from "../services/employeesAPI";

export default function Reporting(){
  const [employees, setEmployees] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedDate, setSelectedDate] = useState(new Date().toISOString().split('T')[0]);

  // Fetch worktime records for selected date
  const fetchWorktimeRecords = async (date) => {
    try {
      setLoading(true);
      setError(null);
      
      console.log('Fetching data for date:', date);
      const worktimeData = await worktimeApi.getWorkTimesByDate(date);
      console.log('Raw worktime data:', worktimeData);
      
      // Transform worktime data
      const transformedEmployees = worktimeData.map(record => {
        console.log('Processing record:', record);
        console.log('late_minutes type:', typeof record.late_minutes, 'value:', record.late_minutes);
        console.log('overtime_minutes type:', typeof record.overtime_minutes, 'value:', record.overtime_minutes);
        console.log('work_hours type:', typeof record.work_hours, 'value:', record.work_hours);
        
        return {
          num: record.emp_id,
          name: record.emp_name || `Employee ${record.emp_id}`,
          shift: record.shift_id || 0,
          delay: formatMinutesToTime(record.late_minutes || 0),
          overtime: formatMinutesToTime(record.overtime_minutes || 0),
          hours: formatHoursToTime(record.work_hours || 0)
        };
      });
      
      console.log('Transformed employees:', transformedEmployees);
      setEmployees(transformedEmployees);
      
    } catch (err) {
      console.error('Error fetching worktime records:', err);
      setError('No worktime records found for selected date');
      
      // Fallback: show all employees with placeholder data
      try {
        const employeesData = await employeesApi.getEmployees();
        const fallbackEmployees = employeesData.map(emp => ({
          num: emp.emp_id || emp.id,
          name: emp.name,
          clockIn: "--:--",
          clockOut: "--:--",
          shift: 0,
          delay: "00:00",
          overtime: "00:00",
          hours: "00:00",
          note: "No worktime record for this date"
        }));
        setEmployees(fallbackEmployees);
      } catch (fallbackErr) {
        setEmployees([]);
      }
    } finally {
      setLoading(false);
    }
  };

  // Helper function to convert string to number safely
  const safeParseNumber = (value) => {
    if (value === null || value === undefined || value === '') return 0;
    
    // If it's already a number, return it
    if (typeof value === 'number') return value;
    
    // If it's a string, try to parse it
    if (typeof value === 'string') {
      const parsed = parseFloat(value);
      return isNaN(parsed) ? 0 : parsed;
    }
    
    return 0;
  };

  // Helper function to format minutes as HH:MM - HANDLES STRINGS
  const formatMinutesToTime = (minutes) => {
    const minutesNumber = safeParseNumber(minutes);
    console.log('Formatting minutes:', minutes, 'as number:', minutesNumber);
    
    if (minutesNumber === 0) return "00:00";
    
    const hours = Math.floor(minutesNumber / 60);
    const mins = minutesNumber % 60;
    return `${hours.toString().padStart(2, '0')}:${mins.toString().padStart(2, '0')}`;
  };

  // Helper function to format hours as HH:MM - HANDLES STRINGS
  const formatHoursToTime = (hours) => {
    const hoursNumber = safeParseNumber(hours);
    console.log('Formatting hours:', hours, 'as number:', hoursNumber);
    
    if (hoursNumber === 0) return "00:00";
    
    const wholeHours = Math.floor(hoursNumber);
    const minutes = Math.round((hoursNumber - wholeHours) * 60);
    return `${wholeHours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}`;
  };

  // Handle date change
  const handleDateChange = (event) => {
    const newDate = event.target.value;
    setSelectedDate(newDate);
  };

  // Fetch data when component mounts or date changes
  useEffect(() => {
    fetchWorktimeRecords(selectedDate);
  }, [selectedDate]);

  if (loading) {
    return (
      <>
        <Header />
        <div style={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          height: "50vh"
        }}>
          <div>Loading worktime records for {selectedDate}...</div>
        </div>
      </>
    );
  }

  return (
    <>
      <Header />
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          alignItems: "center",
          height: "30vh",
        }}
      >
        <div
          style={{
            background: "linear-gradient(to right, #EB4219, #F6892A)",
            WebkitBackgroundClip: "text",
            WebkitTextFillColor: "transparent",
            fontSize: "20px",
            marginBottom: "2px",
          }}
        >
          Date Filter
        </div>

        <div
          style={{
            color: "black",
            fontSize: "14px",
            marginBottom: "3px",
          }}
        >
          Search about records by selected date
        </div>

        <TextField 
          label="Date" 
          type="date"
          value={selectedDate}
          onChange={handleDateChange}
        />
      </div>

      {error && (
        <div style={{
          color: "orange",
          textAlign: "center",
          margin: "10px 0",
          fontSize: "14px"
        }}>
          {error}
        </div>
      )}

      <div
        style={{
          display: "flex",
          justifyContent: "flex-start",
          alignItems: "center",
          color: "black",
          fontSize: "20px",
          marginLeft: "35px",
          marginTop: "10px",
          marginBottom: "0px"
        }}
      >
        {selectedDate} records:
      </div>
      
      <ReportingContent employees={employees} />
      
      <div className='cntbtns'>
        <FontAwesomeIcon icon={faPrint} style={{ marginRight: "8px" }} />
        <button className='cntbtn'>Print</button>
      </div>
    </>
  );
}