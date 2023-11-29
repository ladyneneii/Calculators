const formEncrypt = document.querySelector("#form_encrypt");
const formDecrypt = document.querySelector("#form_decrypt");
const encryptBtn = document.querySelector("#encrypt_btn");
const decryptBtn = document.querySelector("#decrypt_btn");
const decryptInfo = document.querySelector("#decrypt_info");
const privateKeyResult = document.querySelector("#private_key_result");
const modResult = document.querySelector("#mod_result");
const keywordResult = document.querySelector("#keyword_result");
const otpResult = document.querySelector("#otp_result");
const copyPrivateKeyBtn = document.querySelector("#copy_private_key");
const copyModBtn = document.querySelector("#copy_mod");
const copyKeywordBtn = document.querySelector("#copy_keyword");
const copyOtpBtn = document.querySelector("#copy_otp");

formEncrypt.addEventListener("submit", async (e) => {
  e.preventDefault();

  const fileToEncrypt = document
    .querySelector("#file_to_encrypt")
    .value.split("\\")
    .pop();
  const keywordEncrypt = document.querySelector("#keyword_encrypt").value;

  if (isTxtFile(fileToEncrypt)) {
    if (isValidKeyword(keywordEncrypt)) {
      console.log("Encrypting...");

      let formData = {
        fileToEncrypt: fileToEncrypt.replace(/\.txt$/, ""),
        keywordEncrypt,
        action: "encrypt",
      };

      try {
        console.log("This is formData: ", formData);

        const response = await fetch("/sendInputCryptography", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(formData),
        });

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const [cipher, privateKey, mod, keyword, otp] = await response.json();

        decryptInfo.classList.remove("d-none");
        privateKeyResult.value = privateKey;
        modResult.value = mod;
        keywordResult.value = keyword;
        otpResult.value = otp;

        const div = document.createElement("div");
        div.classList.add("alert", "alert-success");
        div.setAttribute("role", "alert");
        div.textContent = "Successfully created encrypted file.";

        // Insert the alert at the beginning of the body
        decryptInfo.insertBefore(div, decryptInfo.firstChild);

        // Set a timeout to remove the alert after 3 seconds
        setTimeout(() => {
          div.remove();
        }, 5000);

        formDecrypt.querySelectorAll("input").forEach((input) => {
          input.value = "";
        });
      } catch (error) {
        console.error("Error: ", error);
      }
    } else {
      alert("Keyword must be 10 characters or less.");

      return;
    }
  } else {
    alert("Please enter a .txt file.");

    return;
  }
});

formDecrypt.addEventListener("submit", async (e) => {
  e.preventDefault();

  const fileToDecrypt = document
    .querySelector("#file_to_decrypt")
    .value.split("\\")
    .pop();
  const privateKeyDecrypt = document.querySelector(
    "#private_key_decrypt"
  ).value;
  const modDecrypt = document.querySelector("#mod_decrypt").value;
  const keywordDecrypt = document.querySelector("#keyword_decrypt").value;
  const otpDecrypt = document.querySelector("#otp_decrypt").value;

  if (isTxtFile(fileToDecrypt)) {
    if (isValidKeyword(keywordDecrypt)) {
      console.log("Decrypting...");

      let formData = {
        fileToDecrypt: fileToDecrypt.replace(/\.txt$/, ""),
        privateKeyDecrypt,
        modDecrypt,
        keywordDecrypt,
        otpDecrypt,
        action: "decrypt",
      };

      try {
        console.log("This is formData: ", formData);

        const response = await fetch("/sendInputCryptography", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(formData),
        });

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const remark = await response.text();

        console.log(remark);

        const div = document.createElement("div");
        div.classList.add("alert", "alert-success");
        div.setAttribute("role", "alert");
        div.textContent = "Successfully created decrypted file.";

        // Insert the alert at the beginning of the body
        formDecrypt.insertBefore(div, formDecrypt.firstChild);

        // Set a timeout to remove the alert after 3 seconds
        setTimeout(() => {
          div.remove();
        }, 5000);
      } catch (error) {
        console.error("Error: ", error);

        const div = document.createElement("div");
        div.classList.add("alert", "alert-danger");
        div.setAttribute("role", "alert");
        div.textContent =
          "Cannot decrypt file because of wrong decrypting input/s.";

        // Insert the alert at the beginning of the body
        formDecrypt.insertBefore(div, formDecrypt.firstChild);

        // Set a timeout to remove the alert after 3 seconds
        setTimeout(() => {
          div.remove();
        }, 5000);
      }
    } else {
      alert("Keyword must be 10 characters or less.");

      return;
    }
  } else {
    alert("Please enter a .txt file.");

    return;
  }
});

formDecrypt.querySelectorAll("input").forEach((input) => {
  input.addEventListener("click", () => {
    input.value = "";
  });
});

const privateKeyDiv = document.querySelector(".private_key_div");
const modDiv = document.querySelector(".mod_div");
const keywordDiv = document.querySelector(".keyword_div");
const otpDiv = document.querySelector(".otp_div");

copyPrivateKeyBtn.addEventListener("click", () => {
  copyToClipboard(privateKeyResult, privateKeyDiv);
});

copyModBtn.addEventListener("click", () => {
  copyToClipboard(modResult, modDiv);
});

copyKeywordBtn.addEventListener("click", () => {
  copyToClipboard(keywordResult, keywordDiv);
});

copyOtpBtn.addEventListener("click", () => {
  copyToClipboard(otpResult, otpDiv);
});

function isTxtFile(fileName) {
  return fileName.endsWith(".txt");
}

function isValidKeyword(keyword) {
  return keyword.length <= 10;
}

function copyToClipboard(element, div) {
  // Select the text in the input
  element.select();
  navigator.clipboard.writeText(element.value);
  successfullyCopied(div);
}

function successfullyCopied(div) {
  const p = document.createElement("p");

  p.textContent = "Successfully copied.";
  p.classList.add("text-success", "mt-2", "position-absolute");
  div.append(p);

  setTimeout(() => {
    p.remove();
  }, 3000);
}
