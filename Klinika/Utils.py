class Utils:
    def safe_get(lst, index):
        try:
            return lst[index]
        except IndexError:
            return ""