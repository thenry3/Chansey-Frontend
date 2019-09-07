import React from "react";
import ReactDOM from "react-dom";
import * as serviceWorker from "./serviceWorker";
import { BrowserRouter as Router } from "react-router-dom";
import { Route, Switch } from "react-router";

import LandingPage from "./pages/landing";
import SignupPage1 from "./pages/signup1";
import SigninPage from "./pages/signin";
import SignupPage2 from "./pages/signup2";

ReactDOM.render(
  <>
    <Router>
      <Switch>
        <Route exact path="/" component={LandingPage} />
        <Route path="/signup1" render={props => <SignupPage1 {...props} />} />
        <Route path="/signin" component={SigninPage} />
        <Route path="/signup2" component={SignupPage2} />
      </Switch>
    </Router>
  </>,
  document.getElementById("root")
);

serviceWorker.unregister();
