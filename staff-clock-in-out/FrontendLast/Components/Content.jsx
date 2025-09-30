import { useState } from "react";
import { worktimeApi } from "../services/worktimeAPI";


export default function Content({ employees, onEmployeeDeleted }) { 
  const shiftTimes = {
    1: { start: "06:00", end: "14:00" }, 
    2: { start: "08:00", end: "16:00" }, 
    3: { start: "16:00", end: "00:00" }  
  };

  // State for selected shifts
  const [selectedShifts, setSelectedShifts] = useState(() => {
    const initialShifts = {};
    employees.forEach(emp => {
      initialShifts[emp.num] = ""; // Initialize with no selection
    });
    return initialShifts;
  });

  // Calculate if employee is late
  const calculateLateMinutes = (clockIn, shiftNumber) => {
    if (clockIn === "00:00" || !shiftNumber || !shiftTimes[shiftNumber]) {
      return 0;
    }

    const shiftStart = shiftTimes[shiftNumber].start;
    const [clockInHours, clockInMinutes] = clockIn.split(':').map(Number);
    const [shiftStartHours, shiftStartMinutes] = shiftStart.split(':').map(Number);

    const clockInTotalMinutes = clockInHours * 60 + clockInMinutes;
    const shiftStartTotalMinutes = shiftStartHours * 60 + shiftStartMinutes;

    // Handle overnight shifts (shift 3)
    let lateMinutes = clockInTotalMinutes - shiftStartTotalMinutes;
    
    // For shift 3 (16:00-00:00), if clock in is after midnight, adjust calculation
    if (shiftNumber === 3 && clockInHours < 12) { 
      lateMinutes = (clockInTotalMinutes + (24 * 60)) - shiftStartTotalMinutes;
    }

    return lateMinutes > 0 ? lateMinutes : 0; // Return 0 if not late
  };

  // Calculate overtime
  const calculateOvertimeMinutes = (clockOut, shiftNumber) => {
    if (clockOut === "00:00" || !shiftNumber || !shiftTimes[shiftNumber]) {
      return 0;
    }

    const shiftEnd = shiftTimes[shiftNumber].end;
    const [clockOutHours, clockOutMinutes] = clockOut.split(':').map(Number);
    const [shiftEndHours, shiftEndMinutes] = shiftEnd.split(':').map(Number);

    const clockOutTotalMinutes = clockOutHours * 60 + clockOutMinutes;
    let shiftEndTotalMinutes = shiftEndHours * 60 + shiftEndMinutes;

    // Handle overnight shifts (shift 3 ends at 00:00 which is 24:00)
    if (shiftNumber === 3 && shiftEndTotalMinutes === 0) {
      shiftEndTotalMinutes = 24 * 60; // 00:00 = 24:00
    }

    const overtimeMinutes = clockOutTotalMinutes - shiftEndTotalMinutes;
    return overtimeMinutes > 0 ? overtimeMinutes : 0;
  };

  // Format minutes to HH:MM
  const formatMinutesToTime = (totalMinutes) => {
    if (totalMinutes <= 0) return "00:00";
    const hours = Math.floor(totalMinutes / 60);
    const minutes = totalMinutes % 60;
    return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}`;
  };

  // Calculate hours worked
  const calculateHours = (clockIn, clockOut) => {
    if (clockIn === "00:00" || clockOut === "00:00") {
      return "00:00";
    }
    
    const [inHours, inMinutes] = clockIn.split(':').map(Number);
    const [outHours, outMinutes] = clockOut.split(':').map(Number);
    
    const totalInMinutes = inHours * 60 + inMinutes;
    const totalOutMinutes = outHours * 60 + outMinutes;
    
    let diffMinutes = totalOutMinutes - totalInMinutes;

    // Handle overnight shifts
    if (diffMinutes < 0) {
      diffMinutes += 24 * 60;
    }
    
    const hours = Math.floor(diffMinutes / 60);
    const minutes = diffMinutes % 60;
    
    return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}`;
  };

  // Initialize state with "00:00" for all employees
  const [employeeTimes, setEmployeeTimes] = useState(() => {
    const initialTimes = {};
    employees.forEach(emp => {
      initialTimes[emp.num] = {
        clockIn: "00:00",
        clockOut: "00:00",
        workTimeId: null
      };
    });
    return initialTimes;
  });


  
  // Function to get current time in HH:MM format
  const getCurrentTime = () => {
    const now = new Date();
    const hours = now.getHours().toString().padStart(2, '0');
    const minutes = now.getMinutes().toString().padStart(2, '0');
    return `${hours}:${minutes}`;
  };

  // Function to get current date in YYYY-MM-DD format
  const getCurrentDate = () => {
    const now = new Date();
    return now.toISOString().split('T')[0];
  };

  // Handle shift selection
  const handleShiftChange = (employeeNum, shiftValue) => {
    setSelectedShifts(prev => ({
      ...prev,
      [employeeNum]: shiftValue
    }));
  };

  // Save work time to database
  const saveWorkTimeToDB = async (employeeNum, clockIn, clockOut) => {
    try {
      const shiftNumber = parseInt(selectedShifts[employeeNum]);
      const lateMinutes = calculateLateMinutes(clockIn, shiftNumber);
      const overtimeMinutes = calculateOvertimeMinutes(clockOut, shiftNumber);
      const timeOfWork = calculateHours(clockIn, clockOut);
      
      const workTimeData = {
        employeeId: employeeNum,
        date: getCurrentDate(),
        clockIn: clockIn,
        clockOut: clockOut,
        timeOfWork: timeOfWork,
        shift: shiftNumber || 0,
        delay: formatMinutesToTime(lateMinutes),
        overtime: formatMinutesToTime(overtimeMinutes),
        late_minutes: lateMinutes
      };

      const savedWorkTime = await worktimeApi.saveWorkTime(workTimeData);
      
      setEmployeeTimes(prev => ({
        ...prev,
        [employeeNum]: {
          ...prev[employeeNum],
          workTimeId: savedWorkTime.id
        }
      }));

      console.log('Work time saved successfully:', savedWorkTime);
      return savedWorkTime;
    } catch (error) {
      console.error('Error saving work time:', error);
      alert('Error saving work time to database');
    }
  };

  // Handle clock in
  const handleClockIn = (employeeNum) => {
    const currentTime = getCurrentTime();
    const updatedTimes = {
      ...employeeTimes[employeeNum],
      clockIn: currentTime
    };
    
    setEmployeeTimes(prev => ({
      ...prev,
      [employeeNum]: updatedTimes
    }));

    if (updatedTimes.clockOut !== "00:00") {
      saveWorkTimeToDB(employeeNum, currentTime, updatedTimes.clockOut);
    }
  };

  // Handle clock out
  const handleClockOut = (employeeNum) => {
    const currentTime = getCurrentTime();
    const updatedTimes = {
      ...employeeTimes[employeeNum],
      clockOut: currentTime
    };
    
    setEmployeeTimes(prev => ({
      ...prev,
      [employeeNum]: updatedTimes
    }));

    if (updatedTimes.clockIn !== "00:00") {
      saveWorkTimeToDB(employeeNum, updatedTimes.clockIn, currentTime);
    }
  };

  // Get current time for an employee
  const getEmployeeTime = (employeeNum, type) => {
    return employeeTimes[employeeNum]?.[type] || "00:00";
  };

  // Get display values for delay and overtime
  const getDisplayDelay = (employeeNum) => {
    const clockIn = getEmployeeTime(employeeNum, 'clockIn');
    const shiftNumber = parseInt(selectedShifts[employeeNum]);
    const lateMinutes = calculateLateMinutes(clockIn, shiftNumber);
    return formatMinutesToTime(lateMinutes);
  };

  const getDisplayOvertime = (employeeNum) => {
    const clockOut = getEmployeeTime(employeeNum, 'clockOut');
    const shiftNumber = parseInt(selectedShifts[employeeNum]);
    const overtimeMinutes = calculateOvertimeMinutes(clockOut, shiftNumber);
    return formatMinutesToTime(overtimeMinutes);
  };

  return (
    <>
        <div
            style={{
                display: "flex",
                justifyContent: "flex-start",
                alignItems: "center",
                color: "black",
                fontSize: "20px",
                marginLeft:"35px",
                marginTop: "40px",
                marginBottom: "0px"
            }}
        >
            Enter clock in/out and shift number: 
        </div>

        <div>
        <table border="1" cellPadding="20" cellSpacing="0">
            <thead>
            <tr>
                <th>Num</th>
                <th>Full name</th>
                <th>Clock in</th>
                <th>Clock out</th>
                <th>Shift number</th>
                <th>Delay</th>
                <th>Overtime</th>
                <th>Hours</th>
                <th>Operations</th>
            </tr>
            </thead>
            <tbody>
            {employees.map((emp) => {
              const currentClockIn = getEmployeeTime(emp.num, 'clockIn');
              const currentClockOut = getEmployeeTime(emp.num, 'clockOut');
              const currentDelay = getDisplayDelay(emp.num);
              const currentOvertime = getDisplayOvertime(emp.num);
              
              return (
                <tr key={emp.num}>
                <td>{emp.num}</td>
                <td>{emp.name}</td>
                <td>
                  <button 
                    className="time-button"
                    onClick={() => handleClockIn(emp.num)}
                    style={{
                      background: currentClockIn === "00:00" ? '#6c757d' : '#28a745',
                      color: 'white',
                      border: 'none',
                      padding: '8px 12px',
                      borderRadius: '4px',
                      cursor: 'pointer',
                      fontSize: '14px',
                      width: '100%'
                    }}
                  >
                    Clock In<br/>{currentClockIn}
                  </button>
                </td>
                <td>
                  <button 
                    className="time-button"
                    onClick={() => handleClockOut(emp.num)}
                    style={{
                      background: currentClockOut === "00:00" ? '#6c757d' : '#dc3545',
                      color: 'white',
                      border: 'none',
                      padding: '8px 12px',
                      borderRadius: '4px',
                      cursor: 'pointer',
                      fontSize: '14px',
                      width: '100%'
                    }}
                  >
                    Clock Out<br/>{currentClockOut}
                  </button>
                </td>
                <td> 
                <div>
                    <select 
                      value={selectedShifts[emp.num] || ""} 
                      onChange={(e) => handleShiftChange(emp.num, e.target.value)}
                      className="dropdown"
                    >
                        <option value="" disabled>Choose a shift:</option>
                        <option value="1">1 : (6-14h)</option>
                        <option value="2">2 : (8-16h)</option>
                        <option value="3">3 : (16-00h)</option>
                    </select>
                </div>
                </td>
                <td>{currentDelay}</td>
                <td>{currentOvertime}</td>
                <td>{calculateHours(currentClockIn, currentClockOut)}</td>
                <td>
                <button 
                    className="opsbtn"
                    onClick={() => {
                    if (window.confirm(`Are you sure you want to delete ${emp.name}?`)) {
                        onEmployeeDeleted(emp.num);
                    }
                    }}
                    
                >
                    Remove
                </button>
                </td>
                </tr>
              );
            })}
            </tbody>
        </table>
        </div>
    </>
  );
}