const body = document.body;
let instance = 1;

document
  .querySelector("#disk_scheduling_input_form")
  .addEventListener("submit", async (e) => {
    e.preventDefault();

    let isValid = /^(\d+|0|\s)+$/;
    let toNumbers = /\b(?:0|[1-9]\d*)\b/g;
    let diskSchedulingAlgorithm = document.querySelector(
      "#disk_scheduling_algorithm"
    ).value;
    let DR = document.querySelector("#disk_requests").value;
    let NOC = document.querySelector("#number_of_cylinders").value;

    if (NOC < 1) {
      alert("Number of cylinders should be greater than 0.");

      return;
    }

    if (isValid.test(DR)) {
      let diskRequests = DR.match(toNumbers);

      diskRequests = diskRequests.map(Number);

      if (Math.max(...diskRequests) >= NOC) {
        alert(
          "The max number in disk requests must not exceed or be equal to the number of cylinders."
        );

        return;
      }

      let formData = {
        diskSchedulingAlgorithm,
        diskRequests,
        numberOfCylinders: NOC,
      };

      try {
        console.log("This is formData: ", formData);

        const response = await fetch("/sendInputDiskScheduling", {
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

        console.log("This is the returned data: ", returnedData);
        constructdiskSchedulingResults(returnedData);

        // constructdiskSchedulingResults(
        //   diskSchedulingAlgorithm,
        //   diskRequests,
        //   returnedData
        // );
      } catch (error) {
        console.error("Error: ", error);
      }
    } else {
      alert("Disk requests inputs should only contain numbers or spaces.");

      return;
    }
  });

function constructdiskSchedulingResults(returnedData) {
  //   diskSchedulingAlgorithm,
  //   diskRequests,
  //   returnedData
  const { diskSchedulingAlgorithm, diskRequests, numberOfCylinders } =
    returnedData;
  const div = document.createElement("div");
  const canvas = document.createElement("canvas");
  div.classList.add("mx-5", "mt-5");
  canvas.id = `myChart-${instance}`;

  div.append(canvas);
  body.append(div);

  const ctx = document.getElementById(`myChart-${instance}`);

  new Chart(ctx, {
    type: "line",
    data: {
      labels: diskRequests,
      datasets: [
        {
          label: diskSchedulingAlgorithm,
          data: diskRequests,
        },
      ],
    },
    options: {
      scales: {
        y: {
          beginAtZero: true,
        },
      },
    },
  });

  instance++;
}
