class Config(object):
    def __str__(self):
        return f"{self.__class__.__name__}({self.__dict__})"

    def __getattr__(self, key):
        return self.__dict__[key]

    def __setattr__(self, key, value):
        self.__dict__[key] = value

    def __getitem__(self, key):
        return self.__dict__[key]

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def from_file(self, file, loader):
        with open(file, "r") as f:
            data = loader(f)
        self.__dict__ |= data

    def from_object(self, obj):
        self.__dict__ |= vars(obj)

