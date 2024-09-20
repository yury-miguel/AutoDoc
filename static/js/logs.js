function buscarLogs() {
    const data = document.getElementById('logDateFilter').value;

    fetch('/Logs', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
            'logDateFilter': data
        })
    })
    .then(response => response.text())
    .then(html => {
        document.body.innerHTML = html;
    })
    .catch(error => console.error('Erro ao buscar logs:', error));
}


function exportarLogs() {
    const data = document.getElementById('logDateFilter').value;

    fetch('/exportar_logs', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
            'logDateFilter': data
        })
    })
    .then(response => response.blob())
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'logs_filtrados.txt';
        document.body.appendChild(a);
        a.click();
        a.remove();
    })
    .catch(error => console.error('Erro ao exportar logs:', error));
}