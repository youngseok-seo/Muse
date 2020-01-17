import React from 'react';
import './button.css';

const Button = ({ children, loading, onClick = () => {} }) => (
    <button className='button' onClick={onClick}>
        {loading? ". . ." : children}
    </button>
);

export default Button;