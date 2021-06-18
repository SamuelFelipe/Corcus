function makeGetRequest(e, form) {
  e.preventDefault()
  let dict = {}
  let headers = new Headers()
  for (const pair of new FormData(form)) {
    dict[pair[0]] = pair[1]
  }
  headers.append('Content-Type', 'application/json')
  headers.append('Authorization', 'Basic '
    + btoa(dict['username'] + ':' + dict['password']))
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
    location.replace('/app')
  })
}

if (sessionStorage.getItem('token') != null){
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
    }
  }).then(data => {
    sessionStorage.setItem('token', data.token)
    location.replace('/app')
  })

}

const form = document.querySelector('#login')

if (form) {
  form.addEventListener('submit', function(e) {
    makeGetRequest(e, form)
  })
}
