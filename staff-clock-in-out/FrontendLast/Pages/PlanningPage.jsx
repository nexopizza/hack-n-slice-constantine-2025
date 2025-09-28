import Header from "../Components/Header"
import DropDownList from "../Components/DropDownList"
import "../index.css"
import { useState, useEffect, useRef } from "react"
import ShiftsDropDownList from "../Components/ShiftDropDownList"
import { employeesApi } from "../services/employeesAPI"
import { planningApi } from "../services/planningAPI"

export default function Planning(){
    const [isOpen, setIsOpen] = useState(false);
    const [employees, setEmployees] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [saving, setSaving] = useState(false);
    const [loadingPlanning, setLoadingPlanning] = useState(false);
    const [activeTab, setActiveTab] = useState(0); // 0-6 for days of week

    // Refs to store the current planning data for each day
    const planningDataRefs = useRef({});
    const existingPlannings = useRef({});

    // Define posts (tasks)
    const posts = [
        { id: 1, name: "Pizzaiolo" },
        { id: 2, name: "Livreur" },
        { id: 3, name: "Agent polyvalent" },
        { id: 4, name: "Prepateur" },
        { id: 5, name: "Cassier" },
        { id: 6, name: "Serveur" },
        { id: 7, name: "Plongeur" },
        { id: 8, name: "Manageur" },
        { id: 9, name: "Packaging" },
        { id: 10, name: "Topping" },
        { id: 11, name: "Bar" }
    ];

    // Define shifts
    const shifts = [
        { id: 1, name: "6:00-14:00 (1)", time: "6:00-14:00" },
        { id: 2, name: "8:00-16:00 (2)", time: "8:00-16:00" },
        { id: 3, name: "16:00-00:00 (3)", time: "16:00-00:00" }
    ];

    // Get dates for the current week (Monday to Sunday)
    const getWeekDates = () => {
        const dates = [];
        const today = new Date();
        const currentDay = today.getDay();
        const monday = new Date(today);
        monday.setDate(today.getDate() - currentDay + (currentDay === 0 ? -6 : 1)); // Adjust to get Monday
        
        for (let i = 0; i < 7; i++) {
            const date = new Date(monday);
            date.setDate(monday.getDate() + i);
            dates.push(date.toISOString().split('T')[0]);
        }
        return dates;
    };

    const [weekDates, setWeekDates] = useState(getWeekDates());

    // Day names for tabs
    const dayNames = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];

    // Get current date for the active tab
    const getCurrentDate = () => weekDates[activeTab];

    // Format date for display
    const formatDateDisplay = (dateString) => {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', { 
            weekday: 'long', 
            month: 'short', 
            day: 'numeric' 
        });
    };

    // Fetch employees from API on component mount
    useEffect(() => {
        const fetchEmployees = async () => {
            try {
                setLoading(true);
                const employeesData = await employeesApi.getEmployees();
                
                const transformedEmployees = employeesData.map(emp => ({
                    name: emp.name,
                    emp_id: emp.emp_id || emp.id
                }));
                
                setEmployees(transformedEmployees);
            } catch (err) {
                console.error('Error fetching employees:', err);
                setError('Failed to load employees');
                setEmployees(getFallbackEmployees());
            } finally {
                setLoading(false);
            }
        };

        fetchEmployees();
    }, []);

    // Load planning when tab changes
    useEffect(() => {
        if (employees.length > 0) {
            loadExistingPlanningForTab(activeTab);
        }
    }, [activeTab, employees]);

    // Function to load existing planning for a specific tab/date
    const loadExistingPlanningForTab = async (tabIndex) => {
        const date = weekDates[tabIndex];
        try {
            setLoadingPlanning(true);
            const planningData = await planningApi.getPlanning(date);
            
            // Store in ref
            existingPlannings.current[date] = planningData;
            
            // Initialize planning data ref for this date if not exists
            if (!planningDataRefs.current[date]) {
                planningDataRefs.current[date] = {};
            }
            
            // Populate the planningDataRef with existing data
            planningData.forEach(assignment => {
                const key = `${assignment.task_id}-${assignment.shift_id}`;
                planningDataRefs.current[date][key] = {
                    shift_id: assignment.shift_id,
                    emp_id: assignment.emp_id,
                    task_id: assignment.task_id,
                    plan_date: date,
                    employee_name: assignment.employee_name
                };
            });
            
            console.log(`Loaded planning for ${date}:`, planningData);
        } catch (error) {
            console.error(`Error loading planning for ${date}:`, error);
            existingPlannings.current[date] = [];
            if (!planningDataRefs.current[date]) {
                planningDataRefs.current[date] = {};
            }
        } finally {
            setLoadingPlanning(false);
        }
    };

    // Function to get fallback employees
    const getFallbackEmployees = () => [
        { name: "Akram Dib", emp_id: 1 },
        { name: "Alaa krem", emp_id: 2 },
        // ... include all your fallback employees with emp_id
    ];

    // Function to handle employee selection in a dropdown
    const handleEmployeeSelect = (postId, shiftId, employee, date) => {
        const key = `${postId}-${shiftId}`;
        if (!planningDataRefs.current[date]) {
            planningDataRefs.current[date] = {};
        }
        planningDataRefs.current[date][key] = {
            shift_id: shiftId,
            emp_id: employee?.emp_id || null,
            task_id: postId,
            plan_date: date,
            employee_name: employee?.name || null
        };
    };

    // Function to get selected employee for a specific post and shift
    const getSelectedEmployee = (postId, shiftId, date) => {
        if (!planningDataRefs.current[date]) return null;
        
        const key = `${postId}-${shiftId}`;
        const assignment = planningDataRefs.current[date][key];
        if (assignment && assignment.emp_id) {
            return employees.find(emp => emp.emp_id === assignment.emp_id) || null;
        }
        return null;
    };

    // Save planning for current tab
    const savePlanning = async () => {
        const currentDate = getCurrentDate();
        try {
            setSaving(true);
            
            // Convert the planning data object to array
            const planningArray = planningDataRefs.current[currentDate] 
                ? Object.values(planningDataRefs.current[currentDate]).filter(item => item.emp_id !== null)
                : [];

            if (planningArray.length === 0) {
                alert('No planning data to save!');
                return;
            }

            await planningApi.savePlanning({
                plan_date: currentDate,
                assignments: planningArray
            });

            alert(`Planning for ${formatDateDisplay(currentDate)} saved successfully!`);
            // Reload the planning to reflect changes
            await loadExistingPlanningForTab(activeTab);
        } catch (error) {
            console.error('Error saving planning:', error);
            alert('Error saving planning: ' + error.message);
        } finally {
            setSaving(false);
        }
    };

    // Save all planning for the entire week
    const saveAllPlanning = async () => {
        try {
            setSaving(true);
            let totalSaved = 0;

            for (const date of weekDates) {
                const planningArray = planningDataRefs.current[date] 
                    ? Object.values(planningDataRefs.current[date]).filter(item => item.emp_id !== null)
                    : [];

                if (planningArray.length > 0) {
                    await planningApi.savePlanning({
                        plan_date: date,
                        assignments: planningArray
                    });
                    totalSaved += planningArray.length;
                }
            }

            alert(`All planning saved successfully! Total assignments: ${totalSaved}`);
        } catch (error) {
            console.error('Error saving all planning:', error);
            alert('Error saving planning: ' + error.message);
        } finally {
            setSaving(false);
        }
    };

   
    // Navigate to previous/next week
    const navigateWeek = (direction) => {
        const newWeekDates = weekDates.map(date => {
            const d = new Date(date);
            d.setDate(d.getDate() + (direction === 'next' ? 7 : -7));
            return d.toISOString().split('T')[0];
        });
        setWeekDates(newWeekDates);
    };

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
                    <div>Loading employees...</div>
                </div>
            </>
        );
    }

    return(
        <>
            <Header /> 
            <div
            style={{
                display: "flex",
                justifyContent: "flex-start",
                alignItems: "center",
                color: "black",
                fontSize: "30px",
                marginLeft:"35px",
                marginTop: "40px",
                marginBottom: "0px",
            }}
            >
               Weekly Planning Table
            </div>
            <div
            style={{
                display: "flex",
                justifyContent: "flex-start",
                alignItems: "center",
                color: "black",
                fontSize: "14px",
                marginLeft:"35px",
                marginTop: "5px",
                marginBottom: "20px",
            }}
            >
               Organize and display work shifts for the entire week
            </div>

            {/* Week Navigation */}
            <div style={{ margin: "0 35px 20px", display: "flex", alignItems: "center", gap: "15px" }}>
                <button 
                    className="cntbtn" 
                    onClick={() => navigateWeek('prev')}
                    style={{ padding: "8px 16px" }}
                >
                    ← Previous Week
                </button>
                <span style={{ fontWeight: "bold", fontSize: "16px" }}>
                    Week of {formatDateDisplay(weekDates[0])} - {formatDateDisplay(weekDates[6])}
                </span>
                <button 
                    className="cntbtn" 
                    onClick={() => navigateWeek('next')}
                    style={{ padding: "8px 16px" }}
                >
                    Next Week →
                </button>
            </div>

            {/* Day Tabs */}
            <div style={{ margin: "0 35px 20px" }}>
                <div className="tabs-container">
                    {dayNames.map((day, index) => (
                        <button
                            key={index}
                            className={`tab-button ${activeTab === index ? 'active' : ''}`}
                            onClick={() => setActiveTab(index)}
                        >
                            <div>{day}</div>
                            <div style={{ fontSize: "12px", opacity: 0.8 }}>
                                {new Date(weekDates[index]).getDate()}
                            </div>
                        </button>
                    ))}
                </div>
            </div>

            {/* Current Tab Info */}
            <div style={{ margin: "0 35px 20px", display: "flex", alignItems: "center", gap: "15px" }}>
                <span style={{ fontWeight: "bold" }}>
                    {formatDateDisplay(getCurrentDate())}
                </span>
                {loadingPlanning && <span>Loading planning...</span>}
                {!loadingPlanning && (
                    <span style={{ color: 'green', fontSize: '14px' }}>
                        Found {existingPlannings.current[getCurrentDate()]?.length || 0} assignments
                    </span>
                )}
            </div>

            {/* Planning Table for Active Tab */}
            <div>
                <table border="1" cellPadding="20" cellSpacing="0" style={{ width: "95%", margin: "0 auto" }}>
                    <thead>
                    <tr>
                        <th>Posts/Shifts</th>
                        {shifts.map(shift => (
                            <th key={shift.id}>{shift.name}</th>
                        ))}
                        <th>Operations</th>
                    </tr>
                    </thead>
                    <tbody>
                    {posts.map(post => (
                        <tr key={post.id}>
                            <td style={{background:"linear-gradient(to right, #EB4219, #F6892A)", color: "white"}}>
                                {post.name}
                            </td>
                            {shifts.map(shift => (
                                <td key={shift.id}>
                                    <DropDownList 
                                        employees={employees}
                                        onSelect={(employee) => handleEmployeeSelect(post.id, shift.id, employee, getCurrentDate())}
                                        selectedEmployee={getSelectedEmployee(post.id, shift.id, getCurrentDate())}
                                    />
                                </td>
                            ))}
                            <td>
                                <button className="edit-btn" onClick={() => setIsOpen(true)}>Edit</button>
                            </td>
                        </tr>
                    ))}    
                    </tbody>
                </table>

                {/* Modal/Dialog */}
                {isOpen && (
                <div className="dialog-backdrop">
                  <div className="dialog-box">
                <h3
                style={{
                  textAlign: "center",
                  marginTop: "0",
                  background: "linear-gradient(to right, #EB4219, #F6892A, #F36224, #EB4219)",
                  WebkitBackgroundClip: "text",
                  WebkitTextFillColor: "transparent"
                }}
                >
                  Edit Box
                </h3>
                <div className="modal">
                  <ShiftsDropDownList Shifts={shifts} />
                  <DropDownList employees={employees} />
                </div>
                <div style={{ textAlign: "center", marginTop:"30px"}}>
                  <button className="edit-btn" onClick={() => setIsOpen(false)}>Close</button>
                  <button className="edit-btn" onClick={() => alert(`Values: ${field1}, ${field2}`)}>Save</button>
                </div>
                </div>
                </div>
                )}

                {/* Action Buttons */}
                <div className='cntbtns' style={{ marginTop: "30px" }}>
                  <button 
                    className='cntbtn' 
                    onClick={savePlanning}
                    disabled={saving || loadingPlanning}
                  >
                    {saving ? 'Saving...' : `Save ${dayNames[activeTab]} Planning`}
                  </button>
                  <button 
                    className='cntbtn' 
                    onClick={saveAllPlanning}
                    disabled={saving}
                    style={{backgroundColor: '#28a745'}}
                  >
                    {saving ? 'Saving...' : 'Save Entire Week'}
                  </button>
                  <button 
                    className='cntbtn' 
                    onClick={() => loadExistingPlanningForTab(activeTab)}
                    disabled={loadingPlanning}
                    style={{backgroundColor: '#17a2b8'}}
                  >
                    {loadingPlanning ? 'Loading...' : 'Refresh'}
                  </button>
                </div>
            </div>

            {/* Add CSS for tabs */}
            <style jsx>{`
                .tabs-container {
                    display: flex;
                    border-bottom: 2px solid #e0e0e0;
                }
                .tab-button {
                    flex: 1;
                    padding: 15px 10px;
                    border: none;
                    background: #f8f9fa;
                    cursor: pointer;
                    transition: all 0.3s ease;
                    border-bottom: 3px solid transparent;
                    text-align: center;
                }
                .tab-button:hover {
                    background: #e9ecef;
                }
                .tab-button.active {
                    background: white;
                    border-bottom: 3px solid #EB4219;
                    font-weight: bold;
                    color: #EB4219;
                }
            `}</style>
        </>
    )
}