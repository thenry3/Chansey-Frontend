import React from "react";
import styled from "styled-components";

const Form = styled("form")`
  background: #f7a9a8;
  border-radius: 10px;
  width: 35%;
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
`;

const Input = styled("input")`
  border: none;
  width: 65%;
  font-size: 1.3vw;
  padding: 10px 20px;
  border-radius: 25px;
  margin-bottom: 10px;
  color: #464655;
  &:focus {
    outline: none;
  }
`;

const SignupText = styled("p")`
  color: white;
  font-size: 3vw;
  font-weight: bold;
  letter-spacing: 0.1em;
  margin-bottom: 2vh;
  margin-top: 3vh;
`;

const FormItems = styled("div")`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 90%;
  font-family: "Quicksand", sans-serif;
`;

const RegisterButton = styled("button")`
  color: #464655;
  font-size: 1.7vw;
  background: white;
  border: none;
  font-family: "Quicksand", sans-serif;
  border-radius: 25px;
  transition: 0.2s;
  margin-top: 2vh;
  margin-bottom: 4vh;
  padding: 0.5vw 2vw;
  letter-spacing: 0.1em;
  &:hover {
    background: #464655;
    color: white;
  }
`;

const ChooseSchool = styled("select")`
  outline: none;
  font-family: "Quicksand", sans-serif;
  &:focus {
    outline: none;
  }
`;

const SchoolOption = styled("option")``;

export default class SignupForm2 extends React.Component {
  render() {
    return (
      <>
        <Form action="/">
          <FormItems>
            <ChooseSchool>
              <SchoolOption value="upenn">
                University of Pennyslvania
              </SchoolOption>
              <SchoolOption value="ucla">
                University of California - Los Angeles
              </SchoolOption>
              <SchoolOption value="umd">
                University of Maryland, College Park
              </SchoolOption>
            </ChooseSchool>
            <Input placeholder="Name" required></Input>
            <Input type="email" placeholder="Email Address" required></Input>
            <Input type="password" placeholder="Password" required></Input>
            <RegisterButton type="submit">Register</RegisterButton>
          </FormItems>
        </Form>
      </>
    );
  }
}
