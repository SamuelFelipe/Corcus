function makeGetRequest(e, form) {
  e.preventDefault()
  let dict = {}
  for (const pair of new FormData(form)) {
    dict[pair[0]] = pair[1]
  }
  let headers = new Headers()
  headers.append('Content-Type', 'application/json')
  const req = new Request('http://127.0.0.1:5000/api/signup', {
    method: 'POST',
    headers: headers,
    body: JSON.stringify(dict)
  })
  fetch(req).then(response => {
    if (response.status === 201){
      return response.json()
    } else {
      return null
    }
  }).then(data => {
    if (data != null) {
      sessionStorage.setItem('token', data.auth_token)
      location.replace('/app')
    }
  })
}

const form = document.querySelector('#signup')

if (form) {
  form.addEventListener('submit', function(e) {
    makeGetRequest(e, form)
  })
}
