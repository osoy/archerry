from subprocess import run, PIPE
from ui import input_word, input_secret, input_choice
import templates

def timezones() -> list[str]:
    proc = run(['bash', '-c', templates.TIMEZONES], stdout=PIPE)
    return proc.stdout.decode('utf-8').split('\n')[0:-1]

class Preferences:
    hostname: str
    username: str
    password: str
    timezone: str

    @classmethod
    def from_input(cls):
        preferences = Preferences()
        preferences.hostname = input_word('hostname')
        preferences.username = input_word('username')
        preferences.password = input_secret('password')
        preferences.timezone = input_choice('timezone', timezones())
        return preferences

    def script(self):
        return '\n\n\n'.join([
            templates.SETUP_HOST.substitute(hostname=self.hostname),
            templates.SETUP_TIMEZONE.substitute(timezone=self.timezone),
            templates.SETUP_USER.substitute(
                name=self.username,
                password=self.password),
        ])
