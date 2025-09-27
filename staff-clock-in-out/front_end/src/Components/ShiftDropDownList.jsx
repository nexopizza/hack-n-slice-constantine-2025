export default function ShiftsDropDownList({Shifts}){
    return(
           <td> 
                <div>
                    <select className="dropdown">
                        <option value="" disabled selected>Choose a shift: </option>
                        {Shifts.map((sh) => (
                            <option>{sh.num}</option>
                        ))}
                    </select>
                </div>
            </td>
    )
}