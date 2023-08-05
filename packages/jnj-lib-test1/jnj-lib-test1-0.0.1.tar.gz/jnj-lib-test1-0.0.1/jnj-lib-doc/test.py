import yaml

data = yaml.load(
    open("./files/test.yaml", "r", encoding="UTF-8"), Loader=yaml.FullLoader
)

print(data)
