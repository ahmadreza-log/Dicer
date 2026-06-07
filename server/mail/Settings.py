# Outbound email settings for verification codes and notifications.


class Settings:
    TestMode = True
    Enabled = False
    Host = "127.0.0.1"
    Port = 587
    Username = ""
    Password = ""
    FromAddress = "noreply@dicer.local"
    FromName = "Dicer"
    UseTls = True
