import aiohttp

async def PostRequest(url,j):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url,json=j) as response:
                r=await(response.text())
                if response.ok==0:
                    return 1
                return r
        except aiohttp.ClientConnectorError as e:
            return 1