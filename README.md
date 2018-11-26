# Chain Importer

Importing state data from a different chain looks difficult in the first place. Fortunately, Parity's fat-db functionality allows us to easily iterate over account and contract state. Therefore, we can gather all relevant parts of a parition or the whole source chain and construct a new target chain, with the benefit to be under our control.

Modifications can be performed for various purposes, such as fuzzing of mainnet or testnet contracts. This is our fuzzing preperation step when using [Galactuzz](https://github.com/Ethermat/galactuzz).


Summarized approach for importing a chain state:

    1. Export state data from (synced) source chain
    2. Generate new genesis spec based on template
    3. Run chain based on generated (and possibly modified) genesis spec

## Usage

As prerequisite a synced (mainnet-) chain is required. Furthermore, the chain is expected to be synced with Parity's fat-db functionality:

 ```
parity --fat-db=on --min-peers=50 --max-peers=100 --cache-size=4096
 ```

 When the target block height has been synchronized (if different heights are targeted, running the node in archive mode should be considered), the state can be exported:

  ```
parity export state ./state_export.bin
  ```

Now we are able to generate a genesis spec, which contains the exported state. However, we are able to modify various parts beforehand (e.g. account balances). Make sure to configure *config/chain.spec.template*. Finally, generate the genesis spec as follows:

 ```
python chainspec_generator.py -s ./state_export.bin -t ./config/chain.spec.template -o ./config/chain.spec
 ```

We are now able to start the local testchain:
 ```
parity --chain ./config/chain.spec --reseal-min-period 0 --no-discovery --no-download --jsonrpc-apis all --min-gas-price 0
 ```
