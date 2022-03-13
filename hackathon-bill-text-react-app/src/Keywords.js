import { React, useState } from "react";
import data from "./KeywordData.json";

function Keywords(props) {
  return (
    <ul>
      {data.map((item) => (
        <li key={item.id} onClick={() => props.onClickKeyword(item.text)}>
          {item.text}
        </li>
      ))}
    </ul>
  );
}

export default Keywords;
