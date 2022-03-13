import React, { useState } from "react";
// import Tab from "@material-ui/core/Tab";
// import Tabs from "@material-ui/core/Tabs";
import "./App.css";
import SearchBar from "./SearchBar";
import { Tabs, Tab } from "react-bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";
import TextSearch from "./TextSearch";

const App = () => {
  const [billId, setBillId] = useState("");
  console.log({ billId });
  //function App() {
  return (
    <div className="App">
      <Tabs defaultActiveKey="keyword" id="uncontrolled-tab-example">
        <Tab eventKey="keyword" title="Keyword Search">
          <SearchBar setBillId={setBillId} />
        </Tab>
        <Tab eventKey="list" title="Text Search">
          <TextSearch billId={billId} />
        </Tab>
      </Tabs>
    </div>
  );
};

// <Tabs defaultActiveKey="keyword" id="uncontrolled-tab-example">
//   <Tab eventKey="keyword" title="Keyword Search">
//     <SearchBar></SearchBar>
//   </Tab>
//   <Tab eventKey="list" title="Text Search">
//     <TextSearch></TextSearch>
//   </Tab>
// </Tabs>

export default App;
