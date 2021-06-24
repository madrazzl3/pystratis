from decimal import Decimal
from typing import Union
from api import APIRequest, EndpointRegister, endpoint
from api.coldstaking.requestmodels import *
from api.coldstaking.responsemodels import *
from pybitcoin import UtxoDescriptor, AddressDescriptor, ExtPubKey
from pybitcoin.types import Address, Money, hexstr


class ColdStaking(APIRequest, metaclass=EndpointRegister):
    route = '/api/coldstaking'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @endpoint(f'{route}/cold-staking-info')
    def info(self, wallet_name: str, **kwargs) -> InfoModel:
        """Gets general information related to cold staking.

        Args:
            wallet_name (str): The wallet name.
            **kwargs:

        Returns:
            InfoModel

        Raises:
            APIError
        """
        request_model = InfoRequest(wallet_name=wallet_name)
        data = self.get(request_model, **kwargs)
        return InfoModel(**data)

    @endpoint(f'{route}/cold-staking-account')
    def account(self,
                wallet_name: str,
                wallet_password: str,
                is_cold_wallet_account: bool = False,
                extpubkey: Union[ExtPubKey, str] = None,
                **kwargs) -> AccountModel:
        """Create a cold staking account.

        Args:
            wallet_name (str): The wallet name.
            wallet_password (str): The wallet password.
            is_cold_wallet_account (bool, optional): If this account is for a cold wallet. Default=False.
            extpubkey (ExtPubKey | str, optional): The extpubkey for the cold wallet.
            **kwargs:

        Returns:
            AccountModel

        Raises:
            APIError
        """
        if extpubkey is not None and isinstance(extpubkey, str):
            extpubkey = ExtPubKey(extpubkey)
        request_model = AccountRequest(
            wallet_name=wallet_name,
            wallet_password=wallet_password,
            is_cold_wallet_account=is_cold_wallet_account,
            extpubkey=extpubkey
        )
        data = self.post(request_model, **kwargs)
        return AccountModel(**data)

    @endpoint(f'{route}/cold-staking-address')
    def address(self,
                wallet_name: str,
                is_cold_wallet_address: bool = False,
                segwit: bool = False,
                **kwargs) -> AddressModel:
        """Gets a cold staking address.

        Args:
            wallet_name (str): The wallet name.
            is_cold_wallet_address (bool, optional): If this address is for a cold wallet. Default=False.
            segwit (bool, optional): If this is a segwit address. Default=False.
            **kwargs:

        Returns:
            AddressModel

        Raises:
            APIError
        """
        request_model = AddressRequest(
            wallet_name=wallet_name,
            is_cold_wallet_address=is_cold_wallet_address,
            segwit=segwit
        )
        data = self.get(request_model, **kwargs)
        data['address'] = Address(address=data['address'], network=self._network)
        return AddressModel(**data)

    @endpoint(f'{route}/setup-cold-staking')
    def setup(self,
              cold_wallet_address: Union[Address, str],
              hot_wallet_address: Union[Address, str],
              wallet_name: str,
              wallet_account: str,
              wallet_password: str,
              amount: Union[Money, int, float, Decimal],
              fees: Union[Money, int, float, Decimal],
              subtract_fee_from_amount: bool = True,
              split_count: int = 1,
              segwit_change_address: bool = False,
              **kwargs) -> SetupModel:
        """Spends funds from a normal wallet addresses to the cold staking script.

        Args:
            cold_wallet_address (Address | str): The cold wallet address.
            hot_wallet_address (Address | str): The hot wallet address.
            wallet_name (str): The wallet name.
            wallet_account (str): The wallet account.
            wallet_password (str): The wallet password.
            amount (Money | int | float | Decimal): The amount to send to the old wallet.
            fees (Money | int | float | Decimal): The transaction fee.
            subtract_fee_from_amount (bool, optional): If fee should be subtracted from amount. Default=True.
            split_count (conint(ge=1), optional): Number of transactions to split over. Default=1.
            segwit_change_address (bool, optional): If change address is a segwit address. Default=False.
            **kwargs:

        Returns:
            SetupModel

        Raises:
            APIError
        """
        if isinstance(cold_wallet_address, str):
            cold_wallet_address = Address(address=cold_wallet_address, network=self._network)
        if isinstance(hot_wallet_address, str):
            hot_wallet_address = Address(address=hot_wallet_address, network=self._network)
        request_model = SetupRequest(
            cold_wallet_address=cold_wallet_address,
            hot_wallet_address=hot_wallet_address,
            wallet_name=wallet_name,
            wallet_account=wallet_account,
            wallet_password=wallet_password,
            amount=Money(amount),
            fees=Money(fees),
            subtract_fee_from_amount=subtract_fee_from_amount,
            split_count=split_count,
            segwit_change_address=segwit_change_address
        )
        data = self.post(request_model, **kwargs)
        data['transactionHex'] = hexstr(data['transactionHex'])
        return SetupModel(**data)

    @endpoint(f'{route}/setup-offline-cold-staking')
    def setup_offline(self,
                      cold_wallet_address: Union[Address, str],
                      hot_wallet_address: Union[Address, str],
                      wallet_name: str,
                      wallet_account: str,
                      amount: Union[Money, int, float, Decimal],
                      fees: Union[Money, int, float, Decimal],
                      subtract_fee_from_amount: bool = True,
                      split_count: int = 1,
                      segwit_change_address: bool = False,
                      **kwargs) -> BuildOfflineSignModel:
        """Creates a cold staking setup transaction in an unsigned state.

        Args:
            cold_wallet_address (Address | str): The cold wallet address.
            hot_wallet_address (Address | str): The hot wallet address.
            wallet_name (str): The wallet name.
            wallet_account (str): The wallet account.
            amount (Money | int | float | Decimal): The amount to send to the old wallet.
            fees (Money | int | float | Decimal): The transaction fee.
            subtract_fee_from_amount (bool, optional): If fee should be subtracted from amount. Default=True.
            split_count (conint(ge=1), optional): Number of transactions to split over. Default=1.
            segwit_change_address (bool, optional): If change address is a segwit address. Default=False.
            **kwargs:

        Returns:
            BuildOfflineSignModel

        Raises:
            APIError
        """
        if isinstance(cold_wallet_address, str):
            cold_wallet_address = Address(address=cold_wallet_address, network=self._network)
        if isinstance(hot_wallet_address, str):
            hot_wallet_address = Address(address=hot_wallet_address, network=self._network)
        request_model = SetupOfflineRequest(
            cold_wallet_address=cold_wallet_address,
            hot_wallet_address=hot_wallet_address,
            wallet_name=wallet_name,
            wallet_account=wallet_account,
            amount=Money(amount),
            fees=Money(fees),
            subtract_fee_from_amount=subtract_fee_from_amount,
            split_count=split_count,
            segwit_change_address=segwit_change_address
        )
        data = self.post(request_model, **kwargs)

        # Build the UtxoDescriptors
        data['utxos'] = [UtxoDescriptor(**x) for x in data['utxos']]

        # Build the AddressDescriptors
        address_descriptors = []
        for address_descriptor in data['addresses']:
            address_descriptor['address'] = Address(address=address_descriptor['address'], network=self._network)
            address_descriptors.append(address_descriptor)
        data['addresses'] = [AddressDescriptor(**x) for x in address_descriptors]
        return BuildOfflineSignModel(**data)

    @endpoint(f'{route}/estimate-cold-staking-setup-tx-fee')
    def estimate_setup_tx_fee(self,
                              cold_wallet_address: Union[Address, str],
                              hot_wallet_address: Union[Address, str],
                              wallet_name: str,
                              wallet_account: str,
                              wallet_password: str,
                              amount: Union[Money, int, float, Decimal],
                              fees: Union[Money, int, float, Decimal],
                              subtract_fee_from_amount: bool = True,
                              split_count: int = 1,
                              segwit_change_address: bool = False,
                              **kwargs) -> Money:
        """Estimate the cold staking setup tx fee.

        Args:
            cold_wallet_address (Address | str): The cold wallet address.
            hot_wallet_address (Address | str): The hot wallet address.
            wallet_name (str): The wallet name.
            wallet_account (str): The wallet account.
            wallet_password (str): The wallet password.
            amount (Money | int | float | Decimal): The amount to send to the old wallet.
            fees (Money | int | float | Decimal): The transaction fee.
            subtract_fee_from_amount (bool, optional): If fee should be subtracted from amount. Default=True.
            split_count (conint(ge=1), optional): Number of transactions to split over. Default=1.
            segwit_change_address (bool, optional): If change address is a segwit address. Default=False.
            **kwargs:

        Returns:
            Money

        Raises:
            APIError
        """
        if isinstance(cold_wallet_address, str):
            cold_wallet_address = Address(address=cold_wallet_address, network=self._network)
        if isinstance(hot_wallet_address, str):
            hot_wallet_address = Address(address=hot_wallet_address, network=self._network)
        request_model = SetupRequest(
            cold_wallet_address=cold_wallet_address,
            hot_wallet_address=hot_wallet_address,
            wallet_name=wallet_name,
            wallet_account=wallet_account,
            wallet_password=wallet_password,
            amount=Money(amount),
            fees=Money(fees),
            subtract_fee_from_amount=subtract_fee_from_amount,
            split_count=split_count,
            segwit_change_address=segwit_change_address
        )
        data = self.post(request_model, **kwargs)
        return Money.from_satoshi_units(data)

    @endpoint(f'{route}/estimate-offline-cold-staking-setup-tx-fee')
    def estimate_offline_setup_tx_fee(self,
                                      cold_wallet_address: Union[Address, str],
                                      hot_wallet_address: Union[Address, str],
                                      wallet_name: str,
                                      wallet_account: str,
                                      amount: Union[Money, int, float, Decimal],
                                      fees: Union[Money, int, float, Decimal],
                                      subtract_fee_from_amount: bool = True,
                                      split_count: int = 1,
                                      segwit_change_address: bool = False,
                                      **kwargs) -> Money:
        """Estimate the cold staking offline setup tx fee.

        Args:
            cold_wallet_address (Address | str): The cold wallet address.
            hot_wallet_address (Address | str): The hot wallet address.
            wallet_name (str): The wallet name.
            wallet_account (str): The wallet account.
            amount (Money | int | float | Decimal): The amount to send to the old wallet.
            fees (Money | int | float | Decimal): The transaction fee.
            subtract_fee_from_amount (bool, optional): If fee should be subtracted from amount. Default=True.
            split_count (conint(ge=1), optional): Number of transactions to split over. Default=1.
            segwit_change_address (bool, optional): If change address is a segwit address. Default=False.
            **kwargs:

        Returns:
            Money

        Raises:
            APIError
        """
        if isinstance(cold_wallet_address, str):
            cold_wallet_address = Address(address=cold_wallet_address, network=self._network)
        if isinstance(hot_wallet_address, str):
            hot_wallet_address = Address(address=hot_wallet_address, network=self._network)
        request_model = SetupOfflineRequest(
            cold_wallet_address=cold_wallet_address,
            hot_wallet_address=hot_wallet_address,
            wallet_name=wallet_name,
            wallet_account=wallet_account,
            amount=Money(amount),
            fees=Money(fees),
            subtract_fee_from_amount=subtract_fee_from_amount,
            split_count=split_count,
            segwit_change_address=segwit_change_address
        )
        data = self.post(request_model, **kwargs)
        return Money.from_satoshi_units(data)

    @endpoint(f'{route}/cold-staking-withdrawal')
    def withdrawal(self,
                   receiving_address: Union[Address, str],
                   wallet_name: str,
                   wallet_password: str,
                   amount: Union[Money, int, float, Decimal],
                   fees: Union[Money, int, float, Decimal],
                   subtract_fee_from_amount: bool = True,
                   **kwargs) -> WithdrawalModel:
        """Spends funds from the cold staking wallet account back to a normal wallet account.

        Args:
            receiving_address (Address | str): The receiving address.
            wallet_password (str): The wallet password.
            wallet_name (str): The wallet name.
            amount (Money | int | float | Decimal): The amount to withdraw to the receiving address.
            fees (Money | int | float | Decimal, optional): The amount paid in fees.
            subtract_fee_from_amount (bool, optional): If fee should be subtracted from amount. Default=True.
            **kwargs:

        Returns:
            WithdrawalModel

        Raises:
            APIError
        """
        if isinstance(receiving_address, str):
            receiving_address = Address(address=receiving_address, network=self._network)
        request_model = WithdrawalRequest(
            wallet_name=wallet_name,
            wallet_password=wallet_password,
            receiving_address=receiving_address,
            fees=Money(fees),
            amount=Money(amount),
            subtract_fee_from_amount=subtract_fee_from_amount
        )
        data = self.post(request_model, **kwargs)
        return WithdrawalModel(**data)

    @endpoint(f'{route}/offline-cold-staking-withdrawal')
    def offline_withdrawal(self,
                           receiving_address: Union[Address, str],
                           wallet_name: str,
                           account_name: str,
                           amount: Union[Money, int, float, Decimal],
                           fees: Union[Money, int, float, Decimal],
                           subtract_fee_from_amount: bool = True,
                           **kwargs) -> BuildOfflineSignModel:
        """Builds a request to spend funds from a cold staking wallet account back to a normal wallet account.

        Args:
            receiving_address (Address | str): The receiving address.
            wallet_name (str): The wallet name.
            account_name (str): The account name.
            amount (Money | int | float | Decimal): The amount to withdraw to the receiving address.
            fees (Money | int | float | Decimal): The amount paid in fees.
            subtract_fee_from_amount (bool, optional): If fee should be subtracted from amount. Default=True.
            **kwargs:

        Returns:
            BuildOfflineSignModel

        Raises:
            APIError
        """
        if isinstance(receiving_address, str):
            receiving_address = Address(address=receiving_address, network=self._network)
        request_model = OfflineWithdrawalRequest(
            wallet_name=wallet_name,
            account_name=account_name,
            receiving_address=receiving_address,
            fees=Money(fees),
            amount=Money(amount),
            subtract_fee_from_amount=subtract_fee_from_amount
        )
        data = self.post(request_model, **kwargs)

        # Build the UtxoDescriptors
        for i in range(len(data['utxos'])):
            data['utxos'][i]['amount'] = Money(data['utxos'][i]['amount'])
        data['utxos'] = [UtxoDescriptor(**x) for x in data['utxos']]
        # Build the AddressDescriptors
        address_descriptors = []
        for address_descriptor in data['addresses']:
            address_descriptor['address'] = Address(address=address_descriptor['address'], network=self._network)
            address_descriptors.append(address_descriptor)
        data['addresses'] = [AddressDescriptor(**x) for x in address_descriptors]
        return BuildOfflineSignModel(**data)

    @endpoint(f'{route}/estimate-offline-cold-staking-withdrawal-tx-fee')
    def estimate_offline_withdrawal_tx_fee(self,
                                           wallet_name: str,
                                           account_name: str,
                                           receiving_address: Union[Address, str],
                                           amount: Union[Money, int, float, Decimal],
                                           subtract_fee_from_amount: bool = True,
                                           **kwargs) -> Money:
        """Estimate the fee for an offline cold staking withdrawal transaction.

        Args:
            wallet_name (str): The wallet name.
            account_name (str): The account name.
            receiving_address (Address | str): The receiving address.
            amount (Money | int | float | Decimal): The amount to withdraw to the receiving address.
            subtract_fee_from_amount (bool, optional): If fee should be subtracted from amount. Default=True.
            **kwargs:

        Returns:
            Money

        Raises:
            APIError
        """
        if isinstance(receiving_address, str):
            receiving_address = Address(address=receiving_address, network=self._network)
        request_model = OfflineWithdrawalFeeEstimationRequest(
            wallet_name=wallet_name,
            account_name=account_name,
            receiving_address=receiving_address,
            amount=Money(amount),
            subtract_fee_from_amount=subtract_fee_from_amount
        )
        data = self.post(request_model, **kwargs)
        return Money.from_satoshi_units(data)

    @endpoint(f'{route}/estimate-cold-staking-withdrawal-tx-fee')
    def estimate_withdrawal_tx_fee(self,
                                   receiving_address: Union[Address, str],
                                   wallet_name: str,
                                   wallet_password: str,
                                   amount: Union[Money, int, float, Decimal],
                                   fees: Union[Money, int, float, Decimal],
                                   account_name: str = 'account 0',
                                   subtract_fee_from_amount: bool = True,
                                   **kwargs) -> Money:
        """Estimate the fee for a cold staking withdrawal transaction.

        Args:
            receiving_address (Address | str): The receiving address.
            wallet_password (str): The wallet password.
            wallet_name (str): The wallet name.
            account_name (str, optional): The account name. Default='account 0'.
            amount (Money | int | float | Decimal): The amount to withdraw to the receiving address.
            fees (Money | int | float | Decimal, optional): The amount paid in fees.
            subtract_fee_from_amount (bool, optional): If fee should be subtracted from amount. Default=True.
            **kwargs:

        Returns:
            Money

        Raises:
            APIError
        """
        if isinstance(receiving_address, str):
            receiving_address = Address(address=receiving_address, network=self._network)
        request_model = WithdrawalRequest(
            wallet_name=wallet_name,
            account_name=account_name,
            wallet_password=wallet_password,
            receiving_address=receiving_address,
            fees=Money(fees),
            amount=Money(amount),
            subtract_fee_from_amount=subtract_fee_from_amount
        )
        data = self.post(request_model, **kwargs)
        return Money.from_satoshi_units(data)
