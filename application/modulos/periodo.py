from datetime import datetime

def saudacao():
    horario = str(datetime.now().strftime('%H:%M:%S'))
    if horario < '12:00:00':
        testesaudacao = "Bom dia"
    elif horario > '12:00:00' and horario < '18:00:00':
        testesaudacao = "Boa tarde"
    else:
        testesaudacao = "Boa Noite"
        
    return testesaudacao
