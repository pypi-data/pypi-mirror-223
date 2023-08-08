from web3 import Web3

class AddressArbitrumJoe:
    #dex
    joe_v2_factory_address=Web3.toChecksumAddress('0x1886D09C9Ade0c5DB822D85D21678Db67B6c2982')
    joe_v2_route_address=Web3.toChecksumAddress('0x7BFd7192E76D950832c77BB412aaE841049D8D9B')
    joe_v2_quote_address=Web3.toChecksumAddress('0x7f281f22eDB332807A039073a7F34A4A215bE89e')

    joe_v1_route_address=Web3.toChecksumAddress('0xbeE5c10Cf6E4F68f831E11C1D9E59B43560B3642')
    joe_v1_factory_address=Web3.toChecksumAddress('0xaE4EC9901c3076D0DdBe76A520F9E90a6227aCB7')

class AddressAbitrumSushi:
    sushi_factory_address=Web3.toChecksumAddress('0xc35DADB65012eC5796536bD9864eD8773aBc74C4')
    sushi_route_address=Web3.toChecksumAddress('0x1b02dA8Cb0d097eB8D57A175b88c7D8b47997506')

class AddressArbitrumTokens:
    #erc20
    usdc=Web3.toChecksumAddress('0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8')
    daie=Web3.toChecksumAddress('0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1')
    weth=Web3.toChecksumAddress('0x82aF49447D8a07e3bd95BD0d56f35241523fBab1')
    wbtc=Web3.toChecksumAddress('0x2f2a2543B76A4166549F7aaB2e75Bef0aefC5B0f')
    joe=Web3.toChecksumAddress('0x371c7ec6D8039ff7933a2AA28EB827Ffe1F52f07')
    gmx=Web3.toChecksumAddress('0xfc5A1A6EB076a2C7aD06eD22C90d7E710E35ad0a')
    arb=Web3.toChecksumAddress('0x912CE59144191C1204E64559FE8253a0e49E6548')
