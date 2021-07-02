
function buildCharts() {
    const JData = JSON.parse(data)
    let config = []
    for (let key1 in JData) {
        if (JData[key1]['answer_type'] === 'closed') {
            let conf = {
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
                                'rgb(170,4,231)',
                                'rgb(4,231,223)',
                                'rgb(245,2,156)',
                                'rgb(57,2,248)',
                            ],
                        }
                    ]
                },
            }
            for (let key2 in JData[key1]['data']) {
                for (let key3 in JData[key1]['data'][key2]) {
                    conf['data']['labels'].push(key3)
                    conf['data']['datasets'][0]['data'].push(JData[key1]['data'][key2][key3])
                }
            }

            config[key1] = conf
        }

    }
    for (let key in config) {
        let ctx = $("#myChart" + key);
        let myChart = new Chart(ctx, config[key]);
    }
}

$(function () {
    buildCharts();
});

