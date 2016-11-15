import React from 'react';
import { IndexRoute, Route  } from 'react-router';

import { requireAuthentication } from './containers/authenticateComponent';
import Layout from './containers/layout';
import Home from './containers/home';
import Search from './containers/search';
import Login from './containers/login';

export default (
  <Route component={Layout} path='/'>
    <IndexRoute component={requireAuthentication(Home)} />
    <Route compoment={requireAuthentication(Search)} path='/search' />
    <Route component={Login} path='login' />
  </Route>
);
