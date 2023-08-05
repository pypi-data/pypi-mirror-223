import time
from enum import Enum
from typing import List, Optional, Union

from gql import gql
from graphql import DocumentNode
from graphql_query import Query, Operation, Field, Argument

from tons import settings
from tons.tonsdk.utils import Address
from .._base import NftItemType


class DAppGqlBase(Query):
    filter: Optional['Filter'] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.filter is None:
            self.filter = Filter()
        self.arguments.append(self.filter)


class DAppGqlQuery(DAppGqlBase):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if 'id' not in self.fields:
            self.fields.insert(0, 'id')
        self.arguments.append(OrderById())
        self.arguments.append(Limit())

    def add_pagination(self, prev_last_id: Optional[str]):
        self.filter.add(Comparison.id_gt(prev_last_id), behavior='replace')

    def gql(self) -> DocumentNode:
        query_text = Operation(type='query', queries=[self]).render()
        return gql(query_text)


class Accounts(DAppGqlQuery):
    """
    Sample accounts query:

    query {
      accounts(
        filter: {
          id: {
            in: ["%address1", "%address2"]
          }
        }
        orderBy: {
          path: "id"
          direction: ASC
        }
        limit: 50
      ) {
        id
        address
        acc_type_name
        state_hash
        last_paid
        balance
        last_trans_lt
        code
        data
      }
    }
    """

    def __init__(self, **kwargs):
        super().__init__(name='accounts', fields=Account().fields, **kwargs)

    @classmethod
    def by_ids(cls, ids: List[str], **kwargs) -> 'Accounts':
        query = cls(**kwargs)
        query.filter.add(Comparison.id_in(ids))
        return query

    def add_pagination(self, prev_last_id: Optional[str]):
        raise NotImplementedError('Pagination should not be used for "accounts" query')


class NftItems(DAppGqlQuery):
    """
    Sample nft_items query:

    query {
      nft_items(
        filter: {
          collection_address: {
            eq: "EQDjPtM6QusgMgWfl9kMcG-EALslbTITnKcH8VZK1pnH3UZA"
          }
          dns_domain: {
            ne: null
          }
          owner_address: {
            in: ["%address1", "%address2"]
          }
        }
        orderBy: {
          path: "id"
          direction: ASC
        }
        limit: 50
      ) {
        id
        nft_item_type
        owner_address
        account {
          id
          address
          acc_type_name
          state_hash
          last_paid
          balance
          last_trans_lt
        }
        dns_domain
        dns_last_fill_up_time
        dns_auction {
          auction_end_time
          max_bid_amount
          max_bid_address
        }
      }
    }
    """

    def __init__(self, **kwargs):
        super().__init__(name='nft_items',
                         fields=['nft_item_type',
                                 'owner_address',
                                 Account(include_code=False, include_data=False)],
                         **kwargs)

    @classmethod
    def DNS(cls, dns_collection_address: str, **kwargs) -> 'NftItems':
        query = cls(**kwargs)
        query.fields.append('dns_domain')
        query.fields.append('dns_last_fill_up_time')
        query.fields.append(DNSAuction())
        query.filter.add(Comparison.collection_address(dns_collection_address))
        query.filter.add(Comparison.dns_domain_available(), behavior='ignore')
        return query


class JettonWallets(DAppGqlQuery):
    """
    Sample jetton_wallets query:

    query {
      jetton_wallets(
        filter: {
          owner_address: {
            in: ["%address1", "%address2", "%address3"]
          }
        }
        orderBy: {
          path: "id"
          direction: ASC
        }
        limit: 50
      ) {
        id
        balance
        owner_address
        jetton_master_address
        jetton_wallet_code_hash
        last_trans_lt
        account {
          id
          address
          acc_type_name
          state_hash
          last_paid
          balance
          last_trans_lt
        }
      }
    }
    """

    def __init__(self, **kwargs):
        super().__init__(name='jetton_wallets',
                         fields=['balance',
                                 'owner_address',
                                 'jetton_master_address',
                                 'jetton_wallet_code_hash',
                                 'last_trans_lt',
                                 Account(include_code=False, include_data=False)],
                         **kwargs)


class JettonMinters(DAppGqlQuery):
    """
    Sample jetton_minters query:

    query {
      jetton_minters(
        filter: {
          address: {
            in: ["0:7e33c39e10eeb9463bdd031f14f5774916e135a79ebdf4ed53ca345e0ae9d809"]
          }
        }
        orderBy: {
          path: "id"
          direction: ASC
        }
        limit: 50
      ) {
        id
        jetton_wallet_code_hash
        admin_address
        last_trans_lt
        account {
          id
          address
          acc_type_name
          state_hash
          last_paid
          balance
          last_trans_lt
        }
        content {
          content_type
          content_type_name
          data {
            key
            value
          }
          uri
        }
      }
    }
    """

    def __init__(self, **kwargs):
        super().__init__(name='jetton_minters',
                         fields=['jetton_wallet_code_hash',
                                 'admin_address',
                                 'last_trans_lt',
                                 Account(include_code=False, include_data=False),
                                 Field(name='content', fields=['content_type',
                                                               'content_type_name',
                                                               Field(name='data', fields=['key', 'value']),
                                                               'uri'])],
                         **kwargs)


# ======================================================================================================================
class DAppGqlSubscription(DAppGqlBase):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def gql(self) -> DocumentNode:
        query_text = Operation(type='subscription', queries=[self]).render()
        return gql(query_text)


class TransactionSubscription(DAppGqlSubscription):
    def __init__(self, **kwargs):
        super().__init__(name='transactions', fields=[
            'id',
            'lt',
            'block_id',
            'in_msg',
            'now',
            'credit_first',
            'aborted'])


# ======================================================================================================================


class Account(Field):
    def __init__(self, include_code: bool = True, include_data: bool = True, **kwargs):
        fields = ['id',
                  'address',
                  'acc_type_name',
                  'state_hash',
                  'last_paid',
                  'balance',
                  'last_trans_lt']

        if include_code:
            fields.append('code')
        if include_data:
            fields.append('data')
        super().__init__(name='account', fields=fields, **kwargs)


class DNSAuction(Field):
    def __init__(self, **kwargs):
        fields = ['auction_end_time', 'max_bid_amount', 'max_bid_address']
        super().__init__(name='dns_auction', fields=fields, **kwargs)


# ======================================================================================================================


class Comparison(Argument):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def basic(cls, field: str, comparison_operator: str, value):
        return cls(name=field, value=Argument(name=comparison_operator, value=value))

    @classmethod
    def id_gt(cls, last_id: Optional[str]) -> Optional['Comparison']:
        if last_id is None:
            return
        return cls.basic('id', 'gt', quote_unquote(last_id))

    @classmethod
    def id_in(cls, ids: List[str]) -> 'Comparison':
        return cls.basic('id', 'in', quote_unquote(ids))

    @classmethod
    def address(cls, address: Union[Address, str]) -> 'Comparison':
        return cls.basic('address', 'eq', quote_unquote(Address.raw_id(address)))

    @classmethod
    def address_in(cls, addresses: List[Union[Address, str]]) -> 'Comparison':
        return cls.basic('address', 'in', quote_unquote(raw_ids(addresses)))

    @classmethod
    def owner_address(cls, address: Union[Address, str]) -> 'Comparison':
        return cls.basic('owner_address', 'eq', quote_unquote(Address.raw_id(address)))

    @classmethod
    def owner_address_in(cls, addresses: List[Union[Address, str]]) -> 'Comparison':
        return cls.basic('owner_address', 'in', quote_unquote(raw_ids(addresses)))

    @classmethod
    def nft_item_type_in(cls, nft_item_types: List[NftItemType]) -> 'Comparison':
        return cls.basic('nft_item_type', 'in', [str(int(item_id)) for item_id in nft_item_types])

    @classmethod
    def collection_address(cls, collection_address: str) -> 'Comparison':
        return cls.basic('collection_address', 'eq', quote_unquote(collection_address))

    @classmethod
    def dns_domain(cls, dns_domain: str):
        return cls.basic('dns_domain', 'eq', quote_unquote(dns_domain))

    @classmethod
    def jetton_master_address(cls, jetton_minter_address: Union[Address, str]):
        return cls.basic('jetton_master_address', 'eq', quote_unquote(Address.raw_id(jetton_minter_address)))

    @classmethod
    def dns_domain_available(cls):
        return cls.basic('dns_domain', 'ne', 'null')

    @classmethod
    def dns_max_bidder_in(cls, bidder_address_in: List[Union[Address, str]]) -> 'Comparison':
        return cls(name='dns_auction',
                   value=cls.basic('max_bid_address', 'in', quote_unquote(raw_ids(bidder_address_in))))

    @classmethod
    def dns_auction_finished(cls):
        current_time = int(time.time())
        return cls(name='dns_auction', value=Argument(name='auction_end_time',
                                                      value=[Argument(name='le', value=f'"{current_time}"'),
                                                             Argument(name='ne', value="null")]
                                                      )
                   )


class Filter(Argument):
    def __init__(self, comparison_list: Optional[List[Comparison]] = None, **kwargs):
        if comparison_list is None:
            comparison_list = []
        super().__init__(name='filter', value=comparison_list, **kwargs)

    class AddBehavior(str, Enum):
        extend = 'extend'
        replace = 'replace'
        ignore = 'ignore'
        raise_error = 'raise_error'

    def add(self, comparison: Optional[Comparison], behavior: Union[str, AddBehavior] = 'extend'):
        """
        :param comparison: Comparison to add
        :param behavior:
            extend | replace | ignore | raise_error - What happens if same comparison already exists
        """
        behavior = Filter.AddBehavior(behavior)
        if not comparison:
            return
        try:
            existing_value = next(val for val in self.value if val.name == comparison.name)
        except StopIteration:
            self.value.append(comparison)
        else:
            if behavior == 'extend':
                if isinstance(existing_value.value, list):
                    existing_value.value.append(comparison.value)
                else:
                    existing_value.value = [existing_value.value, comparison.value]
            elif behavior == 'replace':
                existing_value.value = comparison.value
            elif behavior == 'ignore':
                pass
            elif behavior == 'raise_error':
                raise ValueError("Comparison '{}' already exists".format(comparison.name))


class OrderById(Argument):
    def __init__(self, direction: str = 'ASC', **kwargs):
        super().__init__(name='orderBy', value=[Argument(name='path', value='"id"'),
                                                Argument(name='direction', value=direction)], **kwargs)


class Limit(Argument):
    def __init__(self, value=settings.DAPP_RECORDS_LIMIT, **kwargs):
        super().__init__(name='limit', value=value, **kwargs)


def quote_unquote(value: Union[str, List[str]]) -> Union[str, List[str]]:
    if isinstance(value, str):
        return '"' + value + '"'
    return [quote_unquote(_) for _ in value]


def raw_ids(addresses: List[Union[Address, str]]) -> List[str]:
    return [Address.raw_id(address) for address in addresses]
