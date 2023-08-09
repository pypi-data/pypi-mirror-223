class MissingOrEmptyField(Exception):
    """Required field in configuration is missing or empty."""

    def __init__(self, section, field):
        super().__init__(
            f"Configuration error in section {section}: field {field!r} is required and must not be empty"  # noqa
        )
        self.section = section
        self.field = field


class EmptyOrUnsetEnvVar(Exception):
    """Environment variable set in configuration is unset or empty."""

    def __init__(self, section, var):
        super().__init__(
            f"Configuration error in section {section}: environment variable {var!r} is not set or empty"  # noqa
        )
        self.section = section
        self.var = var
