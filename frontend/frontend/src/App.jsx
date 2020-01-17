import React, { Component } from 'react';
import './App.css';

import { BrowserRouter as Router, Route } from 'react-router-dom';
import MainPage from './pages/MainPage/MainPage';

class App extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <Router>
        <div className="App">
          <Route exact path="/" component={MainPage}/>
        </div>
      </Router>
    );
  }
}

export default App;
