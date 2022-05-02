import pdfkit

# options = {
#     'page-size': 'Letter',
#     'orientation': 'Portrait',
#     'encoding': "UTF-8",
#     'custom-header': [
#         ('Accept-Encoding', 'gzip')
#     ],
#     'no-outline': None,
#     'javascript-delay': '60000'
# }

pdfkit.from_url('https://app.databox.com/datawall/e874523bd147efa17cfbb21414c8306b0597f3072', 'Relatorio.pdf')