async function sendMessage() {
  let inputField = document.getElementById('user-input')
  let chatBox = document.getElementById('chat-box')

  let userMessage = inputField.value
  chatBox.innerHTML += `<p><strong>You:</strong> ${userMessage}</p>`
  inputField.value = ''

  let response = await fetch(
    `/chat?prompt=${encodeURIComponent(userMessage)}`,
    {
      method: 'POST',
    }
  )

  if (!response.ok) {
    chatBox.innerHTML += `<p><strong>AI:</strong> Error: Failed to fetch response.</p>`
    return
  }

  let data = await response.json()
  chatBox.innerHTML += `<p><strong>AI:</strong> ${data.response}</p>`
  chatBox.scrollTop = chatBox.scrollHeight
}
