if (sessionStorage.getItem('token') === null) {
  location.replace('/login')
}

function tokenRequest() {
  let headers = new Headers()
  headers.append('Content-Type', 'application/json')
  headers.append('Authorization', 'Basic '
    + btoa(sessionStorage.getItem('token') + ':unused'))
  const req = new Request('http://127.0.0.1:5000/api/token', {
    method: 'GET',
    headers: headers,
    mode: 'cors'
  })
  fetch(req).then(response => {
    if (response.ok) {
      return response.json()
    } else {
      location.replace('/login')
    }
  }).then(data => {
    sessionStorage.setItem('token', data.token)
  })
}

tokenRequest()

setInterval(tokenRequest, 800000)
