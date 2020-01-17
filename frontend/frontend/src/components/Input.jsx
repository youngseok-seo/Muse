import React, { useState } from 'react';
import './input.css';

// export const Input = () => {
    
//     const [word, setWord] = useState("");

//     const InputField = ({ value, placeholder, onChange }) => (
//         <input
//             value={value}
//             onChange={e => onChange(e.currentTarget.value)}
//             className="input"
//             placeholder={placeholder}
//         />
//     );
    
//     return (
//         <InputField 
//             value={word}
//             placeholder="ex. Today"
//             onChange={word => setWord(word)}
//         />
//     )
// }

const InputField = ({ value, placeholder, onChange }) => (
    <input
        value={value}
        onChange={e => onChange(e.currentTarget.value)}
        className="input"
        placeholder={placeholder}
    />
);

export default InputField;