import Header from "../Components/Header"
import Content from "../Components/Content"
import TextField from "../Components/TextField"
// import Animation3d from "../Components/The3dDesign"


export default function ClockInPage()
{
    const employees = [
    {
      num: 1,
      name: "Akram Dib",
      clockIn: "08:00",
      clockOut: "16:00",
      shift: 0,
      delay: " ",
      overtime: " ",
      hours: " ",
    },
    {
      num: 2,
      name: "Alaa krem",
      clockIn: "09:00",
      clockOut: "17:00",
      shift: 0,
      delay: " ",
      overtime: " ",
      hours: " ",
    },
    {
      num: 3,
      name: "Diaa Chouai",
      clockIn: "07:30",
      clockOut: "15:30",
      shift: 0,
      delay: " ",
      overtime: " ",
      hours: " ",
    },
    {
      num: 4,
      name: "Djelil Bestandji",
      clockIn: "07:30",
      clockOut: "15:30",
      shift: 0,
      delay: " ",
      overtime: " ",
      hours: " ",
    },
  ];
  return (
    <>
      <Header />
      <TextField label="Date"/>
      <Content employees={ employees }/>
      <div className='cntbtns'>
         <button className='cntbtn'>New Employee</button>
         <button className='cntbtn'>Save</button>
      </div>
    </>
  );
}