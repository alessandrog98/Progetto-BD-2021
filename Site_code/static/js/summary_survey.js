const data = {
          labels: [
            'Red',
            'Blue',
            'Yellow'
          ],
          datasets: [{
            label: 'My First Dataset',
            data: [300, 50, 100],
            backgroundColor: [
              'rgb(255, 99, 132)',
              'rgb(54, 162, 235)',
              'rgb(255, 205, 86)'
            ],
            hoverOffset: 4
          }]
        };
const config = {
      type: 'doughnut',
      data: data,
};

class chart {
    constructor(Object) {
        this.$config = {
            type: object.type,
            data: data,
        }
        this.$chart = null;
        this.$container = null;
        this.draw();
    }

    draw() {
        let html =''
        html += '<div><canvas id=></canvas></div>'
        this.$container = $(html);
        this.$chart = this.$container.find(".chart");
    }
}


$(function () {

    $('#itemsContainer').append(topAddButton.$container);




});

var myChart = new Chart(document.getElementById('myChart'), config);