from subprocess import run, PIPE
from ui import input_word, input_secret, input_choice
from utils import cat, bash_lines
import templates

def timezones() -> list[str]:
    return bash_lines(templates.TIMEZONES)

class Preferences:
    hostname: str
    username: str
    password: str
    timezone: str

    @classmethod
    def from_input(cls):
        preferences = Preferences()
        preferences.hostname = input_word('Hostname')
        preferences.username = input_word('Username')
        preferences.password = input_secret('Password')
        preferences.timezone = input_choice('Timezone', timezones())
        return preferences

    def script(self):
        return cat([
            templates.SETUP_HOST.substitute(hostname=self.hostname),
            templates.SETUP_TIMEZONE.substitute(timezone=self.timezone),
            templates.SETUP_USER.substitute(
                name=self.username,
                password=self.password),
        ], 2)
