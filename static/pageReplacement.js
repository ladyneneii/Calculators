const loadingAnimation = document.querySelector("#loadingAnimation");
const body = document.body;
const showSimulation = document.querySelector("#showSimulation");

document
  .querySelector("#page_replacement_input_form")
  .addEventListener("submit", async (e) => {
    e.preventDefault();

    loadingAnimation.classList.remove("d-none");

    let isValid = /^(\d+|0|\s)+$/;
    let toNumbers = /\b(?:0|[1-9]\d*)\b/g;
    let pageReplacementAlgorithm = document.querySelector(
      "#page_replacement_algorithm"
    ).value;
    let PR = document.querySelector("#page_references").value;
    let NOF = document.querySelector("#number_of_frames").value;

    if (NOF < 1) {
      alert("Number of references should be greater than 0.");

      loadingAnimation.classList.add("d-none");

      return;
    }

    if (isValid.test(PR)) {
      let pageReferences = PR.match(toNumbers);

      let formData = {
        pageReplacementAlgorithm,
        pageReferences,
        numberOfFrames: NOF,
      };

      try {
        console.log("This is formData: ", formData);

        const response = await fetch("/sendInputPageReplacement", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(formData),
        });

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const returnedData = await response.json();
        // console.log("This is the returned data: ", returnedData);

        loadingAnimation.classList.add("d-none");

        constructPageReplacementResults(
          pageReplacementAlgorithm,
          pageReferences,
          returnedData
        );
      } catch (error) {
        console.error("Error: ", error);
      }
    } else {
      alert("Page references inputs should only contain numbers or spaces.");

      loadingAnimation.classList.add("d-none");

      return;
    }
  });

function constructPageReplacementResults(
  pageReplacementAlgorithm,
  pageReferences,
  returnedData
) {
  console.log(returnedData);
  const [framesDetailsSet, statistics] = returnedData;

  const { numberOfHits, numberOfFaults, hitsPercentage, faultsPercentage } =
    statistics;

  // get the last table
  const { frames, hitOrFault, remark, replacedRows } =
    framesDetailsSet[framesDetailsSet.length - 1];
  const columns = hitOrFault.length + 1;

  const container = document.createElement("div");
  container.classList.add("mx-5", "mt-5");

  const h1 = document.createElement("h1");
  h1.classList.add("mb-3");
  h1.textContent = pageReplacementAlgorithm;

  container.append(h1);

  // create table
  createTable(
    pageReferences,
    frames,
    replacedRows,
    hitOrFault,
    columns,
    container
  );

  // statistics
  const summary = document.createElement("p");
  summary.textContent = `Out of ${
    columns - 1
  } pages, there are ${numberOfHits} hits (${hitsPercentage}%) and ${numberOfFaults} faults (${faultsPercentage}%).`;

  container.append(summary);
  body.append(container);

  if (showSimulation.checked) {
    const h1 = document.createElement("h1");
    h1.textContent = "SIMULATION";
    h1.classList.add("mt-5");
    container.append(h1);

    // loop through each framesDetails
    framesDetailsSet.forEach((framesDetails) => {
      const { frames, hitOrFault, remark, replacedRows } = framesDetails;

      const container = document.createElement("div");
      container.classList.add("mx-5", "mt-5");

      // create table
      createTable(
        pageReferences,
        frames,
        replacedRows,
        hitOrFault,
        columns,
        container
      );

      // remark
      const p = document.createElement("p");
      p.textContent = `Remark: ${remark}`;

      container.append(p);

      body.append(container);
    });
  }
}

function createTable(
  pageReferences,
  frames,
  replacedRows,
  hitOrFault,
  columns,
  container
) {
  // display page references
  let table = document.createElement("table");
  table.classList.add("table", "table_color", "rounded-3");
  let thead = document.createElement("thead");
  let tr = document.createElement("tr");
  const occupiedColumns = hitOrFault.length + 1;

  for (let i = 0; i < columns; i++) {
    const th = document.createElement("th");
    th.classList.add("header_color", "text-center");
    th.setAttribute("scope", "col");
    th.textContent = i == 0 ? "Pages" : pageReferences[i - 1];

    tr.append(th);
  }

  thead.append(tr);
  table.append(thead);

  // display frames (main table)
  thead = document.createElement("thead");
  tr = document.createElement("tr");

  // headers (column numbers)
  for (let i = 0; i < columns; i++) {
    const th = document.createElement("th");
    th.classList.add("header_color", "text-center");
    th.setAttribute("scope", "col");
    th.textContent = i == 0 ? "Columns" : i;

    tr.append(th);
  }

  thead.append(tr);
  table.append(thead);

  // console.log("These are replaced rows ", replacedRows);

  const tbody = document.createElement("tbody");

  for (let i = 0; i < frames.length; i++) {
    const tr = document.createElement("tr");
    for (let j = 0; j < columns; j++) {
      const td = document.createElement("td");
      td.classList.add("table_color", "text-center");

      if (j > 0) {
        td.textContent = frames[i][j - 1];
        if (j + 1 < occupiedColumns) {
          const { col, row } = replacedRows[j];
          // console.log("THIS IS ", i, j);
          // console.log("ROW COL: ", row, col);

          if (row == i && col == j) {
            td.classList.add("replaced_page");
          }
        }
      } else {
        td.textContent = `Frame ${i + 1}`;
        td.classList.add("header_color", "fw-bold");
      }

      tr.append(td);
    }

    tbody.append(tr);
  }

  // hit or fault
  tr = document.createElement("tr");
  for (let i = 0; i < columns; i++) {
    const th = document.createElement("th");
    th.classList.add("header_color", "text-center");
    th.textContent = i == 0 ? " " : hitOrFault[i - 1];

    tr.append(th);
  }

  tbody.append(tr);

  table.append(tbody);
  container.append(table);
}
