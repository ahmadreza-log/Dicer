# Database connection settings for the Dicer central server.
# Type is set to MySQL for now; additional drivers can be added later.


class Settings:
    # Master switch for database connectivity.
    Enabled = True

    # Database engine type (MySQL only for now).
    Type = "MySQL"

    # MySQL server hostname or IP address.
    Host = "127.0.0.1"

    # MySQL server port.
    Port = 3306

    # MySQL username.
    User = "root"

    # MySQL password.
    Password = ""

    # MySQL database (schema) name.
    Name = "dicer"
