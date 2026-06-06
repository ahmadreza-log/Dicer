from cli.Manager import Manager


class Rules:
    # Shared validation rules for settings that require a stopped server.

    @staticmethod
    def RequireStop(manager: Manager) -> tuple[bool, str]:
        if manager.IsActive():
            return False, "Stop the server before changing this setting."

        return True, ""
