"""
Generated by `compile_contracts.py` script.
Compiled with Solidity v0.8.19.
"""

# source: web3/_utils/contract_sources/ReflectorContracts.sol:AddressReflectorContract
ADDRESS_REFLECTOR_CONTRACT_BYTECODE = "0x608060405234801561001057600080fd5b50610430806100206000396000f3fe608060405234801561001057600080fd5b50600436106100365760003560e01c80630b816c161461003b578063c04d11fc1461006b575b600080fd5b61005560048036038101906100509190610121565b61009b565b604051610062919061015d565b60405180910390f35b610085600480360381019061008091906102d1565b6100a5565b60405161009291906103d8565b60405180910390f35b6000819050919050565b6060819050919050565b6000604051905090565b600080fd5b600080fd5b600073ffffffffffffffffffffffffffffffffffffffff82169050919050565b60006100ee826100c3565b9050919050565b6100fe816100e3565b811461010957600080fd5b50565b60008135905061011b816100f5565b92915050565b600060208284031215610137576101366100b9565b5b60006101458482850161010c565b91505092915050565b610157816100e3565b82525050565b6000602082019050610172600083018461014e565b92915050565b600080fd5b6000601f19601f8301169050919050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052604160045260246000fd5b6101c68261017d565b810181811067ffffffffffffffff821117156101e5576101e461018e565b5b80604052505050565b60006101f86100af565b905061020482826101bd565b919050565b600067ffffffffffffffff8211156102245761022361018e565b5b602082029050602081019050919050565b600080fd5b600061024d61024884610209565b6101ee565b905080838252602082019050602084028301858111156102705761026f610235565b5b835b818110156102995780610285888261010c565b845260208401935050602081019050610272565b5050509392505050565b600082601f8301126102b8576102b7610178565b5b81356102c884826020860161023a565b91505092915050565b6000602082840312156102e7576102e66100b9565b5b600082013567ffffffffffffffff811115610305576103046100be565b5b610311848285016102a3565b91505092915050565b600081519050919050565b600082825260208201905092915050565b6000819050602082019050919050565b61034f816100e3565b82525050565b60006103618383610346565b60208301905092915050565b6000602082019050919050565b60006103858261031a565b61038f8185610325565b935061039a83610336565b8060005b838110156103cb5781516103b28882610355565b97506103bd8361036d565b92505060018101905061039e565b5085935050505092915050565b600060208201905081810360008301526103f2818461037a565b90509291505056fea26469706673582212202278a07c6a9ad25e3b88c707474203c3184e4afb4ce7c622234580a732cd055864736f6c63430008130033"  # noqa: E501
ADDRESS_REFLECTOR_CONTRACT_RUNTIME = "0x608060405234801561001057600080fd5b50600436106100365760003560e01c80630b816c161461003b578063c04d11fc1461006b575b600080fd5b61005560048036038101906100509190610121565b61009b565b604051610062919061015d565b60405180910390f35b610085600480360381019061008091906102d1565b6100a5565b60405161009291906103d8565b60405180910390f35b6000819050919050565b6060819050919050565b6000604051905090565b600080fd5b600080fd5b600073ffffffffffffffffffffffffffffffffffffffff82169050919050565b60006100ee826100c3565b9050919050565b6100fe816100e3565b811461010957600080fd5b50565b60008135905061011b816100f5565b92915050565b600060208284031215610137576101366100b9565b5b60006101458482850161010c565b91505092915050565b610157816100e3565b82525050565b6000602082019050610172600083018461014e565b92915050565b600080fd5b6000601f19601f8301169050919050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052604160045260246000fd5b6101c68261017d565b810181811067ffffffffffffffff821117156101e5576101e461018e565b5b80604052505050565b60006101f86100af565b905061020482826101bd565b919050565b600067ffffffffffffffff8211156102245761022361018e565b5b602082029050602081019050919050565b600080fd5b600061024d61024884610209565b6101ee565b905080838252602082019050602084028301858111156102705761026f610235565b5b835b818110156102995780610285888261010c565b845260208401935050602081019050610272565b5050509392505050565b600082601f8301126102b8576102b7610178565b5b81356102c884826020860161023a565b91505092915050565b6000602082840312156102e7576102e66100b9565b5b600082013567ffffffffffffffff811115610305576103046100be565b5b610311848285016102a3565b91505092915050565b600081519050919050565b600082825260208201905092915050565b6000819050602082019050919050565b61034f816100e3565b82525050565b60006103618383610346565b60208301905092915050565b6000602082019050919050565b60006103858261031a565b61038f8185610325565b935061039a83610336565b8060005b838110156103cb5781516103b28882610355565b97506103bd8361036d565b92505060018101905061039e565b5085935050505092915050565b600060208201905081810360008301526103f2818461037a565b90509291505056fea26469706673582212202278a07c6a9ad25e3b88c707474203c3184e4afb4ce7c622234580a732cd055864736f6c63430008130033"  # noqa: E501
ADDRESS_REFLECTOR_CONTRACT_ABI = [
    {
        "inputs": [{"internalType": "address", "name": "arg", "type": "address"}],
        "name": "reflect",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "pure",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "address[]", "name": "arg", "type": "address[]"}],
        "name": "reflect",
        "outputs": [{"internalType": "address[]", "name": "", "type": "address[]"}],
        "stateMutability": "pure",
        "type": "function",
    },
]
ADDRESS_REFLECTOR_CONTRACT_DATA = {
    "bytecode": ADDRESS_REFLECTOR_CONTRACT_BYTECODE,
    "bytecode_runtime": ADDRESS_REFLECTOR_CONTRACT_RUNTIME,
    "abi": ADDRESS_REFLECTOR_CONTRACT_ABI,
}
