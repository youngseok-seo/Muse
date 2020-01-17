import React from 'react';
import './text.css';

const Text = ({ value }) => (
    <textarea
        className="text"
        placeholder="Your lyrics will show here!"
        value={value}
    />
);

export default Text;