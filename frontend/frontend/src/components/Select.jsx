import React, { useState } from 'react';
import './select.css';

// export const Select = () => {

//     const [data, setData] = useState({
//         artist: "Choose an Artist"
//     });

//     const DropDown = ({ options, onChange, value }) => (
//         <select
//             value={value}
//             defaultValue={data.artist}
//             onChange={e => onChange(e.currentTarget.value)}
//             className="select"
//         >
//             {options.map(([name, idx]) => (
//                 <option key={idx}>
//                     {name}
//                 </option>
//             ))}


//         </select>
//     );

//     return (
//         <DropDown
//             options={[
//                 'a', 'b', 'c'
//             ]}
//             value={data.artist}
//             onChange={name => {
//                 setData({ artist: name });
//             }}
//             className="select"
//         />
//     )

// }

const DropDown = ({ options, onChange, value }) => (
    <select
        value={value}
        defaultValue={value}
        onChange={e => onChange(e.currentTarget.value)}
        className="select"
    >
        {options.map((name, idx) => (
            <option key={idx}>
                {name}
            </option>
        ))}


    </select>
);

export default DropDown;




