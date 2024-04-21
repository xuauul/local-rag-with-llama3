import yaml


def load_config():
    with open("config.yaml") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    return config


if __name__ == "__main__":
    config = load_config()
    print(config)