const express = require("express");
const cors = require("cors");
const app = express();

const { once } = require("node:events");
const { createReadStream } = require("node:fs");
const { createInterface } = require("node:readline");

const PORT = 5000;
const fileName = "files/summary.csv";

app.use(cors());

app.get("/", async (req, res) => {
  try {
    let data = { data: [] };
    const readLine = createInterface({
      input: createReadStream(fileName),
      crlfDelay: Infinity,
    });

    readLine.on("line", (line) => {
      const [date, duration, distance, steps, calories, ...others] =
        line.split(",");
      const coordinates = JSON.parse(others.join(","));
      const dataLine = {
        date,
        duration,
        distance,
        steps,
        calories,
        coordinates,
      };
      data = { data: [...data.data, dataLine] };
    });
    await once(readLine, "close");
    res.send(data);
  } catch (err) {
    console.error(err);
  }
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});