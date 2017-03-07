import React, { Component } from 'react';
import { Link } from 'react-router';

import style from './style.css';

class Home extends Component {
  render() {
    return (
      <div className={`${style.loginContainer}`}>
        <Link className={`${style.beginLoginButton} button`} to='/login'>Login</Link>
      </div>
    );
  }
}

export default Home;
