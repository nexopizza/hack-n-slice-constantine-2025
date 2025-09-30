export default function ReportingContent( { employees } ) {
  return (
    <>
        {/* <div
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
        </div> */}

        
        
        <div>
        <table border="1" cellPadding="20" cellSpacing="0">
            <thead>
            <tr>
                <th>Num</th>
                <th>Full name</th>
                <th>Delay</th>
                <th>Overtime</th>
                <th>Hours</th>
                
            </tr>
            </thead>
            <tbody>
            {employees.map((emp) => (
                <tr>
                <td>{emp.num}</td>
                <td>{emp.name}</td>
                <td>{emp.delay}</td>
                <td>{emp.overtime}</td>
                <td>{emp.hours}</td>
                </tr>
            ))}
            </tbody>
        </table>
        </div>
    </>
  );
}
