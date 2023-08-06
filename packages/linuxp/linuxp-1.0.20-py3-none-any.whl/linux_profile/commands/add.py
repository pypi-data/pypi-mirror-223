from linux_profile.base.file import File
from linux_profile.base.system import System
from linux_profile.base.action import Action
from linux_profile.base.settings import Settings
from linux_profile.utils.text import option
from linux_profile.validators import (
    InputAddPackage,
    InputAddAlias,
    InputAddScript,
    InputAddFile,
    InputAddText
)


class Add(Settings):

    def setup(self):
        """Defines the functions that are executed each
        time the class is instantiated.
        """
        self.command = self.__class__.__name__.lower()
        self.action = Action(
            str(self.path_profile.joinpath(self.file_profile)))

        func = self.join(value=[self.command, self.module], separator="_")
        getattr(self, func, self)()

    def add_package(self):
        fields = InputAddPackage(**{
            "tag": option(text="Package Tag [default]: "),
            "type": option(text="Package Manager: ", required=True),
            "name": option(text="Package Name: ", required=True),
            "version": option(text="Package Version: "),
            "url": option(text="Package URL: "),
            "file": option(text="Package File: "),
            "description": option(text="Package Description [limit 85]: ")}
        )
        for item in fields.generate_all():
            self.action._create_item(
                content=item,
                module=self.module,
                tag=fields.tag
            )

    def add_alias(self):
        fields = InputAddAlias(**{
            "tag": option(text="Alias Tag [default]: "),
            "name": option(text="Alias Name: ", required=True),
            "command": option(text="Alias Command: ", required=True),
            "body": option(text="Alias Body: ", required=True),
            "description": option(text="Package Description [limit 85]: "),
            "type": "exec"}
        )
        self.action._create_item(
            content=fields.__dict__,
            module=self.module,
            tag=fields.tag
        )

    def add_script(self):
        fields = InputAddScript(**{
            "tag": option(text="Script Tag [default]: "),
            "type": option(text="Script Type: ", required=True),
            "name": option(text="Script Name: ", required=True),
            "body": option(text="Script Body: ", required=True, body=True),
            "shebang": option(text="Script Shebang: "),
            "description": option(text="Package Description [limit 85]: ")}
        )
        self.action._create_item(
            content=fields.__dict__,
            module=self.module,
            tag=fields.tag
        )

    def add_file(self):

        def option_body():
            path = self.Base.path_temp.joinpath("temp")
            editor = input(f"Enter text editor [{self.text_editor}]: ") or self.text_editor

            System().system(cmd=[editor, str(path)])

            if path.exists():
                body = File.read(path_file=path)
                path.unlink()
                return body
            return None

        fields = InputAddFile(**{
            "tag": option(text="File Tag [default]: "),
            "name": option(text="File Name: ", required=True),
            "file_path": option(text="File Path: ", required=True),
            "body": option_body(),
            "description": option(text="File Description [limit 85]: ")}
        )
        self.action._create_item(
            content=fields.__dict__,
            module=self.module,
            tag=fields.tag
        )

    def add_text(self):
        fields = InputAddText(**{
            "tag": option(text="Tag [default]: "),
            "name": option(text="Name: ", required=True),
            "text": option(text="Text: ", required=True),
            "label": option(text="Label: ")}
        )
        self.action._create_item(
            content=fields.__dict__,
            module=self.module,
            tag=fields.tag
        )
