from typing import Literal

chains = Literal["btc-mainnet", "eth-mainnet", "matic-mainnet", "bsc-mainnet", "avalanche-mainnet", "fantom-mainnet", "moonbeam-mainnet", "moonbeam-moonriver", "rsk-mainnet", "arbitrum-mainnet", "palm-mainnet", "klaytn-mainnet", "heco-mainnet", "nervos-godwoken-mainnet", "axie-mainnet", "evmos-mainnet", "astar-mainnet", "iotex-mainnet", "harmony-mainnet", "cronos-mainnet", "aurora-mainnet", "emerald-paratime-mainnet", "boba-mainnet", "eth-goerli", "matic-mumbai", "avalanche-testnet", "bsc-testnet", "moonbeam-moonbase-alpha", "rsk-testnet", "arbitrum-goerli", "fantom-testnet", "palm-testnet", "heco-testnet", "nervos-godwoken-testnet", "evmos-testnet", "astar-shiden", "iotex-testnet", "harmony-testnet", "aurora-testnet", "scroll-l2-testnet", "scroll-l1-testnet", "covalent-internal-network-v1", "defi-kingdoms-mainnet", "swimmer-mainnet", "boba-avalanche-mainnet", "boba-bobabeam-mainnet", "boba-bnb-mainnet", "boba-rinkeby-testnet", "boba-bobabase-testnet", "boba-bnb-testnet", "boba-avalanche-testnet", "klaytn-testnet", "gather-mainnet", "gather-testnet", "optimism-mainnet", "skale-calypso", "skale-mainnet", "skale-razor", "avalanche-dexalot-mainnet", "skale-omnus", "avalanche-dexalot-testnet", "astar-shibuya", "cronos-testnet", "defi-kingdoms-testnet", "metis-mainnet", "metis-testnet", "milkomeda-a1-mainnet", "milkomeda-a1-devnet", "milkomeda-c1-mainnet", "milkomeda-c1-devnet", "swimmer-testnet", "solana-mainnet", "skale-europa", "meter-mainnet", "meter-testnet", "skale-exorde", "boba-goerli", "neon-testnet", "skale-staging-uum", "skale-staging-lcc", "arbitrum-nova-mainnet", "canto-mainnet", "bittorrent-mainnet", "bittorrent-testnet", "flarenetworks-flare-mainnet", "flarenetworks-flare-testnet", "flarenetworks-canary-mainnet", "flarenetworks-canary-testnet", "kcc-mainnet", "kcc-testnet", "polygon-zkevm-testnet", "linea-testnet", "base-testnet", "mantle-testnet", "scroll-alpha-testnet", "oasys-mainnet", "oasys-testnet", "findora-mainnet", "findora-forge-testnet", "sx-mainnet"]
quotes = Literal["USD", "CAD", "EUR", "SGD", "INR", "JPY", "VND", "CNY", "KRW", "RUB", "TRY", "NGN", "ARS", "AUD", "CHF", "GBP"]
user_agent = "com.covalenthq.sdk.python/0.0.5"

def check_and_modify_response(json_obj):
    """ modify reponse and remove next_update_at """
    for key in list(vars(json_obj).keys()):
        if key == 'next_update_at':
            del vars(json_obj)[key]
        elif isinstance(vars(json_obj)[key], dict):
            check_and_modify_response(vars(json_obj)[key])
