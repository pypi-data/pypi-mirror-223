# http://tkdocs.com/tutorial/morewidgets.html#text
# https://docs.python.org/3/library/tkinter.html

import configparser
import os
import time
import pathlib

from tkinter import END, Tk
from tkinter.messagebox import showwarning, askyesno

from adop import parse_config, api_client
from . import tk_base, widgets
from .startup import app_checks
from .actions import package_install


class App(tk_base.App):
    def do_startup(self):
        self.actions["startup"].extend(
            [
                self.check_thg,
                self.check_py,
                self.check_git,
            ]
        )
        super().do_startup()

    def do_refresh(self):
        self.actions["refresh"].extend(
            [
                self.clear_widgets,
                self.reload_vars,
                self.read_subproj_conf,
                self.read_adop_ini,
                self.read_requires_ini,
            ]
        )
        return super().do_refresh()

    def setup_grid(self):
        self.startup_state: widgets.StartupState = self.grid.add_partial_widget(
            label="Required software:",
            widget=widgets.StartupState,
            kwargs={"pady": self.grid.padding},
        )
        self.proj: widgets.SelectProj = self.grid.add_partial_widget(
            label="Project folder",
            widget=widgets.SelectProj,
            kwargs={"proj_path": self.proj_path, "refresh": self.do_refresh},
        )
        self.subproj: widgets.SelectSubProj = self.grid.add_partial_widget(
            label="Subprojects folder ",
            widget=widgets.SelectSubProj,
            kwargs={"refresh": self.do_refresh},
        )
        self.subproj_tree: widgets.LocalSubprojTree = self.grid.add_partial_widget(
            label="Subprojects from:\n - config/config\n - requires.ini",
            widget=widgets.LocalSubprojTree,
            kwargs={
                "install": self.do_action_install,
                "remove": self.do_action_remove,
            },
        )
        self.remotes: widgets.SelectRemote = self.grid.add_partial_widget(
            label="Remotes",
            widget=widgets.SelectRemote,
            kwargs={"selection": self.on_remotes_selection},
        )
        self.remote_subproj_tree: widgets.RemotePackageTree = (
            self.grid.add_partial_widget(
                label="Remote packages",
                widget=widgets.RemotePackageTree,
                kwargs={"install": self.do_action_download_install},
            )
        )

        super().setup_grid()

    def check_thg(self, result):
        app_checks.check_thg(self, result)

    def check_py(self, result):
        app_checks.check_py(self, result)

    def check_git(self, result):
        app_checks.check_git(self, result)

    def reload_vars(self):
        self.proj_name: str = ""
        self.subproj_dir: str = None
        self.subproj_list: list[str] = []
        self.subproj_requires: dict = {}
        self.adop_ini: configparser.ConfigParser = None

    def clear_widgets(self):
        for item in self.subproj_tree.get_children():
            self.subproj_tree.delete(item)

    def read_subproj_conf(self):
        conf = f"{self.proj_path}/config/config"
        for line in open(conf, "r").readlines():
            if not line.strip().startswith("proj_path"):
                continue

            self.subproj_list.append(line)

            subproj_path = pathlib.Path(
                line.strip()[line.find('"') :].strip('"')
            ).resolve()
            if subproj_path.match(self.proj_path):
                self.proj_name = subproj_path.name
                continue

            name = subproj_path.name
            self.subproj_requires[subproj_path] = {
                "path": subproj_path,
                "name": name,
                "package": "",
                "version": "",
            }
            self.subproj_tree.insert(
                "",
                END,
                name,
                text=name,
                values=["no package!", "", "installed, no package found"],
            )

    def write_subproj_config(self, new_path, remove: bool = False):
        conf = pathlib.Path(self.proj_path, "config", "config")
        with conf.open(mode="r") as f:
            contents = f.readlines()
        do_write = False
        new_line = f'proj_path = "{pathlib.Path(self.subproj_dir, new_path).resolve().as_posix()}"\n'
        proj_path = self.subproj_list[-1]
        if remove:
            if new_line in contents:
                contents.remove(new_line)
                do_write = True
        else:
            if not new_line in contents:
                pos = contents.index(proj_path)
                contents.insert(pos, new_line)
                do_write = True

        if do_write:
            with conf.open(mode="w") as f:
                contents = "".join(contents)
                f.write(contents)

    def read_adop_ini(self):
        self.adop_ini = parse_config.parse(
            os.path.expanduser("~/.adop/adop.ini"), host=None, port=None
        )
        self.install_section = "install:subprojdir"
        self.subproj_dir = self.adop_ini.get(self.install_section, "install_root")
        self.cache_dir = self.adop_ini.get(self.install_section, "cache_root")
        self.subproj.set(self.subproj_dir)

        remotes_list = []
        for section in self.adop_ini.sections():
            if section.startswith("remote:"):
                remotes_list.append(section)
        self.remotes["values"] = remotes_list

        cache_tags = configparser.ConfigParser()
        cache_tags_path = pathlib.Path(self.proj_path, self.cache_dir, "tags.ini")
        cache_tags.read(str(cache_tags_path))

        tags = {}
        for section in cache_tags.values():
            tags.update((sha, tag) for tag, sha in section.items())

        subproj_state = configparser.ConfigParser()
        autodeploystate_path = pathlib.Path(
            self.proj_path, self.subproj_dir, "autodeploystate.ini"
        )
        subproj_state.read(str(autodeploystate_path))

        for section in subproj_state.sections():
            source_hash = subproj_state.get(section, "source_hash")
            destination_dir = pathlib.Path(
                subproj_state.get(section, "destination_dir")
            ).resolve()
            package = subproj_state.get(
                section, "package", fallback=self.guess_package_name(section)
            )
            if destination_dir in self.subproj_requires:
                name = destination_dir.name
                version = (
                    f"tag:{tags[source_hash]}"
                    if source_hash in tags
                    else f"sha256:{source_hash}"
                )
                self.subproj_requires[destination_dir]["version"] = version
                self.subproj_requires[destination_dir]["package"] = package
                self.subproj_requires[package] = self.subproj_requires[destination_dir]
                self.subproj_tree.item(name, values=[package, version, "installed"])

    def guess_package_name(self, subproj_name: str):
        if subproj_name.startswith(self.proj_name):
            return subproj_name.removeprefix(f"{self.proj_name}_")
        return subproj_name

    def read_requires_ini(self):
        requires_ini = configparser.ConfigParser()
        full_requires_ini_path = f"{self.proj_path}/requires.ini"
        requires_ini.read(full_requires_ini_path)
        if not requires_ini.has_section("requires"):
            self.log_append(f"error parsing {full_requires_ini_path}")
            return

        for package, version in requires_ini.items("requires"):
            if not package in self.subproj_requires:
                self.subproj_requires[package] = {"name": package, "version": version}
                self.subproj_tree.insert(
                    "",
                    END,
                    package,
                    text=package,
                    values=[package, version, "not installed!"],
                )
            elif version != self.subproj_requires[package]["version"]:
                path: pathlib.Path = self.subproj_requires[package]["path"]
                self.subproj_tree.item(
                    path.name, values=(package, version, "installed version mismatch!")
                )

    def write_requires_ini(self, package: str, version: str, remove: bool = False):
        full_requires_ini_path = f"{self.proj_path}/requires.ini"
        config = configparser.ConfigParser(
            allow_no_value=True,
            comment_prefixes=["/"],
            delimiters=["="],
        )
        config.optionxform = lambda option: option
        config_path = pathlib.Path(full_requires_ini_path).expanduser()

        if config_path.exists():
            config.read_string(config_path.read_text())

        do_write = False
        if not config.has_section("requires"):
            config.add_section("requires")
            do_write = True

        if not config.has_section("options"):
            config.add_section("options")
            do_write = True

        if not config.get("options", "install", fallback="") == "subprojdir":
            config.set("options", "install", "subprojdir")
            do_write = True

        if remove:
            if config.has_option("requires", package):
                config.remove_option("requires", package)
                do_write = True
        else:
            if not config.has_option("requires", package):
                config.set("requires", package, version)
                do_write = True

            if not config.get("requires", package) == version:
                config.set("requires", package, version)
                do_write = True

        if do_write:
            config_path.parent.mkdir(parents=True, exist_ok=True)
            with config_path.open("w") as f:
                config.write(f)

    def clear_remote_subproj(self):
        for item in self.remote_subproj_tree.get_children():
            self.remote_subproj_tree.delete(item)

    def load_remote_subproj(self, subproj: str, data: dict):
        self.remote_subproj_tree.insert("", END, subproj, text=subproj)

        def sort_serial(i: tuple[str, dict]):
            return i[1]["serial"]

        for shasum, package in sorted(data.items(), key=sort_serial):
            serial = package["serial"]
            version = (
                f"tag:{package['tag']}"
                if package["tag"]
                else f"sha256:{package['sha256']}"
            )
            date_serial = f"{time.strftime('%Y-%m-%d %X %z', time.localtime(serial))}  /  {serial}"
            self.remote_subproj_tree.insert(
                subproj, 0, shasum, text=version, values=[date_serial]
            )

    def on_remotes_selection(self, event):
        def gen(self: App):
            self.clear_remote_subproj()
            remote_section = self.remotes.get()

            headers = {}
            data = {}
            try:
                remote_data = {
                    "url": self.adop_ini.get(remote_section, "url"),
                    "token": self.adop_ini.get(remote_section, "token"),
                    "insecure": self.adop_ini.getboolean(
                        remote_section, "insecure", fallback=False
                    ),
                    "direct": self.adop_ini.getboolean(
                        remote_section, "direct", fallback=False
                    ),
                }
                for res in api_client.api_client(
                    endpoint="list/zip", remote_data=remote_data, headers=headers
                ):
                    if isinstance(res, str):
                        self.log_append(res)
                        yield
                    else:
                        data = res
            except Exception as err:
                self.log_append(f"{err}")
            if not data:
                self.log_append("No data")
                return
            for k, v in data.items():
                self.load_remote_subproj(k, v)

        self.run_generator(gen(self))

    def do_action_download_install(self):
        def gen():
            yield
            if self.remotes.get().startswith("("):
                showwarning("No remote selected", "Select a remote and try again")
                return
            for iid in self.remote_subproj_tree.selection():
                yield
                package = self.remote_subproj_tree.parent(iid)
                version = self.remote_subproj_tree.item(iid, "text")
                if not askyesno(
                    "Confirm",
                    f"Confirm installation of '{package}' version '{version}'",
                ):
                    return
                self.write_requires_ini(package, version)
                yield
                subproj_path = yield from package_install.package_install(
                    package,
                    version,
                    self.adop_ini,
                    self.install_section,
                    self.remotes.get(),
                    self.log.append,
                )
                if subproj_path:
                    self.write_subproj_config(subproj_path)

                self.do_refresh()

        self.run_generator(gen())

    def do_action_install(self):
        def gen():
            yield
            if self.remotes.get().startswith("("):
                showwarning("No remote selected", "Select a remote and try again")
                return
            for iid in self.subproj_tree.selection():
                yield
                package, version, state = self.subproj_tree.item(iid, "values")
                if "no package" in state:
                    showwarning("Package not found", "Package or version not detected")
                    return
                if not askyesno(
                    "Confirm",
                    f"Confirm installation of '{package}' version '{version}'",
                ):
                    return
                self.write_requires_ini(package, version)
                yield
                subproj_path = yield from package_install.package_install(
                    package,
                    version,
                    self.adop_ini,
                    self.install_section,
                    self.remotes.get(),
                    self.log.append,
                )
                if subproj_path:
                    self.write_subproj_config(subproj_path)

                self.do_refresh()

        self.run_generator(gen())

    def do_action_remove(self):
        def gen():
            yield
            for iid in self.subproj_tree.selection():
                yield
                package = self.subproj_tree.parent(iid)
                subproj_path = self.subproj_tree.item(iid, "text")
                package, version, state = self.subproj_tree.item(iid, "values")
                if not askyesno(
                    "Confirm",
                    f"Remove '{subproj_path}' from 'config/config' and '{package}' from 'reqiures.ini'?",
                ):
                    return
                yield
                self.write_requires_ini(package, version, remove=True)
                yield
                self.write_subproj_config(subproj_path, remove=True)
                yield
                self.do_refresh()

        self.run_generator(gen())


def main(proj_path: str):
    root = Tk()
    root.protocol("WM_DELETE_WINDOW", App(root, proj_path).destroy)
    root.mainloop()


if __name__ == "__main__":
    main("")
