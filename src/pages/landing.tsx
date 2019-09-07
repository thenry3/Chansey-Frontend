import * as React from "react";
import styled from "styled-components";

import NavBar from "../components/navbar";
import LandingDesc from "../components/landingdesc";

const Page = styled("div")`
  background: #feffd1;
  width: 100%;
  height: 100vh;
`;

const PageContent = styled("div")`
  width: 100%;
  display: flex;
`;

export default class LandingPage extends React.Component {
  render() {
    return (
      <>
        <Page>
          <NavBar></NavBar>
          <PageContent>
            <LandingDesc />
          </PageContent>
        </Page>
      </>
    );
  }
}
