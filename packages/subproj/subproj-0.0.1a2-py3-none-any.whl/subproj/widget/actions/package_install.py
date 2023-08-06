import configparser

from adop import zip_install_sequences


def ini_parser(
    adop_ini: configparser.ConfigParser, install_section: str, remote_section: str
):
    keep_on_disk = 0
    if adop_ini.getboolean("auto_delete", "on"):
        keep_on_disk = adop_ini.getint("auto_delete", "keep_on_disk")
    install_data = {
        "install_section": install_section,
        "install_root": adop_ini.get(install_section, "install_root"),
        "cache_root": adop_ini.get(install_section, "cache_root"),
    }

    remote_data = [
        {
            "url": adop_ini.get(remote_section, "url"),
            "token": adop_ini.get(remote_section, "token"),
            "insecure": adop_ini.getboolean(remote_section, "insecure", fallback=False),
            "direct": adop_ini.getboolean(remote_section, "direct", fallback=False),
        }
    ]
    return keep_on_disk, install_data, remote_data


def package_install(
    package: str,
    version: str,
    adop_ini: configparser.ConfigParser,
    install_section: str,
    remote_section: str,
    logger: callable,
):
    keep_on_disk, install_data, remote_data = ini_parser(
        adop_ini, install_section, remote_section
    )
    requires_data = {package: version}
    extra_data = {}
    yield
    _handle_zip = zip_install_sequences.client_install_zip_sequence(
        install_data, keep_on_disk, remote_data, requires_data, extra_data
    )
    install_path = ""
    try:
        for res in _handle_zip:
            yield
            if isinstance(res, dict):
                if "root" in res:
                    logger(f"Requires: {res['root']}")
                elif "result_code" in res:
                    logger(f"Result: {res['result']}")
                    if res["result_code"] == 0:
                        install_path = res["result_data"]["root"]
            else:
                logger(f"          {res}")
    except Exception as err:
        logger(f"ERROR: {err}")
    return install_path
