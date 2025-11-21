import os
import re
from logging.handlers import RotatingFileHandler


class FriendlyRotatingFileHandler(RotatingFileHandler):
    """
    file.log -> file(1).log -> file(2).log -> ...
    """

    pattern = re.compile(r"^(.*)\((\d+)\)\.log$")

    def rotate(self, source, dest):
        # source: /path/file.log
        # dest:   /path/file.log.1

        base = os.path.dirname(source)
        original_name = os.path.basename(source)

        name_without_ext, _ = os.path.splitext(original_name)

        existing = []
        for f in os.listdir(base):
            match = self.pattern.match(f)
            if match and match.group(1) == name_without_ext:
                existing.append(int(match.group(2)))

        next_index = 1 if not existing else max(existing) + 1

        new_name = f"{name_without_ext}({next_index}).log"
        new_path = os.path.join(base, new_name)

        os.replace(source, new_path)
