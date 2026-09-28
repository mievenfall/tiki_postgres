from configparser import ConfigParser

def load_config(filename="database.ini", section="postgresql"):
    parser = ConfigParser()
    parser.read(filename)

    if not parser.has_section(section):
        raise Exception(f"Section {section} not found in {filename}")

    return dict(parser.items(section))


if __name__ == "__main__":
    print(load_config())
