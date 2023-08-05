from datetime import datetime
from typing import Generic, TypeVar, List, Optional
import requests
from .util.back_off import ExponentialBackoff
from .util.api_helper import check_and_modify_response, chains, quotes, user_agent

class BlockResponse:
    updated_at: datetime
    """ The timestamp when the response was generated. Useful to show data staleness to users. """
    chain_id: int
    """ The requested chain ID eg: `1`. """
    chain_name: str
    """ The requested chain name eg: `eth-mainnet`. """
    items: List["Block"]
    """ List of response items. """

    def __init__(self, data):
        self.updated_at = datetime.fromisoformat(data["updated_at"])
        self.chain_id = int(data["chain_id"])
        self.chain_name = data["chain_name"]
        self.items = [Block(item_data) for item_data in data["items"]]

class Block:
    signed_at: Optional[datetime]
    """ The block signed timestamp in UTC. """
    height: Optional[int]
    """ The block height. """

    def __init__(self, data):
        self.signed_at = datetime.fromisoformat(data["signed_at"]) if "signed_at" in data and data["signed_at"] is not None else None
        self.height = int(data["height"]) if "height" in data and data["height"] is not None else None
            

class ResolvedAddress:
    updated_at: datetime
    """ The timestamp when the response was generated. Useful to show data staleness to users. """
    chain_id: int
    """ The requested chain ID eg: `1`. """
    chain_name: str
    """ The requested chain name eg: `eth-mainnet`. """
    items: List["ResolvedAddressItem"]
    """ List of response items. """

    def __init__(self, data):
        self.updated_at = datetime.fromisoformat(data["updated_at"])
        self.chain_id = int(data["chain_id"])
        self.chain_name = data["chain_name"]
        self.items = [ResolvedAddressItem(item_data) for item_data in data["items"]]

class ResolvedAddressItem:
    address: Optional[str]
    name: Optional[str]

    def __init__(self, data):
        self.address = data["address"] if "address" in data and data["address"] is not None else None
        self.name = data["name"] if "name" in data and data["name"] is not None else None
            

class BlockHeightsResponse:
    updated_at: datetime
    """ The timestamp when the response was generated. Useful to show data staleness to users. """
    chain_id: int
    """ The requested chain ID eg: `1`. """
    chain_name: str
    """ The requested chain name eg: `eth-mainnet`. """
    items: List["Block"]
    """ List of response items. """
    pagination: Optional["Pagination"]
    """ Pagination metadata. """

    def __init__(self, data):
        self.updated_at = datetime.fromisoformat(data["updated_at"])
        self.chain_id = int(data["chain_id"])
        self.chain_name = data["chain_name"]
        self.items = [Block(item_data) for item_data in data["items"]]
        self.pagination = Pagination(data["pagination"]) if "pagination" in data and data["pagination"] is not None else None

class Pagination:
    has_more: Optional[bool]
    """ True is there is another page. """
    page_number: Optional[int]
    """ The requested page number. """
    page_size: Optional[int]
    """ The requested number of items on the current page. """
    total_count: Optional[int]
    """ The total number of items across all pages for this request. """

    def __init__(self, data):
        self.has_more = data["has_more"] if "has_more" in data and data["has_more"] is not None else None
        self.page_number = int(data["page_number"]) if "page_number" in data and data["page_number"] is not None else None
        self.page_size = int(data["page_size"]) if "page_size" in data and data["page_size"] is not None else None
        self.total_count = int(data["total_count"]) if "total_count" in data and data["total_count"] is not None else None
            

class GetLogsResponse:
    updated_at: datetime
    """ The timestamp when the response was generated. Useful to show data staleness to users. """
    chain_id: int
    """ The requested chain ID eg: `1`. """
    chain_name: str
    """ The requested chain name eg: `eth-mainnet`. """
    items: List["GetLogsEvent"]
    """ List of response items. """

    def __init__(self, data):
        self.updated_at = datetime.fromisoformat(data["updated_at"])
        self.chain_id = int(data["chain_id"])
        self.chain_name = data["chain_name"]
        self.items = [GetLogsEvent(item_data) for item_data in data["items"]]

class GetLogsEvent:
    block_signed_at: Optional[datetime]
    """ The block signed timestamp in UTC. """
    block_height: Optional[int]
    """ The height of the block. """
    block_hash: Optional[str]
    """ The hash of the block. """
    tx_offset: Optional[int]
    """ The offset is the position of the tx in the block. """
    log_offset: Optional[int]
    tx_hash: Optional[str]
    """ The requested transaction hash. """
    raw_log_topics: Optional[List[str]]
    sender_contract_decimals: Optional[int]
    """ Use contract decimals to format the token balance for display purposes - divide the balance by `10^{contract_decimals}`. """
    sender_name: Optional[str]
    sender_contract_ticker_symbol: Optional[str]
    """ The ticker symbol for the sender. This field is set by a developer and non-unique across a network. """
    sender_address: Optional[str]
    sender_address_label: Optional[str]
    sender_logo_url: Optional[str]
    """ The contract logo URL. """
    raw_log_data: Optional[str]
    decoded: Optional["DecodedItem"]

    def __init__(self, data):
        self.block_signed_at = datetime.fromisoformat(data["block_signed_at"]) if "block_signed_at" in data and data["block_signed_at"] is not None else None
        self.block_height = int(data["block_height"]) if "block_height" in data and data["block_height"] is not None else None
        self.block_hash = data["block_hash"] if "block_hash" in data and data["block_hash"] is not None else None
        self.tx_offset = int(data["tx_offset"]) if "tx_offset" in data and data["tx_offset"] is not None else None
        self.log_offset = int(data["log_offset"]) if "log_offset" in data and data["log_offset"] is not None else None
        self.tx_hash = data["tx_hash"] if "tx_hash" in data and data["tx_hash"] is not None else None
        self.raw_log_topics = data["raw_log_topics"] if "raw_log_topics" in data and data["raw_log_topics"] is not None else None
        self.sender_contract_decimals = int(data["sender_contract_decimals"]) if "sender_contract_decimals" in data and data["sender_contract_decimals"] is not None else None
        self.sender_name = data["sender_name"] if "sender_name" in data and data["sender_name"] is not None else None
        self.sender_contract_ticker_symbol = data["sender_contract_ticker_symbol"] if "sender_contract_ticker_symbol" in data and data["sender_contract_ticker_symbol"] is not None else None
        self.sender_address = data["sender_address"] if "sender_address" in data and data["sender_address"] is not None else None
        self.sender_address_label = data["sender_address_label"] if "sender_address_label" in data and data["sender_address_label"] is not None else None
        self.sender_logo_url = data["sender_logo_url"] if "sender_logo_url" in data and data["sender_logo_url"] is not None else None
        self.raw_log_data = data["raw_log_data"] if "raw_log_data" in data and data["raw_log_data"] is not None else None
        self.decoded = DecodedItem(data["decoded"]) if "decoded" in data and data["decoded"] is not None else None

class DecodedItem:
    name: Optional[str]
    signature: Optional[str]
    params: Optional[List["Param"]]

    def __init__(self, data):
        self.name = data["name"] if "name" in data and data["name"] is not None else None
        self.signature = data["signature"] if "signature" in data and data["signature"] is not None else None
        self.params = [Param(item_data) for item_data in data["params"]] if "params" in data and data["params"] is not None else None

class Param:
    name: Optional[str]
    type: Optional[str]
    indexed: Optional[bool]
    decoded: Optional[bool]
    value: Optional[str]

    def __init__(self, data):
        self.name = data["name"] if "name" in data and data["name"] is not None else None
        self.type = data["type"] if "type" in data and data["type"] is not None else None
        self.indexed = data["indexed"] if "indexed" in data and data["indexed"] is not None else None
        self.decoded = data["decoded"] if "decoded" in data and data["decoded"] is not None else None
        self.value = data["value"] if "value" in data and data["value"] is not None else None
            

class LogEventsByAddressResponse:
    updated_at: datetime
    """ The timestamp when the response was generated. Useful to show data staleness to users. """
    chain_id: int
    """ The requested chain ID eg: `1`. """
    chain_name: str
    """ The requested chain name eg: `eth-mainnet`. """
    items: List["LogEvent"]
    """ List of response items. """
    pagination: Optional["Pagination"]
    """ Pagination metadata. """

    def __init__(self, data):
        self.updated_at = datetime.fromisoformat(data["updated_at"])
        self.chain_id = int(data["chain_id"])
        self.chain_name = data["chain_name"]
        self.items = [LogEvent(item_data) for item_data in data["items"]]
        self.pagination = Pagination(data["pagination"]) if "pagination" in data and data["pagination"] is not None else None

class LogEvent:
    block_signed_at: Optional[datetime]
    """ The block signed timestamp in UTC. """
    block_height: Optional[int]
    """ The height of the block. """
    tx_offset: Optional[int]
    """ The offset is the position of the tx in the block. """
    log_offset: Optional[int]
    tx_hash: Optional[str]
    """ The requested transaction hash. """
    raw_log_topics: Optional[List[str]]
    sender_contract_decimals: Optional[int]
    """ Use contract decimals to format the token balance for display purposes - divide the balance by `10^{contract_decimals}`. """
    sender_name: Optional[str]
    sender_contract_ticker_symbol: Optional[str]
    sender_address: Optional[str]
    sender_address_label: Optional[str]
    sender_logo_url: Optional[str]
    """ The contract logo URL. """
    raw_log_data: Optional[str]
    decoded: Optional["DecodedItem"]

    def __init__(self, data):
        self.block_signed_at = datetime.fromisoformat(data["block_signed_at"]) if "block_signed_at" in data and data["block_signed_at"] is not None else None
        self.block_height = int(data["block_height"]) if "block_height" in data and data["block_height"] is not None else None
        self.tx_offset = int(data["tx_offset"]) if "tx_offset" in data and data["tx_offset"] is not None else None
        self.log_offset = int(data["log_offset"]) if "log_offset" in data and data["log_offset"] is not None else None
        self.tx_hash = data["tx_hash"] if "tx_hash" in data and data["tx_hash"] is not None else None
        self.raw_log_topics = data["raw_log_topics"] if "raw_log_topics" in data and data["raw_log_topics"] is not None else None
        self.sender_contract_decimals = int(data["sender_contract_decimals"]) if "sender_contract_decimals" in data and data["sender_contract_decimals"] is not None else None
        self.sender_name = data["sender_name"] if "sender_name" in data and data["sender_name"] is not None else None
        self.sender_contract_ticker_symbol = data["sender_contract_ticker_symbol"] if "sender_contract_ticker_symbol" in data and data["sender_contract_ticker_symbol"] is not None else None
        self.sender_address = data["sender_address"] if "sender_address" in data and data["sender_address"] is not None else None
        self.sender_address_label = data["sender_address_label"] if "sender_address_label" in data and data["sender_address_label"] is not None else None
        self.sender_logo_url = data["sender_logo_url"] if "sender_logo_url" in data and data["sender_logo_url"] is not None else None
        self.raw_log_data = data["raw_log_data"] if "raw_log_data" in data and data["raw_log_data"] is not None else None
        self.decoded = DecodedItem(data["decoded"]) if "decoded" in data and data["decoded"] is not None else None

class LogEventsByTopicHashResponse:
    updated_at: datetime
    """ The timestamp when the response was generated. Useful to show data staleness to users. """
    chain_id: int
    """ The requested chain ID eg: `1`. """
    chain_name: str
    """ The requested chain name eg: `eth-mainnet`. """
    items: List["LogEvent"]
    """ List of response items. """
    pagination: Optional["Pagination"]
    """ Pagination metadata. """

    def __init__(self, data):
        self.updated_at = datetime.fromisoformat(data["updated_at"])
        self.chain_id = int(data["chain_id"])
        self.chain_name = data["chain_name"]
        self.items = [LogEvent(item_data) for item_data in data["items"]]
        self.pagination = Pagination(data["pagination"]) if "pagination" in data and data["pagination"] is not None else None

class AllChainsResponse:
    updated_at: datetime
    """ The timestamp when the response was generated. Useful to show data staleness to users. """
    items: List["ChainItem"]
    """ List of response items. """

    def __init__(self, data):
        self.updated_at = datetime.fromisoformat(data["updated_at"])
        self.items = [ChainItem(item_data) for item_data in data["items"]]

class ChainItem:
    name: Optional[str]
    """ The chain name eg: `eth-mainnet`. """
    chain_id: Optional[str]
    """ The requested chain ID eg: `1`. """
    is_testnet: Optional[bool]
    """ True if the chain is a testnet. """
    db_schema_name: Optional[str]
    """ Schema name to use for direct SQL. """
    label: Optional[str]
    """ The chains label eg: `Ethereum Mainnet`. """
    category_label: Optional[str]
    """ The category label eg: `Ethereum`. """
    logo_url: Optional[str]
    """ A svg logo url for the chain. """
    black_logo_url: Optional[str]
    """ A black png logo url for the chain. """
    white_logo_url: Optional[str]
    """ A white png logo url for the chain. """
    is_appchain: Optional[bool]
    """ True if the chain is an AppChain. """
    appchain_of: Optional["ChainItem"]
    """ The ChainItem the appchain is a part of. """

    def __init__(self, data):
        self.name = data["name"] if "name" in data and data["name"] is not None else None
        self.chain_id = data["chain_id"] if "chain_id" in data and data["chain_id"] is not None else None
        self.is_testnet = data["is_testnet"] if "is_testnet" in data and data["is_testnet"] is not None else None
        self.db_schema_name = data["db_schema_name"] if "db_schema_name" in data and data["db_schema_name"] is not None else None
        self.label = data["label"] if "label" in data and data["label"] is not None else None
        self.category_label = data["category_label"] if "category_label" in data and data["category_label"] is not None else None
        self.logo_url = data["logo_url"] if "logo_url" in data and data["logo_url"] is not None else None
        self.black_logo_url = data["black_logo_url"] if "black_logo_url" in data and data["black_logo_url"] is not None else None
        self.white_logo_url = data["white_logo_url"] if "white_logo_url" in data and data["white_logo_url"] is not None else None
        self.is_appchain = data["is_appchain"] if "is_appchain" in data and data["is_appchain"] is not None else None
        self.appchain_of = ChainItem(data["appchain_of"]) if "appchain_of" in data and data["appchain_of"] is not None else None

class AllChainsStatusResponse:
    updated_at: datetime
    """ The timestamp when the response was generated. Useful to show data staleness to users. """
    items: List["ChainStatusItem"]
    """ List of response items. """

    def __init__(self, data):
        self.updated_at = datetime.fromisoformat(data["updated_at"])
        self.items = [ChainStatusItem(item_data) for item_data in data["items"]]

class ChainStatusItem:
    name: Optional[str]
    """ The chain name eg: `eth-mainnet`. """
    chain_id: Optional[str]
    """ The requested chain ID eg: `1`. """
    is_testnet: Optional[bool]
    """ True if the chain is a testnet. """
    logo_url: Optional[bool]
    """ A svg logo url for the chain. """
    black_logo_url: Optional[str]
    """ A black png logo url for the chain. """
    white_logo_url: Optional[str]
    """ A white png logo url for the chain. """
    is_appchain: Optional[bool]
    """ True if the chain is an AppChain. """
    synced_block_height: Optional[int]
    """ The height of the lastest block available. """
    synced_blocked_signed_at: Optional[datetime]
    """ The signed timestamp of lastest block available. """
    has_data: Optional[bool]
    """ True if the chain has data and ready for querying. """

    def __init__(self, data):
        self.name = data["name"] if "name" in data and data["name"] is not None else None
        self.chain_id = data["chain_id"] if "chain_id" in data and data["chain_id"] is not None else None
        self.is_testnet = data["is_testnet"] if "is_testnet" in data and data["is_testnet"] is not None else None
        self.logo_url = data["logo_url"] if "logo_url" in data and data["logo_url"] is not None else None
        self.black_logo_url = data["black_logo_url"] if "black_logo_url" in data and data["black_logo_url"] is not None else None
        self.white_logo_url = data["white_logo_url"] if "white_logo_url" in data and data["white_logo_url"] is not None else None
        self.is_appchain = data["is_appchain"] if "is_appchain" in data and data["is_appchain"] is not None else None
        self.synced_block_height = int(data["synced_block_height"]) if "synced_block_height" in data and data["synced_block_height"] is not None else None
        self.synced_blocked_signed_at = datetime.fromisoformat(data["synced_blocked_signed_at"]) if "synced_blocked_signed_at" in data and data["synced_blocked_signed_at"] is not None else None
        self.has_data = data["has_data"] if "has_data" in data and data["has_data"] is not None else None
            



T = TypeVar('T')

class Response(Generic[T]):
    data: Optional[T]
    error: bool
    error_code: Optional[int]
    error_message: Optional[str]

    def __init__(self, data: Optional[T], error: bool, error_code: Optional[int], error_message: Optional[str]):
        self.data = data
        self.error = error
        self.error_code = error_code
        self.error_message = error_message


class BaseService:
    __api_key: str
    def __init__(self, api_key: str):
        self.__api_key = api_key


    def get_block(self, chain_name: chains, block_height: str) -> Response[BlockResponse]:
        """
        Parameters:

        chain_name (string): The chain name eg: `eth-mainnet`.
        block_height (str): The block height or `latest` for the latest block available.
        """
        success = False
        data: Optional[Response[BlockResponse]] = None
        response = None
        backoff = ExponentialBackoff()
        while not success:
            try:
                url_params = {}
                

                response = requests.get(f"https://api.covalenthq.com/v1/{chain_name}/block_v2/{block_height}/", params=url_params, headers={
                    "Authorization": f"Bearer {self.__api_key}",
                    "X-Requested-With": user_agent
                })

                res = response.json()
                data = Response(**res)

                if data.error and data.error_code == 429:
                    try:
                        backoff.back_off()
                    except Exception:
                        success = True
                        return Response(
                            data=None,
                            error=data.error,
                            error_code=data.error_code if data else response.status_code,
                            error_message=data.error_message if data else "401 Authorization Required"
                        )
                else:
                    data_class = BlockResponse(data.data)
                    check_and_modify_response(data_class)
                    success = True
                    return Response(
                        data=data_class,
                        error=data.error,
                        error_code=data.error_code if data else response.status_code,
                        error_message=data.error_message if data else "401 Authorization Required"
                    )
            except Exception:
                success = True
                return Response(
                    data=None,
                    error=True,
                    error_code=data.error_code if data is not None else response.status_code if response is not None else None,
                    error_message=data.error_message if data else "401 Authorization Required"
                )
        return Response (
            data=None,
            error=True,
            error_code=data.error_code if data is not None else response.status_code if response is not None else None,
            error_message=data.error_message if data is not None else None
        )
        
    def get_resolved_address(self, chain_name: chains, wallet_address: str) -> Response[ResolvedAddress]:
        """
        Parameters:

        chain_name (string): The chain name eg: `eth-mainnet`.
        wallet_address (str): The requested address. Passing in an `ENS`, `RNS`, `Lens Handle`, or an `Unstoppable Domain` resolves automatically.
        """
        success = False
        data: Optional[Response[ResolvedAddress]] = None
        response = None
        backoff = ExponentialBackoff()
        while not success:
            try:
                url_params = {}
                

                response = requests.get(f"https://api.covalenthq.com/v1/{chain_name}/address/{wallet_address}/resolve_address/", params=url_params, headers={
                    "Authorization": f"Bearer {self.__api_key}",
                    "X-Requested-With": user_agent
                })

                res = response.json()
                data = Response(**res)

                if data.error and data.error_code == 429:
                    try:
                        backoff.back_off()
                    except Exception:
                        success = True
                        return Response(
                            data=None,
                            error=data.error,
                            error_code=data.error_code if data else response.status_code,
                            error_message=data.error_message if data else "401 Authorization Required"
                        )
                else:
                    data_class = ResolvedAddress(data.data)
                    check_and_modify_response(data_class)
                    success = True
                    return Response(
                        data=data_class,
                        error=data.error,
                        error_code=data.error_code if data else response.status_code,
                        error_message=data.error_message if data else "401 Authorization Required"
                    )
            except Exception:
                success = True
                return Response(
                    data=None,
                    error=True,
                    error_code=data.error_code if data is not None else response.status_code if response is not None else None,
                    error_message=data.error_message if data else "401 Authorization Required"
                )
        return Response (
            data=None,
            error=True,
            error_code=data.error_code if data is not None else response.status_code if response is not None else None,
            error_message=data.error_message if data is not None else None
        )
        
    def get_block_heights(self, chain_name: chains, start_date: datetime, end_date: datetime) -> Response[BlockHeightsResponse]:
        """
        Parameters:

        chain_name (string): The chain name eg: `eth-mainnet`.
        start_date (datetime): The start date in YYYY-MM-DD format.
        end_date (datetime): The end date in YYYY-MM-DD format.
        """
        success = False
        data: Optional[Response[BlockHeightsResponse]] = None
        response = None
        backoff = ExponentialBackoff()
        while not success:
            try:
                url_params = {}
                

                response = requests.get(f"https://api.covalenthq.com/v1/{chain_name}/block_v2/{start_date}/{end_date}/", params=url_params, headers={
                    "Authorization": f"Bearer {self.__api_key}",
                    "X-Requested-With": user_agent
                })

                res = response.json()
                data = Response(**res)

                if data.error and data.error_code == 429:
                    try:
                        backoff.back_off()
                    except Exception:
                        success = True
                        return Response(
                            data=None,
                            error=data.error,
                            error_code=data.error_code if data else response.status_code,
                            error_message=data.error_message if data else "401 Authorization Required"
                        )
                else:
                    data_class = BlockHeightsResponse(data.data)
                    check_and_modify_response(data_class)
                    success = True
                    return Response(
                        data=data_class,
                        error=data.error,
                        error_code=data.error_code if data else response.status_code,
                        error_message=data.error_message if data else "401 Authorization Required"
                    )
            except Exception:
                success = True
                return Response(
                    data=None,
                    error=True,
                    error_code=data.error_code if data is not None else response.status_code if response is not None else None,
                    error_message=data.error_message if data else "401 Authorization Required"
                )
        return Response (
            data=None,
            error=True,
            error_code=data.error_code if data is not None else response.status_code if response is not None else None,
            error_message=data.error_message if data is not None else None
        )
        
    def get_logs(self, chain_name: chains, starting_block: Optional[int] = None, ending_block: Optional[str] = None, address: Optional[str] = None, topics: Optional[str] = None, block_hash: Optional[str] = None, skip_decode: Optional[bool] = None) -> Response[GetLogsResponse]:
        """
        Parameters:

        chain_name (string): The chain name eg: `eth-mainnet`.
        starting_block (int): The first block to retrieve log events with. Accepts decimals, hexadecimals, or the strings `earliest` and `latest`.
        ending_block (str): The last block to retrieve log events with. Accepts decimals, hexadecimals, or the strings `earliest` and `latest`.
        address (str): The address of the log events sender contract.
        topics (str): The topic hash(es) to retrieve logs with.
        block_hash (str): The block hash to retrieve logs for.
        skip_decode (bool): Omit decoded log events.
        """
        success = False
        data: Optional[Response[GetLogsResponse]] = None
        response = None
        backoff = ExponentialBackoff()
        while not success:
            try:
                url_params = {}
                
                if starting_block is not None:
                    url_params["starting-block"] = str(starting_block)
                    
                if ending_block is not None:
                    url_params["ending-block"] = str(ending_block)
                    
                if address is not None:
                    url_params["address"] = str(address)
                    
                if topics is not None:
                    url_params["topics"] = str(topics)
                    
                if block_hash is not None:
                    url_params["block-hash"] = str(block_hash)
                    
                if skip_decode is not None:
                    url_params["skip-decode"] = str(skip_decode)
                    

                response = requests.get(f"https://api.covalenthq.com/v1/{chain_name}/events/", params=url_params, headers={
                    "Authorization": f"Bearer {self.__api_key}",
                    "X-Requested-With": user_agent
                })

                res = response.json()
                data = Response(**res)

                if data.error and data.error_code == 429:
                    try:
                        backoff.back_off()
                    except Exception:
                        success = True
                        return Response(
                            data=None,
                            error=data.error,
                            error_code=data.error_code if data else response.status_code,
                            error_message=data.error_message if data else "401 Authorization Required"
                        )
                else:
                    data_class = GetLogsResponse(data.data)
                    check_and_modify_response(data_class)
                    success = True
                    return Response(
                        data=data_class,
                        error=data.error,
                        error_code=data.error_code if data else response.status_code,
                        error_message=data.error_message if data else "401 Authorization Required"
                    )
            except Exception:
                success = True
                return Response(
                    data=None,
                    error=True,
                    error_code=data.error_code if data is not None else response.status_code if response is not None else None,
                    error_message=data.error_message if data else "401 Authorization Required"
                )
        return Response (
            data=None,
            error=True,
            error_code=data.error_code if data is not None else response.status_code if response is not None else None,
            error_message=data.error_message if data is not None else None
        )
        
    def get_log_events_by_address(self, chain_name: chains, contract_address: str, starting_block: Optional[int] = None, ending_block: Optional[str] = None) -> Response[LogEventsByAddressResponse]:
        """
        Parameters:

        chain_name (string): The chain name eg: `eth-mainnet`.
        contract_address (str): The requested contract address. Passing in an `ENS`, `RNS`, `Lens Handle`, or an `Unstoppable Domain` resolves automatically.
        starting_block (int): The first block to retrieve log events with. Accepts decimals, hexadecimals, or the strings `earliest` and `latest`.
        ending_block (str): The last block to retrieve log events with. Accepts decimals, hexadecimals, or the strings `earliest` and `latest`.
        """
        success = False
        data: Optional[Response[LogEventsByAddressResponse]] = None
        response = None
        backoff = ExponentialBackoff()
        while not success:
            try:
                url_params = {}
                
                if starting_block is not None:
                    url_params["starting-block"] = str(starting_block)
                    
                if ending_block is not None:
                    url_params["ending-block"] = str(ending_block)
                    

                response = requests.get(f"https://api.covalenthq.com/v1/{chain_name}/events/address/{contract_address}/", params=url_params, headers={
                    "Authorization": f"Bearer {self.__api_key}",
                    "X-Requested-With": user_agent
                })

                res = response.json()
                data = Response(**res)

                if data.error and data.error_code == 429:
                    try:
                        backoff.back_off()
                    except Exception:
                        success = True
                        return Response(
                            data=None,
                            error=data.error,
                            error_code=data.error_code if data else response.status_code,
                            error_message=data.error_message if data else "401 Authorization Required"
                        )
                else:
                    data_class = LogEventsByAddressResponse(data.data)
                    check_and_modify_response(data_class)
                    success = True
                    return Response(
                        data=data_class,
                        error=data.error,
                        error_code=data.error_code if data else response.status_code,
                        error_message=data.error_message if data else "401 Authorization Required"
                    )
            except Exception:
                success = True
                return Response(
                    data=None,
                    error=True,
                    error_code=data.error_code if data is not None else response.status_code if response is not None else None,
                    error_message=data.error_message if data else "401 Authorization Required"
                )
        return Response (
            data=None,
            error=True,
            error_code=data.error_code if data is not None else response.status_code if response is not None else None,
            error_message=data.error_message if data is not None else None
        )
        
    def get_log_events_by_topic_hash(self, chain_name: chains, topic_hash: str, starting_block: Optional[int] = None, ending_block: Optional[str] = None, secondary_topics: Optional[str] = None) -> Response[LogEventsByTopicHashResponse]:
        """
        Parameters:

        chain_name (string): The chain name eg: `eth-mainnet`.
        topic_hash (str): The endpoint will return event logs that contain this topic hash.
        starting_block (int): The first block to retrieve log events with. Accepts decimals, hexadecimals, or the strings `earliest` and `latest`.
        ending_block (str): The last block to retrieve log events with. Accepts decimals, hexadecimals, or the strings `earliest` and `latest`.
        secondary_topics (str): Additional topic hash(es) to filter on - padded & unpadded address fields are supported.
        """
        success = False
        data: Optional[Response[LogEventsByTopicHashResponse]] = None
        response = None
        backoff = ExponentialBackoff()
        while not success:
            try:
                url_params = {}
                
                if starting_block is not None:
                    url_params["starting-block"] = str(starting_block)
                    
                if ending_block is not None:
                    url_params["ending-block"] = str(ending_block)
                    
                if secondary_topics is not None:
                    url_params["secondary-topics"] = str(secondary_topics)
                    

                response = requests.get(f"https://api.covalenthq.com/v1/{chain_name}/events/topics/{topic_hash}/", params=url_params, headers={
                    "Authorization": f"Bearer {self.__api_key}",
                    "X-Requested-With": user_agent
                })

                res = response.json()
                data = Response(**res)

                if data.error and data.error_code == 429:
                    try:
                        backoff.back_off()
                    except Exception:
                        success = True
                        return Response(
                            data=None,
                            error=data.error,
                            error_code=data.error_code if data else response.status_code,
                            error_message=data.error_message if data else "401 Authorization Required"
                        )
                else:
                    data_class = LogEventsByTopicHashResponse(data.data)
                    check_and_modify_response(data_class)
                    success = True
                    return Response(
                        data=data_class,
                        error=data.error,
                        error_code=data.error_code if data else response.status_code,
                        error_message=data.error_message if data else "401 Authorization Required"
                    )
            except Exception:
                success = True
                return Response(
                    data=None,
                    error=True,
                    error_code=data.error_code if data is not None else response.status_code if response is not None else None,
                    error_message=data.error_message if data else "401 Authorization Required"
                )
        return Response (
            data=None,
            error=True,
            error_code=data.error_code if data is not None else response.status_code if response is not None else None,
            error_message=data.error_message if data is not None else None
        )
        
    def get_all_chains(self ) -> Response[AllChainsResponse]:
        """
        Parameters:

        
        """
        success = False
        data: Optional[Response[AllChainsResponse]] = None
        response = None
        backoff = ExponentialBackoff()
        while not success:
            try:
                url_params = {}
                

                response = requests.get(f"https://api.covalenthq.com/v1/chains/", params=url_params, headers={
                    "Authorization": f"Bearer {self.__api_key}",
                    "X-Requested-With": user_agent
                })

                res = response.json()
                data = Response(**res)

                if data.error and data.error_code == 429:
                    try:
                        backoff.back_off()
                    except Exception:
                        success = True
                        return Response(
                            data=None,
                            error=data.error,
                            error_code=data.error_code if data else response.status_code,
                            error_message=data.error_message if data else "401 Authorization Required"
                        )
                else:
                    data_class = AllChainsResponse(data.data)
                    check_and_modify_response(data_class)
                    success = True
                    return Response(
                        data=data_class,
                        error=data.error,
                        error_code=data.error_code if data else response.status_code,
                        error_message=data.error_message if data else "401 Authorization Required"
                    )
            except Exception:
                success = True
                return Response(
                    data=None,
                    error=True,
                    error_code=data.error_code if data is not None else response.status_code if response is not None else None,
                    error_message=data.error_message if data else "401 Authorization Required"
                )
        return Response (
            data=None,
            error=True,
            error_code=data.error_code if data is not None else response.status_code if response is not None else None,
            error_message=data.error_message if data is not None else None
        )
        
    def get_all_chain_status(self ) -> Response[AllChainsStatusResponse]:
        """
        Parameters:

        
        """
        success = False
        data: Optional[Response[AllChainsStatusResponse]] = None
        response = None
        backoff = ExponentialBackoff()
        while not success:
            try:
                url_params = {}
                

                response = requests.get(f"https://api.covalenthq.com/v1/chains/status/", params=url_params, headers={
                    "Authorization": f"Bearer {self.__api_key}",
                    "X-Requested-With": user_agent
                })

                res = response.json()
                data = Response(**res)

                if data.error and data.error_code == 429:
                    try:
                        backoff.back_off()
                    except Exception:
                        success = True
                        return Response(
                            data=None,
                            error=data.error,
                            error_code=data.error_code if data else response.status_code,
                            error_message=data.error_message if data else "401 Authorization Required"
                        )
                else:
                    data_class = AllChainsStatusResponse(data.data)
                    check_and_modify_response(data_class)
                    success = True
                    return Response(
                        data=data_class,
                        error=data.error,
                        error_code=data.error_code if data else response.status_code,
                        error_message=data.error_message if data else "401 Authorization Required"
                    )
            except Exception:
                success = True
                return Response(
                    data=None,
                    error=True,
                    error_code=data.error_code if data is not None else response.status_code if response is not None else None,
                    error_message=data.error_message if data else "401 Authorization Required"
                )
        return Response (
            data=None,
            error=True,
            error_code=data.error_code if data is not None else response.status_code if response is not None else None,
            error_message=data.error_message if data is not None else None
        )
