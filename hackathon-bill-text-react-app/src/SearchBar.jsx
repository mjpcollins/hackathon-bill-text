import { React, useCallback, useState } from "react";
// import TextField from "@mui/material/TextField";
import Keywords from "./Keywords";
import "./App.css";
import { useEffect } from "react";
import axios from "axios";

function SearchBar({ setBillId }) {
  const [searchVal, setSearchVal] = useState("");
  const [results, setResults] = useState([]);

  const fetchSearchResults = useCallback(async () => {
    const ret = await axios
      .get(
        `https://hackathon-bill-text-nmgxkhvw5a-nw.a.run.app/search/${searchVal}`
      )
      .then((a) => a.data);
    setResults(ret.search_results);
  }, [searchVal]);

  useEffect(() => {
    if (searchVal.length >= 4) {
      fetchSearchResults();
    } else {
      setResults([]);
    }
  }, [fetchSearchResults, searchVal]);

  return (
    <div className="container">
      <h1>Welcome to Smash Parliament.uk</h1>
      <div className="search">
        <input
          type="text"
          value={searchVal}
          onInput={(ev) => setSearchVal(ev.target.value)}
          style={{ color: "black" }}
        />
        {/* <TextField
          id="outlined-basic"
          variant="outlined"
          fullWidth
          label="Search"
        /> */}
      </div>

      <ul style={{ position: "absolute", background: "white" }}>
        {results.map((result) => {
          return (
            <li onClick={() => setBillId(result.data.billId)}>
              {result.data.shortTitle}
            </li>
          );
        })}
      </ul>
      <Keywords onClickKeyword={(keyword) => setSearchVal(keyword)} />
    </div>
  );
}

export default SearchBar;
