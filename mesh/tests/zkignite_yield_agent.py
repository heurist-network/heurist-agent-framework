import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

from mesh.zkignite_yield_agent import ZkIgniteYieldAgent
import asyncio

async def run_agent():
    agent = ZkIgniteYieldAgent()
    try:
        result = await agent.handle_message({})
        print(result)
    finally:
        await agent.cleanup()

asyncio.run(run_agent())

'''
Example output:
{'response': '**ZKsync Era Top 10 Yield Opportunities Report**\n\n**Ranking Criteria:** APR (Annual Percentage Rate) as per \'aprRecord\' field, descending order\n\n**Selection Criteria:** Yield opportunities with ZKsync token as the reward token (as per \'rewardsRecord\' field)\n\n**Top 10 Yield Opportunities:**\n\n1. **Opportunity:** "Provide Liquidity to ETH-USDC Pool on Zyberswap"  \n\xa0\xa0\xa0**APR:** 43.21% (as per \'aprRecord\')  \n\xa0\xa0\xa0**Yield Earning Action:** Supply ETH and USDC to the specified liquidity pool on Zyberswap DEX.\n\n2. **Opportunity:** "Supply wBTC on LendHub for 90-Day Fixed Term"  \n\xa0\xa0\xa0**APR:** 38.50%  \n\xa0\xa0\xa0**Yield Earning Action:** Lend wBTC for a fixed term of 90 days on LendHub\'s lending market.\n\n3. **Opportunity:** "Stake UNI on Apex Staking Platform - 30-Day Lock"  \n\xa0\xa0\xa0**APR:** 36.89%  \n\xa0\xa0\xa0**Yield Earning Action:** Stake UNI tokens with a 30-day lock period on Apex Staking Platform.\n\n4. **Opportunity:** "Provide Liquidity to ZKSYNC-ETH Pool on OmniDex"  \n\xa0\xa0\xa0**APR:** 35.67%  \n\xa0\xa0\xa0**Yield Earning Action:** Supply ZKSYNC and ETH to the specified liquidity pool on OmniDex DEX.\n\n5. **Opportunity:** "Lend DAI on BentoBox for Variable Rate"  \n\xa0\xa0\xa0**APR:** 34.22%  \n\xa0\xa0\xa0**Yield Earning Action:** Supply DAI to BentoBox\'s lending market at a variable interest rate.\n\n6. **Opportunity:** "Farm CRV on Ellipsis Finance - 2x Reward Multiplier"  \n\xa0\xa0\xa0**APR:** 33.45%  \n\xa0\xa0\xa0**Yield Earning Action:** Engage in liquidity farming for CRV on Ellipsis Finance with a 2x reward multiplier.\n\n7. **Opportunity:** "Supply USDT on Teller Protocol for 60-Day Fixed Term"  \n\xa0\xa0\xa0**APR:** 32.91%  \n\xa0\xa0\xa0**Yield Earning Action:** Lend USDT for a fixed term of 60 days on Teller Protocol\'s lending market.\n\n8. **Opportunity:** "Provide Liquidity to LINK-WETH Pool on BebSwap"  \n\xa0\xa0\xa0**APR:** 32.41%  \n\xa0\xa0\xa0**Yield Earning Action:** Supply LINK and WETH to the specified liquidity pool on BebSwap DEX.\n\n9. **Opportunity:** "Stake AAVE on Aave Lending V2 - Flexible Staking"  \n\xa0\xa0\xa0**APR:** 31.85%  \n\xa0\xa0\xa0**Yield Earning Action:** Stake AAVE tokens with flexible staking terms on Aave Lending V2.\n\n10. **Opportunity:** "Lend ETH on Fulcrum for Variable Rate, Isolated Mode"  \n\xa0\xa0\xa0\xa0**APR:** 31.29%  \n\xa0\xa0\xa0\xa0**Yield Earning Action:** Supply ETH to Fulcrum\'s lending market at a variable interest rate in isolated mode.', 'data': [{'name': 'ZK\non\nVenus', 'protocol': {'name': 'Venus', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/protocols/venus.svg'}, 'tvl': 26651936.43705049, 'apr': 14.45294259396982, 'status': 'LIVE', 'dailyRewards': 6309.328767634042, 'tokens': [{'id': '4346757527029214277', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/tokens/ZK.png'}, {'id': '9248902611183079206', 'icon': ''}]}, {'name': 'SyncSwap\nZK-WETH', 'protocol': {'name': 'SyncSwap', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/protocols/syncswap.svg'}, 'tvl': 8592926.392593691, 'apr': 31.52250308510061, 'status': 'LIVE', 'dailyRewards': 5684.860373083571, 'tokens': [{'id': '11069116170639388822', 'icon': ''}, {'id': '1690446589080997791', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/tokens/WETH.svg'}, {'id': '4346757527029214277', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/tokens/ZK.png'}]}, {'name': 'ZK\non\nAave', 'protocol': {'name': 'Aave', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/protocols/aave.svg'}, 'tvl': 25463035.31562104, 'apr': 13.26457609373875, 'status': 'LIVE', 'dailyRewards': 4542.716711863079, 'tokens': [{'id': '17652896972264996251', 'icon': ''}, {'id': '4346757527029214277', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/tokens/ZK.png'}]}, {'name': 'USDC.e\non\nVenus', 'protocol': {'name': 'Venus', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/protocols/venus.svg'}, 'tvl': 21221326.63609444, 'apr': 12.67171333400013, 'status': 'LIVE', 'dailyRewards': 4206.219177691614, 'tokens': [{'id': '14266888279099432172', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/tokens/USDC.svg'}, {'id': '6819568633837948275', 'icon': ''}]}, {'name': 'USDC.e\non\nZeroLend', 'protocol': {'name': 'ZeroLend', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/protocols/zerolend.png'}, 'tvl': 12602528.91610732, 'apr': 20.06674766379144, 'status': 'LIVE', 'dailyRewards': 3235.553232167143, 'tokens': [{'id': '14266888279099432172', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/tokens/USDC.svg'}, {'id': '3804548436209882038', 'icon': ''}]}, {'name': 'KOI\nUSDC.e-USDT\n0.01%', 'protocol': {'name': 'Koi Finance', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/protocols/koi.svg'}, 'tvl': 6686522.763339854, 'apr': 17.65475489130696, 'status': 'LIVE', 'dailyRewards': 3234.216998956429, 'tokens': [{'id': '14266888279099432172', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/tokens/USDC.svg'}, {'id': '7640849246837422980', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/tokens/USDT.svg'}]}, {'name': 'USDC.e\non\nReactor\nFusion', 'protocol': {'name': 'Reactor Fusion', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/protocols/reactorfusion.svg'}, 'tvl': 6335086.475926572, 'apr': 28.49196606439843, 'status': 'LIVE', 'dailyRewards': 2911.997892501107, 'tokens': [{'id': '11250372896151032422', 'icon': ''}, {'id': '14266888279099432172', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/tokens/USDC.svg'}]}, {'name': 'USDC\non\nAave', 'protocol': {'name': 'Aave', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/protocols/aave.svg'}, 'tvl': 14136891.29555683, 'apr': 16.70640243422407, 'status': 'LIVE', 'dailyRewards': 2588.442571477636, 'tokens': [{'id': '15366660311882098085', 'icon': ''}, {'id': '1610739310155958189', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/tokens/USDC.svg'}]}, {'name': 'PancakeSwapV3\nZK-WETH\n0.25%', 'protocol': {'name': 'PancakeSwap', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/protocols/pancakeswap.svg'}, 'tvl': 2554217.372933698, 'apr': 33.58108601755197, 'status': 'LIVE', 'dailyRewards': 2349.955981041428, 'tokens': [{'id': '1690446589080997791', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/tokens/WETH.svg'}, {'id': '4346757527029214277', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/tokens/ZK.png'}]}, {'name': 'SyncSwap\nUSDC.e-WETH\nClassic', 'protocol': {'name': 'SyncSwap', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/protocols/syncswap.svg'}, 'tvl': 7488365.884022438, 'apr': 21.06887006715933, 'status': 'LIVE', 'dailyRewards': 2315.839540087857, 'tokens': [{'id': '14266888279099432172', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/tokens/USDC.svg'}, {'id': '15884022110407599374', 'icon': ''}, {'id': '1690446589080997791', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/tokens/WETH.svg'}]}, {'name': 'ZK\non\nReactor\nFusion', 'protocol': {'name': 'Reactor Fusion', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/protocols/reactorfusion.svg'}, 'tvl': 7447495.565844058, 'apr': 16.55723693152335, 'status': 'LIVE', 'dailyRewards': 2264.887249357543, 'tokens': [{'id': '4346757527029214277', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/tokens/ZK.png'}, {'id': '8633150067705462402', 'icon': ''}]}, {'name': 'Deposit\nto\nHoldstation\nUSDC.e\nVault', 'protocol': {'name': 'Holdstation', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/protocols/holdstation.svg'}, 'tvl': 2806552.708857139, 'apr': 66.59888223124132, 'status': 'LIVE', 'dailyRewards': 2130.851348599286, 'tokens': [{'id': '13352176591897978566', 'icon': ''}, {'id': '14266888279099432172', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/tokens/USDC.svg'}]}, {'name': 'ZKSwap\nZK-WETH', 'protocol': {'name': 'ZKSwap', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/protocols/zkswap.svg'}, 'tvl': 2771652.628260503, 'apr': 41.91532731171905, 'status': 'LIVE', 'dailyRewards': 1981.296859724286, 'tokens': [{'id': '15116823002753514542', 'icon': ''}, {'id': '1690446589080997791', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/tokens/WETH.svg'}, {'id': '4346757527029214277', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/tokens/ZK.png'}]}, {'name': 'UniswapV3\nZK-WETH\n0.3%', 'protocol': {'name': 'Uniswap', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/protocols/uniswap.svg'}, 'tvl': 2027959.589830235, 'apr': 34.78836817828843, 'status': 'LIVE', 'dailyRewards': 1932.86040717, 'tokens': [{'id': '1690446589080997791', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/tokens/WETH.svg'}, {'id': '4346757527029214277', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/tokens/ZK.png'}]}, {'name': 'USDC.e-ZK\non\nRFX', 'protocol': {'name': 'RFX', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/protocols/rfx.svg'}, 'tvl': 1003971.54995117, 'apr': 90.43031654686119, 'status': 'LIVE', 'dailyRewards': 1619.900442804286, 'tokens': [{'id': '14266888279099432172', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/tokens/USDC.svg'}, {'id': '4346757527029214277', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/tokens/ZK.png'}, {'id': '9985151971114862238', 'icon': ''}]}, {'name': 'USDC.e\non\nVest', 'protocol': {'name': 'Vest Exchange', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/protocols/vest.svg'}, 'tvl': 1712223.549718091, 'apr': 81.59226297479745, 'status': 'LIVE', 'dailyRewards': 1294.221314799286, 'tokens': [{'id': '14266888279099432172', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/tokens/USDC.svg'}]}, {'name': 'ZK\non\nZeroLend', 'protocol': {'name': 'ZeroLend', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/protocols/zerolend.png'}, 'tvl': 7040001.29273262, 'apr': 11.89563000267282, 'status': 'LIVE', 'dailyRewards': 1261.865753965457, 'tokens': [{'id': '4346757527029214277', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/tokens/ZK.png'}, {'id': '853840747588151308', 'icon': ''}]}, {'name': 'ZKSwap\nUSDC-USDC.e-USDT', 'protocol': {'name': 'ZKSwap', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/protocols/zkswap.svg'}, 'tvl': 2782241.775314771, 'apr': 43.35124977599943, 'status': 'LIVE', 'dailyRewards': 1187.498556019286, 'tokens': [{'id': '11816644167945905386', 'icon': ''}, {'id': '14266888279099432172', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/tokens/USDC.svg'}, {'id': '1610739310155958189', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/tokens/USDC.svg'}, {'id': '7640849246837422980', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/tokens/USDT.svg'}]}, {'name': 'M-BTC\non\nZeroLend', 'protocol': {'name': 'ZeroLend', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/protocols/zerolend.png'}, 'tvl': 13285797.74478637, 'apr': 6.361071307069276, 'status': 'LIVE', 'dailyRewards': 1016.161832830674, 'tokens': [{'id': '2606240620424062677', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/tokens/MBTC.svg'}, {'id': '4457761898826812347', 'icon': ''}]}, {'name': 'UniswapV3\nUSDC.e-ZK\n0.3%', 'protocol': {'name': 'Uniswap', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/protocols/uniswap.svg'}, 'tvl': 993548.3568414471, 'apr': 35.09427496452712, 'status': 'LIVE', 'dailyRewards': 955.2838143985715, 'tokens': [{'id': '14266888279099432172', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/tokens/USDC.svg'}, {'id': '4346757527029214277', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/tokens/ZK.png'}]}, {'name': 'PancakeSwapV3\nUSDC.e-ZK\n1%', 'protocol': {'name': 'PancakeSwap', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/protocols/pancakeswap.svg'}, 'tvl': 913371.5187730098, 'apr': 38.17489215383907, 'status': 'LIVE', 'dailyRewards': 955.2838143985715, 'tokens': [{'id': '14266888279099432172', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/tokens/USDC.svg'}, {'id': '4346757527029214277', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/tokens/ZK.png'}]}, {'name': 'USDC.e-WETH\non\nRFX', 'protocol': {'name': 'RFX', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/protocols/rfx.svg'}, 'tvl': 551189.5503716577, 'apr': 125.9117184405405, 'status': 'LIVE', 'dailyRewards': 813.4337490321428, 'tokens': [{'id': '14266888279099432172', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/tokens/USDC.svg'}, {'id': '1690446589080997791', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/tokens/WETH.svg'}, {'id': '8241778347625680838', 'icon': ''}]}, {'name': 'WETH\non\nVenus', 'protocol': {'name': 'Venus', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/protocols/venus.svg'}, 'tvl': 8385453.187928394, 'apr': 7.270606732933819, 'status': 'LIVE', 'dailyRewards': 779.1572846932286, 'tokens': [{'id': '15530301140303696339', 'icon': ''}, {'id': '1690446589080997791', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/tokens/WETH.svg'}]}, {'name': 'Koi\nZK-WETH', 'protocol': {'name': 'Koi Finance', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/protocols/koi.svg'}, 'tvl': 824302.8977234064, 'apr': 53.18500350282895, 'status': 'LIVE', 'dailyRewards': 764.2270295864286, 'tokens': [{'id': '1690446589080997791', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/tokens/WETH.svg'}, {'id': '2993894859146349194', 'icon': ''}, {'id': '4346757527029214277', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/tokens/ZK.png'}]}, {'name': 'iZUMi\nZK-WETH\n1%', 'protocol': {'name': 'Izumi', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/protocols/izumi.svg'}, 'tvl': 737404.731720353, 'apr': 37.82764793877541, 'status': 'LIVE', 'dailyRewards': 764.2270295864286, 'tokens': [{'id': '1690446589080997791', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/tokens/WETH.svg'}, {'id': '4346757527029214277', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/tokens/ZK.png'}]}, {'name': 'USDC.e-WETH\non\nRFX', 'protocol': {'name': 'RFX', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/protocols/rfx.svg'}, 'tvl': 649231.6689099174, 'apr': 100.2610600514341, 'status': 'LIVE', 'dailyRewards': 727.3973278942857, 'tokens': [{'id': '13668635739550670451', 'icon': ''}, {'id': '14266888279099432172', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/tokens/USDC.svg'}, {'id': '1690446589080997791', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/tokens/WETH.svg'}]}, {'name': 'SyncSwap\nUSDC-USDC.e', 'protocol': {'name': 'SyncSwap', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/protocols/syncswap.svg'}, 'tvl': 2062729.663599172, 'apr': 33.58510515600912, 'status': 'LIVE', 'dailyRewards': 722.44279228, 'tokens': [{'id': '14266888279099432172', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/tokens/USDC.svg'}, {'id': '1610739310155958189', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/tokens/USDC.svg'}, {'id': '17642046330598349222', 'icon': ''}]}, {'name': 'WETH\non\nAave', 'protocol': {'name': 'Aave', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/protocols/aave.svg'}, 'tvl': 15700736.1273673, 'apr': 6.796850279032739, 'status': 'LIVE', 'dailyRewards': 662.405488577195, 'tokens': [{'id': '16074389614704641858', 'icon': ''}, {'id': '1690446589080997791', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/tokens/WETH.svg'}]}, {'name': 'ZKSwap\nUSDC.e-WETH', 'protocol': {'name': 'ZKSwap', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/protocols/zkswap.svg'}, 'tvl': 2046790.658661417, 'apr': 17.7248140840879, 'status': 'LIVE', 'dailyRewards': 647.1106025685715, 'tokens': [{'id': '14266888279099432172', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/tokens/USDC.svg'}, {'id': '1690446589080997791', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/tokens/WETH.svg'}, {'id': '18210688409713020579', 'icon': ''}]}, {'name': 'Maverick\nBoosted\nPosition\nMBP-ZK-WETH-39', 'protocol': {'name': 'Maverick', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/protocols/maverick.svg'}, 'tvl': 1403626.127737794, 'apr': 148.6389379796855, 'status': 'LIVE', 'dailyRewards': 636.8558762657143, 'tokens': [{'id': '1690446589080997791', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/tokens/WETH.svg'}, {'id': '17856624126154670083', 'icon': ''}, {'id': '4346757527029214277', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/tokens/ZK.png'}]}, {'name': 'WETH\non\nZeroLend', 'protocol': {'name': 'ZeroLend', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/protocols/zerolend.png'}, 'tvl': 4468623.616673344, 'apr': 8.852057393274496, 'status': 'LIVE', 'dailyRewards': 603.0038307385714, 'tokens': [{'id': '1690446589080997791', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/tokens/WETH.svg'}, {'id': '3209157847953732228', 'icon': ''}]}, {'name': 'Koi\nUSDC.e-WETH', 'protocol': {'name': 'Koi Finance', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/protocols/koi.svg'}, 'tvl': 1519411.880235329, 'apr': 18.48683218681712, 'status': 'LIVE', 'dailyRewards': 539.2588720278571, 'tokens': [{'id': '12267458025043616433', 'icon': ''}, {'id': '14266888279099432172', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/tokens/USDC.svg'}, {'id': '1690446589080997791', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/tokens/WETH.svg'}]}, {'name': 'SyncSwap\nWETH-wrsETH', 'protocol': {'name': 'SyncSwap', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/protocols/syncswap.svg'}, 'tvl': 4275202.812809874, 'apr': 8.868390947393493, 'status': 'LIVE', 'dailyRewards': 479.1641274042858, 'tokens': [{'id': '1690446589080997791', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/tokens/WETH.svg'}, {'id': '56394143214746203', 'icon': ''}, {'id': '6560462356137679872', 'icon': ''}]}, {'name': 'PancakeSwapV3\nUSDC-USDC.e\n0.01%', 'protocol': {'name': 'PancakeSwap', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/protocols/pancakeswap.svg'}, 'tvl': 878208.5887603868, 'apr': 17.76930302747802, 'status': 'LIVE', 'dailyRewards': 427.5384804114286, 'tokens': [{'id': '14266888279099432172', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/tokens/USDC.svg'}, {'id': '1610739310155958189', 'icon': 'https://raw.githubusercontent.com/AngleProtocol/angle-token-list/main/src/assets/tokens/USDC.svg'}]}]}
'''