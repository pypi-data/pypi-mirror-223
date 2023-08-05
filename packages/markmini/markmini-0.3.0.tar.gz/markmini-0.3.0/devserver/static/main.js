const input = document.getElementById("input");
const output_html = document.getElementById("output_html");
const output_raw = document.getElementById("output_raw");

input.oninput = async (e) => {
  const val = input.value;
  const res = await fetch("/mdcompile", {
    "body": JSON.stringify({ "input": val }),
    "method": "POST",
    headers: { "content-type": "application/json" },
  })
  const data = await res.json();
  output_html.innerHTML = data;
  output_raw.textContent = data;
}
