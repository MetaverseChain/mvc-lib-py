from mvclib.constants import Chain
from mvclib.keys import Key
from mvclib.script.type import P2pkScriptType
from mvclib.service.sensiblequery import SensibleQuery
from mvclib.service.whatsonchain import WhatsOnChain
from mvclib.wallet import Wallet


def test_chain_provider():
    w = Wallet()
    assert w.chain == Chain.MAIN
    assert w.provider is None

    w = Wallet(chain=Chain.TEST)
    assert w.chain == Chain.TEST
    assert w.provider is None

    w = Wallet(provider=WhatsOnChain())
    assert w.chain == Chain.MAIN
    assert isinstance(w.provider, WhatsOnChain)
    assert w.provider.chain == Chain.MAIN

    w = Wallet(chain=Chain.TEST, provider=WhatsOnChain())
    assert w.chain == Chain.MAIN
    assert isinstance(w.provider, WhatsOnChain)
    assert w.provider.chain == Chain.MAIN

    w = Wallet(provider=SensibleQuery(Chain.TEST))
    assert w.chain == Chain.TEST
    assert isinstance(w.provider, SensibleQuery)
    assert w.provider.chain == Chain.TEST


def test():
    p1 = Key('L5agPjZKceSTkhqZF2dmFptT5LFrbr6ZGPvP7u4A6dvhTrr71WZ9')
    p2 = Key('5KiANv9EHEU4o9oLzZ6A7z4xJJ3uvfK2RLEubBtTz1fSwAbpJ2U')

    w1 = Wallet(provider=WhatsOnChain()).add_key(p1).add_key(p2)
    w2 = Wallet(provider=SensibleQuery()).add_keys([p1, p2])
    w3 = Wallet([p1, p2])

    assert w1.get_keys() == w2.get_keys()
    assert w1.get_keys() == w3.get_keys()

    assert w1.get_unspents() == []
    assert w1.get_balance() == 0

    w1.get_unspents(refresh=True)
    assert w1.get_balance() == w1.get_balance(refresh=True)

    w2.get_unspents(refresh=True)
    assert w2.get_balance() == w2.get_balance(refresh=True)

    has_p2pk = False
    for unspent in w2.get_unspents():
        if unspent.script_type == P2pkScriptType():
            has_p2pk = True
            break
    if has_p2pk:
        assert w1.get_balance() < w2.get_balance()
    else:
        assert w1.get_balance() == w2.get_balance()
