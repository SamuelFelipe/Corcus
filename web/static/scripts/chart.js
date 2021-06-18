let ctx1 = document.getElementById('payroll')
let ctx2 = document.getElementById('eps')
let ctx3 = document.getElementById('others')


function getData() {
  let headers = new Headers()
  headers.append('Content-Type', 'application/json')
  headers.append('Authorization', 'Basic '
    + btoa(sessionStorage.getItem('token') + ':unused'))
  const req = new Request('http://127.0.0.1:5000/api/employees', {
    method: 'GET',
    headers: headers,
    mode: 'cors'
  })
  fetch(req)
  .then(response => {
    console.log(response)
    return response.ok ? response.json() : Promise.reject(response);
  })
  .then(data => {
    console.log(1)
    if (data) {
      let payment = 0
      let arl = 0
      let health = 0
      let pension = 0
      let p_f = 0
      let cesantias = 0
      let in_cesantias = 0
      let eps_list = []
      let epss = {}
      for (let i in data){
        arl += data[i]['arl']
        payment += data[i]['salary']
        health += data[i]['health']
        pension += data[i]['pension']
        p_f += data[i]['parafiscales']
        cesantias = data[i]['cesantias']
        in_cesantias = data[i]['in_cesantias']
        if (eps_list.indexOf(data[i]['eps']) === -1) {
          eps_list.push(data[i]['eps'])
          epss[data[i]['eps']] = 1
        } else {
          epss[data[i]['eps']] += 1
        }
      }
      if (payment === 0) {
        payment += 1
      }
      var myChart = new Chart(ctx1, {
        type: 'doughnut',
        data: {
          labels: ['Salarios', 'ARL', 'Salud', 'Pension',
                   'Parafiscales'],
          datasets: [{
            data: [payment, arl, health, pension, p_f],
            backgroundColor: [
              'rgb(242, 65, 80)',
              'rgb(166, 93, 154)',
              'rgb(66, 44, 89)',
              'rgb(242, 229, 41)',
              'rgb(242, 121, 121)',
            ],
            borderColor: [
              'rgb(242, 65, 80)',
              'rgb(166, 93, 154)',
              'rgb(66, 44, 89)',
              'rgb(242, 229, 41)',
              'rgb(242, 121, 121)',
            ],
            borderWidth: 1
          }]
        },
      });
      let count = []
      let employees = 0
      for (let i in epss) {
        count.push(epss[i])
        employees += 1
      }
      var chart = new Chart(ctx2, {
        type: 'bar',
        data: {
          labels: eps_list,
          datasets: [{
            data: count,
            backgroundColor: [
              'rgb(60, 0, 89)',
              'rgb(153, 0, 230)',
              'rgb(102, 0, 153)',
              'rgb(111, 0, 166)',
              'rgb(85, 0, 128)',
              'rgb(57, 48, 115)',
            ],
            borderColor: [
              'rgb(60, 0, 89)',
              'rgb(153, 0, 230)',
              'rgb(102, 0, 153)',
              'rgb(111, 0, 166)',
              'rgb(85, 0, 128)',
              'rgb(57, 48, 115)',
            ],
          }]
        }
      })
      var myChart = new Chart(ctx3, {
        type: 'doughnut',
        data: {
          labels: ['Cesantias', 'ARL', 'Salud', 'Pension', 'Parafiscales'],
          datasets: [{
            data: [(cesantias + in_cesantias), arl, health, pension, p_f],
            backgroundColor: [
              'rgb(242, 65, 80)',
              'rgb(166, 93, 154)',
              'rgb(66, 44, 89)',
              'rgb(242, 229, 41)',
              'rgb(242, 121, 121)',
            ],
            borderColor: [
              'rgb(242, 65, 80)',
              'rgb(166, 93, 154)',
              'rgb(66, 44, 89)',
              'rgb(242, 229, 41)',
              'rgb(242, 121, 121)',
            ],
            borderWidth: 1
          }]
        },
      });
    }
  })
  .catch(err => {
    console.log(err)
    console.error(`Error ${err.status} ${err.statusText || 'ocurrio un error'}`)
  })
}

getData()
