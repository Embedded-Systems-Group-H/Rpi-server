import React, { useEffect, useState } from "react";
import "./App.css";
import Table from './Table';
import Image from './Lily_run.jpeg';

const Home = () => {
  const [data, setData] = useState<any>(null);
  useEffect(() => {
    fetch("http://localhost:5000/")
      .then((res) => res.json())
      .then((data) => setData(data))
      .catch((error) => console.log("error while fetching data: ", error));
  }, []);
  
  return (
    <div className="App">
      <img src={require("./Lily_run.jpg")} width="100%"/>
      {data && data.data && <Table entries={data.data} />}
    </div>
  );
}

export default Home;
