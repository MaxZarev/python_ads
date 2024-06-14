def get_wallets(file_path: str = "data/wallets.txt") -> list[str]:
    """
    The function returns a list of wallets from a text file.
    :param file_path: path to file
    :return: list of wallets
    """
    with open(file_path, "r") as file:
        wallets = file.read().split("\n")
    return wallets
