import React, { useState } from 'react';
import './mainPage.css';
import Logo from '../../components/Logo';
import TempSlider from '../../components/Slider';
import DropDown from '../../components/Select';
import Header from '../../components/Header';
import InputField from '../../components/Input';
import Button from '../../components/Button';
import Text from '../../components/Text';

import Axios from 'axios';
const apiurl = 'http://muse-lyrics-server.herokuapp.com/';

const MainPage = () => {

    const [data, setData] = useState({
        artist: "",
        temp: 0.5,
        word: "",
        text: "",
        clicked: false
    })

    console.dir(data.artist);
    console.dir(data.word);
    console.dir(data.temp);


    return (
        <div className='mainPage'>
            <Logo />
            <Header value="Choose an artist:"/>
            <DropDown
                options={[
                    'Select', 'ABBA', 'The Beatles', 'Bee Gees', 'Bon Jovi', 
                    'Elton John', 'Michael Jackson', 'Queen', "Stevie Wonder"
                ]}
                value={data.artist}
                onChange={name => {
                    setData({ ...data, artist: name });
                }}
                className="select"
            /> 
            <Header value="Pick a temperature:" />
            <TempSlider valueLabelDisplay="auto" aria-label="slider" 
                        defaultValue={0.5} aria-valuetext={data.temp}
                        onChangeCommitted={ (e, val) => setData({ ...data, temp: val })}
                        max={1.0} min={0.1} step={0.1}
            />
            <Header value="Enter a starting word:" />
            <InputField 
                value={data.word}
                placeholder="ex. Today"
                onChange={word => setData({ ...data, word: word })}
            />
            <Button 
                onClick={( clicked ) => {
                    Axios.post(apiurl, data)
                        .then(response => {
                            setData({ ...data, text: response.data.text, clicked: false })
                            console.log(response);
                            console.dir(data.text);
                        });
                    setData({ ...data, clicked: true });
                }}
                loading={ data.clicked }
            >
                Generate!
            </Button>
            <Text value={ data.text } />
        </div>
    )
}

export default MainPage;