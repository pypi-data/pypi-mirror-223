import pkg_resources
import pandas as pd
import subprocess
import platform
import requests
import zipfile
import json
import re
import os


class Wk:
    def __init__(self, sys: str = None, support: str = None, arch: str = None, extension: str = None):
        self.__df = self.__get_df_from_wkorg()
        self.sys = self.__sys_validator(sys)
        self.support = self.__support_validator(support)
        self.arch = self.__arch_validator(arch)
        self.extension = self.__extension_validator(extension)

    def __get_df_from_wkorg(self) -> pd.DataFrame:
        html = requests.get("https://wkhtmltopdf.org/downloads.html")
        df = pd.read_html(html.content, extract_links="body")[0]
        df = df.drop(columns=[col for col in df.columns if 'Unnamed' in col])

        arch_columns = [col for col in df.columns if col.startswith('Architectures')]
        df['arch'] = df.apply(lambda row: row[arch_columns].tolist(), axis=1)
        df['arch'] = df['arch'].apply(lambda x: list(filter(lambda y: not pd.isna(y), x)))
        df['arch'] = df['arch'].apply(lambda row: [{'arch': arch[0], 'url': arch[1]} for arch in row])
        for column in ["OS/Distribution", "Supported on"]:
            df[column] = df[column].apply(lambda x: x[0])

        df = df.drop(columns=arch_columns)
        return df

    def __get_linux_info(self, info: str) -> str:
        distro_paths = ['/etc/os-release',
                        '/etc/system-release'
                        '/usr/lib/os-release',
                        '/etc/lsb-release',
                        '/etc/debian_version',
                        '/etc/redhat-release']

        for distro_path in distro_paths:
            if os.path.isfile(distro_path):
                with open(distro_path, "r") as file:
                    data = file.read()

                dictionary = {s.split('=')[0]: s.split('=')[1] for s in data.splitlines()}
                return dictionary.get(info)

        raise FileNotFoundError("cannot find release/version info file")

    def __match_platform_version_scrapper(self):
        avaliable_platforms = {"Windows": "Windows",
                               "Darwin": "macOS",
                               "Linux": self.__get_linux_info}

        version_getter = avaliable_platforms.get(platform.system())
        return version_getter("NAME") if callable(version_getter) else version_getter

    def __sys_validator(self, sys: str) -> str:
        if not sys:
            sys = self.__match_platform_version_scrapper()

        valid_systems = set(self.__df['OS/Distribution'].to_list())
        for valid_sys in valid_systems:
            match = re.search(rf"\b{sys}\b", valid_sys, re.IGNORECASE)
            if match:
                return valid_sys

        raise ValueError(f"invalid sys '{sys}', avaiable sys: {', '.join(valid_systems)}")

    def __support_validator(self, support: str) -> str:
        if not support:
            support = platform.release()

        if self.sys in ["Windows", "macOS"]:
            if self.sys == "Windows":

                with open(pkg_resources.resource_filename(__name__, "resources/windows_versions.json"), "r") as file:
                    windows_versions = json.load(file)

                if support in windows_versions:
                    version_number = windows_versions[support]
                elif re.match(r'^[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?$', support):
                    version_number = float(support)
                else:
                    raise ValueError("Invalid Windows version")

                if version_number >= windows_versions["Vista"]:
                    return "Installer (Vista or later)"
                elif version_number >= windows_versions["XP"]:
                    return "7z Archive (XP/2003 or later)"
                else:
                    raise ValueError("Unsupported Windows version")

            if self.sys == "macOS":
                if not float(platform.mac_ver()[0]) >= 10.7:
                    raise ValueError("unsupported macOS version, just 10.7 or later")

        valid_supports = self.__df.loc[self.__df['OS/Distribution'].str.contains(self.sys), 'Supported on'].to_list()
        for valid_support in valid_supports:
            match = re.search(rf"\b{support}\b", valid_support, re.IGNORECASE)
            if match:
                return valid_support

        raise ValueError(f"invalid support '{support}', avaiable supports: {', '.join(valid_supports)}")

    def __arch_validator(self, arch: str) -> str:
        if not arch:
            arch = platform.architecture()[0]
        string_cleaned = re.sub(r"[-_]", "", arch.lower())
        valid_archs = self.__df.loc[self.__df['Supported on'].str.contains(self.support, regex=False), :]
        valid_archs = valid_archs['arch'].iat[0]
        valid_archs = [key["arch"] for key in valid_archs if key["arch"]]

        match_arch = None
        match_similarity = 0

        for valid_arch in valid_archs:
            arq_cleaned = re.sub(r"[-_]", "", valid_arch.lower())
            regex = r"\b" + re.sub(r" ", r"[ _-]?", re.escape(arq_cleaned)) + r"\b"

            if re.search(regex, string_cleaned, re.IGNORECASE):
                similarity = len(set(string_cleaned).intersection(set(arq_cleaned))) / max(len(string_cleaned), len(arq_cleaned))
                if similarity > match_similarity:
                    match_similarity = similarity
                    match_arch = valid_arch

        if match_arch:
            return match_arch

        raise ValueError(f"invalid arch '{arch}', avaliable archs: {', '.join(valid_archs)}")

    def __extension_validator(self, extension: str) -> str:
        valid_extensions = self.__df.loc[self.__df['Supported on'].str.contains(self.support, regex=False), :]
        valid_extensions = [valid_extension for valid_extension in valid_extensions['arch'].iat[0] if valid_extension["arch"] == self.arch]
        valid_extensions = set([re.search(r'[^.]+$', key["url"]).group() for key in valid_extensions])
        for valid_extension in valid_extensions:
            match = re.search(rf"\b{extension}\b", valid_extension, re.IGNORECASE)
            if match:
                return valid_extension

        raise ValueError(f"invalid extension '{extension}', avaliable extensions: {', '.join(valid_extensions)}")

    def __get_url(self) -> str:
        valid_content = self.__df.loc[(self.__df['OS/Distribution'] == self.sys) & (self.__df['Supported on'] == self.support)]
        valid_content = valid_content["arch"].iat[0]
        return [valid_dict["url"] for valid_dict in valid_content if valid_dict["arch"] == self.arch][0]

    def __unzip(self, filepath: str) -> None:
        with zipfile.ZipFile(filepath, 'r') as zip_ref:
            zip_ref.extractall(os.path.dirname(filepath))
            os.unlink(filepath)

    def __un7z(self, filepath: str, winrar_path: str) -> None:
        if not winrar_path or not os.path.exists(winrar_path):
            raise FileNotFoundError("winrar not found in 'winrar_path' arg (winrar path is required to extract 7z files), please install or pass an valid path")
        command = [winrar_path, "e", filepath, "-o+", os.path.dirname(filepath), "-ibck"]
        subprocess.run(command, check=True)

        return os.path.dirname(filepath)

    def __match_descompressor(self, filepath: str, winrar_path: str = None) -> None:
        compressed_extensions = {"zip": self.__unzip,
                                 "7z": self.__un7z}
        extension = re.search(r'[^.]+$', filepath).group()
        descompressor = compressed_extensions.get(extension)
        if extension == "7z":
            descompressor(filepath, winrar_path)
        else:
            descompressor(filepath)

    def get_wk(self, path: str = '', extract: bool = False, winrar_path=None) -> None:

        url = self.__get_url()
        data = requests.get(url)
        filename = re.search(r'[^/]+$', url).group()

        if path and not os.path.exists(path):
            os.makedirs(path)

        with open(os.path.join(path, filename), "wb") as file:
            file.write(data.content)

        if extract is True:
            if not re.search(r'[^.]+$', filename).group() in ["zip", "7z"]:
                raise ValueError(f"file '{filename}' is not supported, supported compressed files: zip and 7z")

            return self.__match_descompressor(os.path.join(path, filename), winrar_path)

        return os.path.join(path, filename)
