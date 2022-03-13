/* eslint-disable react-hooks/rules-of-hooks */
import axios from "axios";

// const myMarkdownFile = require("./full-text.txt");

// fetch(myMarkdownFile)
//   .then((response) => response.text())
//   .then((text) => this.setState({ text }));

import React, { useState, useEffect } from "react";
import "./App.css";
import { fullTextData } from "./fulltext";

{
  /* <Tooltip title="Delete">
  <IconButton>
    <DeleteIcon />
  </IconButton>
</Tooltip> */
}

{
  /* <div class="tooltip">
  Hover over me
  <span class="tooltiptext">Tooltip text</span>
</div>; */
}

// function convertToJson() {
//   const txtToJson = require("txt-file-to-json");
//   const dataInJSON = txtToJson({ filePath: "./filePath.txt" });
//   console.log(dataInJSON);
// }

export const fullText = (props) => {
  const { billId } = props;
  const [billData, setBillData] = useState(null);
  useEffect(async () => {
    const { data: ret } = await axios.get(
      `https://hackathon-bill-text-nmgxkhvw5a-nw.a.run.app/bill-amendments/${billId}`
    );
    setBillData(ret);
  }, [billId]);

  console.log({ billId });

  if (!billData)
    return (
      <>
        <h3>Loading...</h3>
      </>
    );
  return (
    <>
      <div
        className="full-text"
        data-toggle="tooltip"
        data-placement="right"
        style={{ display: "flex" }}
      >
        <p style={{ width: "600px" }}>{billData.full_text}</p>

        <div
          className="amendments"
          style={{ width: "400px", textAlign: "left" }}
        >
          <h3>Agreed</h3>
          <ul>
            {billData.amendments.Agreed?.map((amendment) => {
              return (
                <li
                  title={amendment.sponsors
                    .map((sponsor) => sponsor.name)
                    .join(", ")}
                >
                  {amendment.summaryText?.map((text) => (
                    <>
                      {text}
                      <br />
                    </>
                  ))}
                </li>
              );
            })}
          </ul>
          <h3>Withdrawn</h3>
          <ul>
            {billData.amendments.Withdrawn?.map((amendment) => {
              return (
                <li
                  title={amendment.sponsors
                    .map((sponsor) => sponsor.name)
                    .join(", ")}
                >
                  {amendment.summaryText?.map((text) => (
                    <>
                      {text}
                      <br />
                    </>
                  ))}
                </li>
              );
            })}
          </ul>
          <h3>NotMoved</h3>
          <ul>
            {billData.amendments.NotMoved?.map((amendment) => {
              return (
                <li
                  title={amendment.sponsors
                    .map((sponsor) => sponsor.name)
                    .join(", ")}
                >
                  {amendment.summaryText?.map((text) => (
                    <>
                      {text}
                      <br />
                    </>
                  ))}
                </li>
              );
            })}
          </ul>
        </div>
        {/* 
        {fullTextData.map((fulltext, key) => {
          return (
            <div key={key}>
              {fulltext.introduction +
                " , " +
                fulltext.body +
                " ," +
                fulltext.amendments +
                ", " +
                fulltext.date}
              <p>
                But a person is entitled to receive payments by way of
                compensation for loss of earnings only if,
                <a
                  href="#"
                  data-mdb-toggle="tooltip"
                  title="Amended by Liz Truss"
                >
                  in consequence of acting as an emergency volunteer, the person
                  has suffered a loss of earnings that the person would
                  otherwise not have suffered.
                </a>
              </p>
            </div>
          );
        })} */}
      </div>
    </>
  );
};

// function getUrl() {
//   axios
//     .get("https://hackathon-bill-text-nmgxkhvw5a-nw.a.run.app/bill/2731")
//     .then(function (response) {
//       // handle success
//       console.log(response);
//     })
//     .catch(function (error) {
//       // handle error
//       console.log(error);
//     })
//     .then(function () {
//       // always executed
//     });
// }

// function App() {
//   return (
//     <div className="grid bg-yellow">
//       <header className="App-header">
//         <p>
//           Edit <code>src/App.js</code> and save to reload.
//         </p>
//         <a
//           className="App-link"
//           href="https://reactjs.org"
//           target="_blank"
//           rel="noopener noreferrer"
//         >
//           {myMarkdownFile}
//         </a>
//       </header>
//     </div>
//   );
// }

// function App() {
//   return (
//     <div className="grid bg-yellow">
//       {getUrl()}
//       <header className="App-header">
//         <p>
//           Edit <code>src/App.js</code> and save to reload.
//         </p>
//         <a
//           className="App-link"
//           href="https://reactjs.org"
//           target="_blank"
//           rel="noopener noreferrer"
//         >
//           Learn React
//         </a>
//       </header>
//     </div>
//   );
// }

export default fullText;
