import React from "react";
import styled from "styled-components";

const DescBox = styled("div")`
  background: #c4a29e;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0.8;
`;

const DescText = styled("p")`
  color: white;
  font-family: "Quicksand", sans-serif;
  margin: 4vw;
  font-size: 1.5vw;
`;

export default class LandingDesc extends React.Component {
  render() {
    return (
      <>
        <DescBox>
          <DescText>description</DescText>
        </DescBox>
      </>
    );
  }
}
