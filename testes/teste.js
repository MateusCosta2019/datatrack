// let inputName = document.querySelector('.input__name');
// let inputDate = document.querySelector('.input__date');

// let previewName = document.querySelector('.preview__name--second');
// let previewDate = document.querySelector('.preview__date');

// inputName.addEventListener('keyup', () => {
//     previewName.innerHTML = inputName.value;
// });

// inputDate.addEventListener('change', () => {
//     previewDate.innerHTML = inputDate.value;
// });

let btnGenerate = document.querySelector('#generate-image');
let btnDownload = document.querySelector('.download');

btnGenerate.addEventListener('click', () =>  {
    html2canvas(document.querySelector(".preview")).then(canvas => {
        btnDownload.href = canvas.toDataURL('image/png');
        btnDownload.download =  'minha-imagem';
        btnDownload.click();
    })
});


var options = {
    chart: {
        type: 'line'
    },
    series: [{
        name: 'sales',
        data: [30,40,35,50,49,60,70,91,125]
    }],
    xaxis: {
        categories: [1991,1992,1993,1994,1995,1996,1997, 1998,1999]
    }
    }
var chart = new ApexCharts(document.querySelector("#MyCanvas"), options);
chart.render();
