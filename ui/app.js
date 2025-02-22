const getData = async (url, isJson) => {
    let resultElement = document.getElementById("greetingResult");
  
    try {
      let response = await axios.get(url);
      resultElement.innerHTML = displayResults(response, isJson);
    } catch (error) {
      resultElement.innerHTML = displayError(error);
    }
  };
  
  const tellJoke = async (e) => {
    e.preventDefault();
    let resultElement = document.getElementById("jokeResult");
    let payload = document.getElementById("topicPayload").value;
  
    try {
      let response = await axios.post("http://localhost:5000/v1/joke", payload, {
        headers: {
          "content-type": "application/json",
        },
      });
      resultElement.innerHTML = displayResults(response, true);
    } catch (error) {
      resultElement.innerHTML = displayError(error);
    }
  };

  const showProducts = async (e) => {
    e.preventDefault();
    let resultElement = document.getElementById("productsResult");
    let payload = document.getElementById("categoryPayload").value;
  
    try {
      let response = await axios.post("http://localhost:5000/v1/products", payload, {
        headers: {
          "content-type": "application/json",
        },
      });
      resultElement.innerHTML = displayResults(response, true);
    } catch (error) {
      resultElement.innerHTML = displayError(error);
    }
  };

  const answerQuestion = async (e) => {
    e.preventDefault();
    let resultElement = document.getElementById("ragResult");
    let payload = document.getElementById("questionPayload").value;
  
    try {
      let response = await axios.post("http://localhost:5000/v1/queryPDF", payload, {
        headers: {
          "content-type": "application/json",
        },
      });
      resultElement.innerHTML = displayResults(response, true);
    } catch (error) {
      resultElement.innerHTML = displayError(error);
    }
  };
  
  const displayResults = (response, isJson) => {
    const encodeXml = (xml) => {
      return xml
        .replace(/&/g, "&amp;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&apos;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/\t/g, "&#x9;")
        .replace(/\n/g, "&#xA;")
        .replace(/\r/g, "&#xD;");
    };
    return `<h4>Result:</h4>
          <h5>Status:</h5>
          <pre>${response.status} ${response.statusText}</pre>
          <h5>Headers:</h5>
          <pre>${JSON.stringify(response.headers, null, "\t")}</pre>
          <h5>Data:</h5>
          <pre>${
            isJson
              ? JSON.stringify(response.data, null, "\t")
              : encodeXml(response.data)
          }</pre>
          `;
  };
  
  const displayError = (error) => {
    return `<h4>Result:</h4>
          <h5>Message:</h5>
          <pre>${error.message}</pre>
          <h5>Status:</h5>
          <pre>${error.response.status} ${error.response.statusText}</pre>
          <h5>Headers:</h5>
          <pre>${JSON.stringify(error.response.headers, null, "\t")}</pre>
          <h5>Data:</h5>
          <pre>${JSON.stringify(error.response.data, null, "\t")}</pre>`;
  };
  
  const clearOutput = () => {
    let resultElement = document.getElementById("greetingResult");
    resultElement.innerHTML = "";
    resultElement = document.getElementById("jokeResult");
    resultElement.innerHTML = "";
    resultElement = document.getElementById("productsResult");
    resultElement.innerHTML = "";
    resultElement = document.getElementById("ragResult");
    resultElement.innerHTML = "";
  };
  
  document.getElementById("jokeForm").addEventListener("submit", tellJoke);
  document.getElementById("productsForm").addEventListener("submit", showProducts);
  document.getElementById("questionForm").addEventListener("submit", answerQuestion);
  