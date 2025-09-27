export default function DropDownList({employees}){
    return(
           <td> 
                <div>
                    <select id="employees" name="employees" className="dropdown">
                        <option value="" disabled selected>Choose an employee </option>
                        {employees.map((emp) => (
                            <option>{emp.name}</option>
                        ))}
                    </select>
                </div>
            </td>
    )
}

