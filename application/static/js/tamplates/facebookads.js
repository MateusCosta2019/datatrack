var options = {
    chart: {
        type: 'line'
        },
        series: [{
        name: 'Impressões',
        data: [0,0,0,7566,158352,139604,98,4,3]
        }],
        xaxis: {
        categories: ['JAN','FEV','MAR','ABR','MAI','JUN','JUL', 'AGO','SET']
        }
    }

    var chart = new ApexCharts(
    document.querySelector("#chart"),
    options
    );
    chart.render();

var options = {
    chart: {
        type: 'line'
        },
        series: [{
        name: 'Impressões',
        data: [10,590,0,566,1552,1394,98,4,3]
        }],
        xaxis: {
        categories: ['JAN','FEV','MAR','ABR','MAI','JUN','JUL', 'AGO','SET']
        }
    }

    var chart = new ApexCharts(
    document.querySelector("#chartCURTIDAS"),
    options
    );
    chart.render();