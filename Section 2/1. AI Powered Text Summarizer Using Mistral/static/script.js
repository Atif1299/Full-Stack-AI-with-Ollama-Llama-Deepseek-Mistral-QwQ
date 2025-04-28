async function summarizeText() {
  let inputText = document.getElementById('text-input').value
  let summaryDiv = document.getElementById('summary')

  let formData = new FormData()
  formData.append('text', inputText)

  let response = await fetch('/summarize', {
    method: 'POST',
    body: formData,
  })

  if (!response.ok) {
    summaryDiv.innerHTML =
      "<p style='color: red;'>Error: Failed to fetch summary.</p>"
    return
  }

  let data = await response.json()
  summaryDiv.innerHTML = `<p>${data.summary}</p>`
}
