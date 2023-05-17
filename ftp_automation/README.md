# Citibank FTP Automation Tool

O script em questão tem a finalidade de automatizar o processo de download dos arquivos de retorno e upload dos arquivos de remessa para o Citibank.
As etapas que consistem no processo são as seguintes:
- Conecta no FTP server;
- Verifica se há arquivos disponíveis no diretório /mailbox e faz o download para o local path D:\Conectividade_CITI\Download;
- Verifica se os arquivos estão no formato esperado

# Requisitos para funcionamento correto do script:
    WinPG (https://gnupg.org/download/index.html ver 4.1.0)
    boto3 Python library
        A library necessita de acesso a internet (0.0.0.0/0 porta 443) para fucionamento correto

# Permissões necessárias:
    - A library boto3 necessita de acesso a internet (0.0.0.0/0) através da porta 443
    - Necessário criar IAM role que permita o GET no secrets manager que hospeda as senhas utilizadas


Sintaxe não interativas utilizadas

```PowerShell
Decrypt# gpg --batch --pinentry-mode=loopback --yes --passphrase <passphrase> --decrypt -o <full-path-decrypted-file> <full-path-encrypted-file>
Encrypt# gpg --batch --pinentry-mode=loopback --yes --recipient <recipient-name> --encrypt -o <full-path-encrypted-file> <full-path-decrypted-file>
```
Mapa de variáveis

source_path = Local onde os arquivos são armazenados após o download do FTP Citi
staging_path = Local onde os arquivos são descriptografados
destination_path = Local definitivo onde os arquivos são armazenados para processamento



Funções:
    * file_ops.file_fmt_chk()
        ** Retorna um dicionário:
```Python
checked_files = {'chk_pass': [], 'chk_fail': []}
```


Testing Server
'''
#  FTP Server information - Testing
citi_ftp_homolog = {'host': 'test.rebex.net',
                 'user': 'demo',
                 'pass': 'password',
                 'down_dir': '/pub/example/'}
'''