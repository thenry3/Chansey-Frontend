import React from "react";
import styled from "styled-components";
import { Link } from "react-router-dom";

const NavComponents = styled("div")`
  display: flex;
  justify-content: space-between;
  background: #f7a9a8;
  width: 100%;
  font-family: "Comfortaa", cursive;
`;

const Title = styled("p")`
  color: #464655;
  font-size: 3vw;
  font-weight: bold;
  letter-spacing: 0.08em;
  margin: 2vh 5vw;
  height: 100%;
`;

const BarLinks = styled("div")`
  display: flex;
  font-size: 1.7vw;
  align-items: center;
  margin-right: 5vw;
`;

const NavLinkText = styled("p")``;

const NavLink = styled(Link)`
  height: 100%;
  color: #464655;
  text-decoration: none;
  text-align: center;
  margin: auto;
  padding-left: 1vw;
  padding-right: 1vw;
  transition: 0.2s;
  &:hover {
    background: #464655;
    color: #f7a9a8;
  }
`;

export default class NavBar extends React.Component {
  render() {
    return (
      <>
        <NavComponents>
          <Title>Chansey</Title>
          <BarLinks>
            <NavLink to="/signup1">
              <NavLinkText>sign up</NavLinkText>
            </NavLink>
            <NavLink to="/signin">
              <NavLinkText>sign in</NavLinkText>
            </NavLink>
          </BarLinks>
        </NavComponents>
      </>
    );
  }
}
