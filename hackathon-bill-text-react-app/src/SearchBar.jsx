import React, { useState } from "react";

function SearchBar() {
  const [name, setName] = useState("");
  const [h1_Text, setHeading] = useState("");
  const [isMousedOver, setMouseOver] = useState(false);

  function handleChange(event) {
    setName(event.target.value);
    console.log(event.target.value);
    // console.log(event);
    // console.log(event.target.type);
    // console.log(event.target.placeholder);
  }

  function handleMouseOver() {
    setMouseOver(!isMousedOver);
  }

  function handleClick(event) {
    setHeading(name);
    // console.log({ name });

    event.preventDefault();
  }

  return (
    <div className="container">
      <h1>Welcome to Smash Parliament.uk {h1_Text} </h1>
      <form onSubmit={handleClick}>
        <input
          onChange={handleChange}
          type="text"
          placeholder="Please enter a keyword"
          value={name}
        />
        <button
          style={{ backgroundColor: isMousedOver ? "Aqua" : "white" }}
          type="submit"
          onMouseOver={handleMouseOver}
          onMouseOut={handleMouseOver}
        >
          Submit
        </button>
      </form>
    </div>
  );
}

export default SearchBar;
