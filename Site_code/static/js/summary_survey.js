
$(function () {
    const JData = JSON.parse(data)
    let config= []
    for (var key1 in JData) {
        if(JData[key1]['answer_type'] == 'closed'){
           var conf = {
            type: 'doughnut',
            data: {
                labels: [],
                datasets: [
                    {
                        data: [],
                        backgroundColor: [
                            'rgb(255, 99, 132)',
                            'rgb(54, 162, 235)',
                            'rgb(255, 205, 86)',
                            'rgb(248,66,19)',
                            'rgb(56,231,4)',
                        ],
                    }
                    ]
                },
            }
            for (var key2 in JData[key1]['data']) {
                for (var key3 in JData[key1]['data'][key2]) {
                    conf['data']['labels'].push(key3)
                    conf['data']['datasets'][0]['data'].push(JData[key1]['data'][key2][key3])
                }
            }

        config[key1] = conf
        }

   }
    for (var key in config) {
        var name = "myChart"+key
        var ctx = document.getElementById(name).getContext('2d');
        var myChart =new Chart(ctx, config[key]);
    }



});

