export default function Content( { employees } ) {
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
            {employees.map((emp) => (
                <tr>
                <td>{emp.num}</td>
                <td>{emp.name}</td>
                <td contentEditable="true"  data-placeholder="Clock in"></td>
                <td contentEditable="true"  data-placeholder="Clock out"></td>
                <td> 
                <div>
                    <select id="employees" name="employees" className="dropdown">
                        <option value="" disabled selected>Choose a shift:</option>
                        <option value="akram">1 : (6-14h)</option>
                        <option value="nouha">2 : (8-16h)</option>
                        <option value="samir">3 : (16-00h)</option>
                    </select>
                </div>
                </td>
                <td>{emp.delay}</td>
                <td>{emp.overtime}</td>
                <td>{emp.hours}</td>
                <td><button className="opsbtn">Remove</button></td>
                </tr>
            ))}
            </tbody>
        </table>
        </div>
    </>
  );
}
