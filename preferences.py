from typing import Optional
from subprocess import run, PIPE
from ui import input_word, input_secret, input_choice
from utils import concat, bash_lines
import templates

def timezones() -> list[str]:
    return bash_lines(templates.TIMEZONES)

class Preferences:
    hostname: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    timezone: Optional[str] = None

    @classmethod
    def from_dict(cls, obj: dict):
        pref = Preferences()
        pref.hostname = obj.get('hostname')
        pref.username = obj.get('username')
        pref.password = obj.get('password')
        pref.timezone = obj.get('timezone')
        return pref

    def input_missing(self):
        if not self.hostname:
            self.hostname = input_word('Hostname')
        if not self.username:
            self.username = input_word('Username')
        if not self.password:
            self.password = input_secret('Password')
        if not self.timezone:
            self.timezone = input_choice('Timezone', timezones())

    def root_script(self):
        return concat([
            templates.SETUP_HOST.substitute(hostname=self.hostname),
            templates.SETUP_USER.substitute(
                name=self.username,
                password=self.password),
        ], 2)

    def user_script(self):
        return concat([
            templates.SETUP_LOCALE,
            templates.SETUP_TIMEZONE.substitute(timezone=self.timezone),
        ], 2)
