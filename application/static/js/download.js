let btnGenerate = document.querySelector('#generate-image');
let btnDownload = document.querySelector('.download');
var dateNow = Date.now();

btnGenerate.addEventListener('click', () =>  {
    html2canvas(document.querySelector("#wapper")).then(canvas => {
        btnDownload.href = canvas.toDataURL('image/png');
        btnDownload.download = dateNow;
        btnDownload.click();
    })
});