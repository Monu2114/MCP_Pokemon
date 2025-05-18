from mcp.client.fastmcp import FastMCP

client = FastMCP("pokemon", transport="tcp", host="127.0.0.1", port=12345)

# Call the resource to get info about pikachu
print("Its running")
result = client.call("pokemon://info/pikachu")
print(result)
