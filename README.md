# aws-aurora-db

Script de ejemplo para conectarse a una base de datos **Amazon Aurora (MySQL)** usando **AWS IAM Database Authentication** en lugar de una contraseña tradicional.

En vez de guardar una contraseña de base de datos, el script le pide a AWS un token de acceso temporal (válido 15 minutos) usando tus credenciales de IAM, y lo usa para autenticarse. Así no hay contraseñas de base de datos que administrar ni rotar.

## Requisitos previos

- [uv](https://docs.astral.sh/uv/) instalado.
- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) configurado con un usuario/rol IAM que tenga permiso `rds-db:connect` sobre el usuario de base de datos correspondiente.
- Un usuario de base de datos creado con autenticación IAM habilitada (`IDENTIFIED WITH AWSAuthenticationPlugin AS 'RDS'`), con los privilegios que necesites.
- El certificado raíz de Amazon RDS (`global-bundle.pem`), necesario para la conexión TLS. Descárgalo así:

  ```bash
  curl -o global-bundle.pem https://truststore.pki.rds.amazonaws.com/global/global-bundle.pem
  ```

## Instalación

Clona el repositorio e instala las dependencias con `uv`:

```bash
git clone <url-del-repo>
cd aws-aurora-db
uv sync
```

## Configuración

Las credenciales y datos de conexión **no van en el código**, sino en un archivo `.env` en la raíz del proyecto (este archivo está en `.gitignore` y nunca se sube al repositorio).

Copia la plantilla de ejemplo y complétala con tus propios datos:

```bash
cp .env.example .env
```

Edita `.env` con los valores de tu instancia de Aurora:

```env
DB_HOST=tu-cluster.cluster-xxxxxxxx.us-east-1.rds.amazonaws.com
DB_PORT=3306
DB_NAME=mysql
DB_USER=tu_usuario_iam
AWS_REGION=us-east-1
SSL_CA=./global-bundle.pem
```

## Uso

Con `.env` y `global-bundle.pem` en su lugar, ejecuta:

```bash
uv run main.py
```

Si todo está bien configurado (permisos de IAM, security group de la base de datos y usuario con autenticación IAM habilitada), el script se conecta y muestra la versión del motor de la base de datos.

## Notas de seguridad

- Nunca subas al repositorio los archivos `.env` ni `*.pem` — ambos están excluidos vía `.gitignore`.
- El token de autenticación se genera al vuelo en cada ejecución y expira a los 15 minutos; no se almacena en ningún lado.
