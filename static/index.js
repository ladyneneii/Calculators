const loadingAnimation = document.querySelector("#loadingAnimation");
const priority = document.querySelector("#priority");
const level = document.querySelector("#level");
const main_algorithm = document.querySelector("#main_algorithm");
const rr_qt = document.querySelector("#rr_qt");
const add_btn = document.querySelector("#add_btn");
let mlfq_qt = document.querySelectorAll(".mlfq_qt");
const mlfq_algorithm = document.querySelector("#mlfq_algorithm");
const mlfq_algo_div = document.querySelector(".mlfq_algo_div");
const add_lvl_btn = document.querySelector("#add_lvl_btn");
const last_lvl = document.querySelector("#last_lvl");
let mlq_algo_divs = document.querySelectorAll(".mlq_algo_div");
let mlq_algorithms = document.querySelectorAll(".mlq_algorithm");
let delete_divs = document.querySelectorAll(".btn-close");
let isPriority = false;
let isRR = false;
let isMLQ = false;
let isMLFQ = false;

main_algorithm.addEventListener("change", () => {
  isPriority = main_algorithm.value.includes("Priority");
  isRR = main_algorithm.value === "RoundRobin";
  isMLQ = main_algorithm.value === "MLQ";
  isMLFQ = main_algorithm.value === "MLFQ";

  toggleElements();
});

mlfq_algorithm.addEventListener("change", () => {
  isPriority = mlfq_algorithm.value.includes("Priority");
  isRR = mlfq_algorithm.value === "RoundRobin";
  isMLQ = mlfq_algorithm.value === "MLQ";

  toggleElements();
});

const user_input_form = document.querySelector("#user_input_form");
const mlq_row = document.querySelector("#mlq_row");

let mlq_level = 2;
add_btn.addEventListener("click", () => {
  mlq_level++;
  // Create a new mlq_algo_div
  const newDiv = document.createElement("div");
  newDiv.classList.add("mb-3", "col", "mlq_algo_div");

  const label_close = document.createElement("div");
  label_close.className = "label_close";

  // Create a new label for the new mlq_algo_div
  const newLabel = document.createElement("label");
  newLabel.classList.add("form-label");
  newLabel.textContent = `Algorithm Level ${mlq_level} (MLQ):`;

  const close_btn = document.createElement("button");
  close_btn.setAttribute("type", "button");
  close_btn.className = "btn-close";

  // Create a new select for the new mlq_algo_div
  const newSelect = document.createElement("select");
  newSelect.classList.add("form-select", "mlq_algorithm");

  // Add options to the new select
  const options = [
    "FCFS (First-Come, First-Served)",
    "SJF (Shortest Job First)",
    "Priority (Non-Preemptive)",
    "Priority (Preemptive)",
    "SRTF (Shortest Remaining Time First)",
  ];
  options.forEach((optionValue) => {
    const option = document.createElement("option");

    option.value = optionValue.split(" ")[0];
    if (optionValue === "Priority (Non-Preemptive)") {
      option.value += "NP";
    } else if (optionValue === "Priority (Preemptive)") {
      option.value += "P";
    }
    option.textContent = optionValue;
    newSelect.appendChild(option);
  });

  // Append the new label and select to the new mlq_algo_div
  label_close.appendChild(newLabel);
  label_close.appendChild(close_btn);
  newDiv.append(label_close);
  newDiv.appendChild(newSelect);

  // Append the new mlq_algo_div to the container
  mlq_row.append(newDiv);
  // newDiv.querySelector(".mlq_algorithm").addEventListener("change", traverseMLQAlgoDivs);

  // this is update the values of mlq_alglo_divs and mlq_algorithms with the newly added mlq_algorithm select elements
  mlq_algo_divs = document.querySelectorAll(".mlq_algo_div");
  mlq_algorithms = document.querySelectorAll(".mlq_algorithm");

  delete_divs = document.querySelectorAll(".btn-close");
  deleteAlgoLevel();

  traverseMLQAlgoDivs();
});

let last_level = 3;
const quantum_row = document.querySelector("#quantum_row");
add_lvl_btn.addEventListener("click", () => {
  const newDiv = document.createElement("div");
  newDiv.classList.add("mb-3", "mlfq_qt", "col");

  const label_close = document.createElement("div");
  label_close.className = "label_close";

  const label = document.createElement("label");
  label.classList.add("form-label");
  label.textContent = `Level ${last_level} Quantum Time`;

  const close_btn = document.createElement("button");
  close_btn.setAttribute("type", "button");
  close_btn.className = "btn-close";

  const input = document.createElement("input");
  input.type = "number";
  input.classList.add("form-control", "mlfq_quantum_time");

  // Append the elements to the container
  label_close.append(label);
  label_close.append(close_btn);
  newDiv.appendChild(label_close);
  newDiv.appendChild(input);

  quantum_row.insertBefore(newDiv, mlfq_algo_div);

  last_level++;
  last_lvl.textContent = `Level ${last_level} Algorithm:`;

  mlfq_qt = document.querySelectorAll(".mlfq_qt");

  delete_divs = document.querySelectorAll(".btn-close");
  deleteAlgoLevel();
});

function deleteAlgoLevel() {
  delete_divs.forEach((delete_div) => {
    // Remove existing event listener before adding a new one
    delete_div.removeEventListener("click", handleDeleteClick);

    // Add a new event listener
    delete_div.addEventListener("click", handleDeleteClick);
  });
}

function handleDeleteClick(e) {
  const class_list = e.target.parentElement.parentElement.classList;
  if (class_list.contains("mlfq_qt")) {
    last_level--;
    if (last_level <= 1) {
      alert("You must have at least two levels in MLFQ.");
      last_level++;

      loadingAnimation.classList.add("d-none");

      return;
    }
  } else if (class_list.contains("mlq_algo_div")) {
    mlq_level--;
    if (mlq_level <= 0) {
      alert("You must have at least one level in MLQ.");
      mlq_level++;

      loadingAnimation.classList.add("d-none");
      
      return;
    }
  }
  class_list.add("d-none");
  e.currentTarget.parentElement.parentElement.remove();

  // update
  mlq_algo_divs = document.querySelectorAll(".mlq_algo_div");
  mlq_algorithms = document.querySelectorAll(".mlq_algorithm");
  updateQuantumLevelLabel();
  updateMLQLevelLabel();
  checkPrio();
}

function updateQuantumLevelLabel() {
  let level = 1;
  mlfq_qt.forEach((qt) => {
    if (!qt.classList.contains("d-none")) {
      const formLabel = qt.querySelector(".form-label");
      if (formLabel) {
        formLabel.textContent = `Level ${level} Quantum Time`;
        level++;
      }
    }
  });
  const formLabel = mlfq_algo_div.querySelector(".form-label");
  if (formLabel) {
    formLabel.textContent = `Level ${level} Algorithm`;
  }
}

function updateMLQLevelLabel() {
  let level = 1;
  mlq_algo_divs.forEach((mlq) => {
    if (!mlq.classList.contains("d-none")) {
      const formLabel = mlq.querySelector(".form-label");
      if (formLabel) {
        formLabel.textContent = `Algorithm Level ${level} (MLQ):`;
        level++;
      }
    }
  });
}

function toggleElements() {
  priority.classList.toggle("d-none", !isPriority);
  mlq_algo_divs.forEach((mlq_algo_div) => {
    mlq_algo_div.classList.toggle("d-none", !isMLQ);
  });
  add_btn.classList.toggle("d-none", !isMLQ);
  level.classList.toggle("d-none", !isMLQ);

  mlfq_qt.forEach((qt) => {
    qt.classList.toggle("d-none", !isMLFQ);
  });
  add_lvl_btn.classList.toggle("d-none", !isMLFQ);
  mlfq_algo_div.classList.toggle("d-none", !isMLFQ);

  if (isMLQ) {
    // this is called so that each mlq_algorithm select element can listen for the change event. if this is not called, they will not be able to listen to it since the event listening is inside a function, which is this.
    traverseMLQAlgoDivs();
  }

  rr_qt.classList.toggle("d-none", !isRR);

  delete_divs = document.querySelectorAll(".btn-close");
  deleteAlgoLevel();
}

function traverseMLQAlgoDivs() {
  mlq_algorithms.forEach((mlq_algorithm) => {
    if (mlq_algorithm.value.includes("Priority")) {
      isPriority = true;
      priority.classList.remove("d-none");
    }
    mlq_algorithm.addEventListener("change", () => {
      // every time any of the mlq_algorithm select element gets their value changed, the program goes through all the mlq_algorithm select elements until it finds that one of the select elements has a value of Priority, then removes d-none. If it hasn't found any, it adds d-none back.
      checkPrio();
    });
  });
}

function checkPrio() {
  let i;

  for (i = 0; i < mlq_algorithms.length; i++) {
    if (mlq_algorithms[i].value.includes("Priority")) {
      isPriority = true;
      priority.classList.remove("d-none");
      break; // exit the loop
    }
  }
  if (i == mlq_algorithms.length) {
    isPriority = false;
    priority.classList.add("d-none");
  }
}

let globalFormData = {};
user_input_form.addEventListener("submit", async (e) => {
  e.preventDefault();

  loadingAnimation.classList.remove("d-none");

  let bt_length;

  let isValid = /^(\d+|0|\s)+$/;
  let toNumbers = /\b(?:0|[1-9]\d*)\b/g;
  let AT = document.querySelector("#arrival_time").value;
  let BT = document.querySelector("#burst_time").value;
  if (isValid.test(AT) && isValid.test(BT)) {
    let numbers1 = AT.match(toNumbers);
    let numbers2 = BT.match(toNumbers);
    let arrival_time = numbers1.map(Number);
    let burst_time = numbers2.map(Number);

    bt_length = burst_time.length;

    if (arrival_time.length !== bt_length) {
      alert("Arrival time and burst time lengths should be the same");

      loadingAnimation.classList.add("d-none");

      return;
    }
  } else {
    alert("Inputs should only contain numbers or spaces.");

    loadingAnimation.classList.add("d-none");

    return;
  }

  if (isPriority) {
    let P = document.querySelector("#priorityInput").value;
    if (!isValid.test(P)) {
      alert("Invalid input in Priority field.");

      loadingAnimation.classList.add("d-none");

      return;
    }
    let PNumbers = P.match(toNumbers);
    let priority = PNumbers.map(Number);

    if (priority.length !== bt_length) {
      alert("Priority and burst time lengths should be the same");
      console.log(priority.length, burst_time.length);

      loadingAnimation.classList.add("d-none");

      return;
    }
  }

  const mlqAlgorithmValues = Array.from(
    mlq_algorithms,
    (algorithm) => algorithm.value
  );

  if (isMLQ) {
    let L = document.querySelector("#levelInput").value;
    if (!isValid.test(L)) {
      alert("Invalid input in Level field.");

      loadingAnimation.classList.add("d-none");

      return;
    } else {
      let numbers = L.match(toNumbers);
      let levels = numbers.map(Number);

      if (levels.length !== bt_length) {
        alert("Level and burst time lengths should be the same");

        loadingAnimation.classList.add("d-none");

        return;
      }

      if (Math.max(...levels) > mlqAlgorithmValues.length) {
        alert(
          "Make sure the maximum number in the Level input field does not exceed the total number of MLQ algorithms."
        );

        loadingAnimation.classList.add("d-none");

        return;
      }
    }
  }

  const mlfq_quantum_times = document.querySelectorAll(".mlfq_quantum_time");
  const mlfq_qt = [];

  // Iterate through each input element and store its value in the array
  mlfq_quantum_times.forEach((qt) => {
    mlfq_qt.push(parseInt(qt.value));
  });

  let formData = {
    main_algorithm: main_algorithm.value,
    arrival_time: document.querySelector("#arrival_time").value,
    burst_time: document.querySelector("#burst_time").value,
    priority: document.querySelector("#priorityInput").value || null,
    quantum_time: document.querySelector("#quantum_time").value || null,
    mlfq_qt: mlfq_qt || [],
    mlfq_algorithm: mlfq_algorithm.value || null,
    mlq_algorithms: mlqAlgorithmValues || [],
    level: document.querySelector("#levelInput").value || null,
  };

  if (!isPriority) {
    delete formData.priority;
  }
  if (!isRR) {
    delete formData.quantum_time;
  }
  if (!isMLQ) {
    delete formData.mlq_algorithms;
    delete formData.level;
  }
  if (!isMLFQ) {
    delete formData.mlfq_qt;
    delete formData.mlfq_algorithm;
  }

  globalFormData = formData;

  try {
    console.log(formData);
    const response = await fetch("/sendInputCPUScheduling", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formData),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const data = await response.json();
    // console.log(timestamps);
    // console.log(processNumbers);
    // console.log(processesList);

    loadingAnimation.classList.add("d-none");

    constructResults(data.data);
  } catch (error) {
    console.error("Error: ", error);
  }
});

const data_container = document.querySelector("#data_container");
const results_container = document.querySelector("#results_container");
function constructResults(results) {
  if (!isMLFQ) {
    const [timestamps, processNumbers, processesList] = results;

    createGanttChart(timestamps, processNumbers, globalFormData.main_algorithm);
    createTable(processesList);
  } else {
    const [
      timestamps,
      processNumbers,
      processesList,
      mlfqTimestamps,
      mlfqOrderOfProcesses,
    ] = results;

    createGanttChart(timestamps, processNumbers, globalFormData.main_algorithm);

    // mlfqTimestamps.length contains the number of timestamps and orderOfProcesses queues, therefore referring to the number of levels in mlfq
    for (let i = 0; i < mlfqTimestamps.length; i++) {
      if (i == mlfqTimestamps.length - 1) {
        createGanttChart(
          mlfqTimestamps[i],
          mlfqOrderOfProcesses[i],
          `Level ${i + 1} Algorithm = ${globalFormData.mlfq_algorithm}`
        );
      } else {
        createGanttChart(
          mlfqTimestamps[i],
          mlfqOrderOfProcesses[i],
          `Level ${i + 1} Time Slice = ${globalFormData.mlfq_qt[i]}`
        );
      }
    }
    createTable(processesList);
  }
}

let lastTimeStamp;
function createGanttChart(timestamps, processNumbers, algorithm) {
  const main_algo_label = document.createElement("label");
  if (algorithm.includes("RoundRobin")) {
    main_algo_label.textContent = `${algorithm} (Quantum Time: ${globalFormData.quantum_time})`;
  } else if (algorithm.includes("MLQ")) {
    main_algo_label.textContent = `${algorithm} ( `;
    for (let i = 0; i < globalFormData.mlq_algorithms.length; i++) {
      main_algo_label.textContent += `${i + 1}: ${
        globalFormData.mlq_algorithms[i]
      } `;
    }
    main_algo_label.textContent += `)`;
  } else if (algorithm === "MLFQ") {
    main_algo_label.textContent = `${algorithm} (Combined Gantt Charts)`;
  } else {
    main_algo_label.textContent = algorithm;
  }
  main_algo_label.classList.add("d-block", "mt-4");
  results_container.append(main_algo_label);

  let i;
  processNumbers.push("P0");
  for (i = 0; i < processNumbers.length; i++) {
    const processDiv = document.createElement("div");
    processDiv.classList.add(
      "border-start",
      "py-4",
      "d-inline-block",
      "process_num_block",
      "my-4"
    );
    processDiv.textContent =
      processNumbers[i] === " " ? "__" : processNumbers[i];
    // processDiv.style.position = "relative";
    results_container.appendChild(processDiv);

    const timeSpan = document.createElement("span");
    timeSpan.textContent = timestamps[i];
    timeSpan.style.position = "absolute";
    timeSpan.style.bottom = "-20px";
    timeSpan.style.left = "-5px";
    processDiv.appendChild(timeSpan);

    if (i == processNumbers.length - 1) {
      processDiv.style.visibility = "hidden";
      timeSpan.style.visibility = "visible";
      lastTimeStamp = timestamps[i];
    }
  }
}

function createTable(processesList) {
  const headers = ["Processes", "Arrival", "Burst"];
  if (isPriority && isMLQ) {
    headers.push("Priority", "Level");
  } else if (isPriority) {
    headers.push("Priority");
  } else if (isMLQ) {
    headers.push("Level");
  }
  headers.push("Ending", "Turnaround", "Waiting");

  const table = document.createElement("table");
  table.classList.add("table", "table_color", "mt-3");

  const thead = document.createElement("thead");
  const tr = document.createElement("tr");

  for (let i = 0; i < headers.length; i++) {
    const th = document.createElement("th");
    th.classList.add("header_color", "text-center");
    th.setAttribute("scope", "col");
    th.textContent = headers[i];

    tr.append(th);
  }

  thead.append(tr);
  table.append(thead);

  const tbody = document.createElement("tbody");

  for (let i = 0; i < processesList.length; i++) {
    const tr = document.createElement("tr");
    for (let j = 0; j < processesList[i].length; j++) {
      const td = document.createElement("td");
      td.classList.add("table_color", "text-center");
      td.textContent = processesList[i][j];

      tr.append(td);
    }
    tbody.append(tr);
  }

  table.append(tbody);

  results_container.append(table);

  displayEfficiency(processesList);
}

function displayEfficiency(processesList) {
  let turnaround,
    waiting,
    burst = 2;
  if (isPriority && isMLQ) {
    turnaround = 6;
  } else if (isPriority || isMLQ) {
    turnaround = 5;
  } else {
    turnaround = 4;
  }
  waiting = turnaround + 1;

  let CPUUtilization = 0;
  let aveTT = 0;
  let aveWT = 0;

  for (let i = 0; i < processesList.length; i++) {
    CPUUtilization += processesList[i][burst];
    aveTT += processesList[i][turnaround];
    aveWT += processesList[i][waiting];
  }
  CPUUtilization /= lastTimeStamp;
  CPUUtilization = Math.round(CPUUtilization * 10000) / 100;
  aveTT /= processesList.length;
  aveWT /= processesList.length;

  const efficiencyDiv = document.createElement("div");
  efficiencyDiv.classList.add("efficiency_div");
  const utilizationSpan = document.createElement("span");
  const aveTTSpan = document.createElement("span");
  const aveWTSpan = document.createElement("span");

  utilizationSpan.textContent = `CPU Utilization: ${CPUUtilization}%`;
  aveTTSpan.textContent = `Average Turnaround Time: ${aveTT}`;
  aveWTSpan.textContent = `Average Waiting Time: ${aveWT}`;

  efficiencyDiv.append(utilizationSpan);
  efficiencyDiv.append(aveTTSpan);
  efficiencyDiv.append(aveWTSpan);
  results_container.append(efficiencyDiv);
}
