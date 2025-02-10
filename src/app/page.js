//HomePage

/**'use client';

import { Contract, JsonRpcProvider, Wallet } from "ethers";
import { useEffect, useState } from "react";
import styles from "./page.module.css";
import { formatWeiAmount } from "./utils.js";
import blockchain from "./blockchain.json";
import Logo from "../components/Logo";
import Transfer from "../components/Transfer";

const initialChain = blockchain.chains[0]; //loads wallet 0 (eding with 2266)
const initialNativeAsset = blockchain.assets.find(asset => asset.id === initialChain.nativeAssetId);
const initialTokenAssts = blockchain.assets.filter(asset => (
  asset.chainId === initialNativeAsset.chainId && asset.id !== initialNativeAsset.id
)

);
const initialTransfer = {

  to: '0x70997970C51812dc3A010C7d01b50e0d17dc79C8',
  amount: "1",
  asset: initialNativeAsset
};

export default function Home() {
  const [provider, setProvider] = useState(undefined);
  const [wallet, setWallet] = useState(undefined);
  const[chain,setChain] = useState(initialChain);
  const[balance,setBalance] = useState(undefined);
  const[nativeAsset,setNativeAsset] = useState(initialNativeAsset);
  const[tokenAssets,setTokenAssets] = useState(initialTokenAssts);
  const[transfer,setTransfer] = useState(initialTransfer);
  const[showTransferModal,setShowTransferModal] = useState(false);

  useEffect(() => {
    // Ensure environment variables are loaded correctly
    const mnemonic = process.env.NEXT_PUBLIC_MNEMONIC;
    const rpcUrl = process.env.NEXT_PUBLIC_LOCAL_RPC_URL;

    if (!mnemonic) {
      console.error("Mnemonic is missing.");
      return; // Exit if either environment variable is missing
    }

    if(!rpcUrl) {
      console.error("RPC URL Missing");
      return;
    }

    if (!wallet) {
      try {
        const provider = new JsonRpcProvider(rpcUrl, {
          chainId: 31337,
          name: "localhost", 
          ensAddress: null, // Disable ENS address resolution
        });
        

        const wallet = Wallet.fromPhrase(mnemonic).connect(provider);
        setProvider(provider);
        setWallet(wallet);
      } catch (error) {
        console.error("Error initializing wallet:", error);
      }
    }
  }, [wallet]);

  useEffect(()=>{
    const init = async ()  => {
      const calls  = tokenAssets.map(token => {
        const tokenContract = new Contract(token.address, blockchain.abis.erc20, wallet);
        return tokenContract.balanceOf(wallet.address);
      });
      calls.push(provider.getBalance(wallet.address));
      const results = await Promise.all(calls);
      const nativeBalance = results.pop();
      const newTokenAssets = tokenAssets.map((token, i) => ({...token, balance: results[i]}));
      setNativeAsset(nativeAsset => ({...nativeAsset, ...{balance: nativeBalance}}));
      setTokenAssets(newTokenAssets);
    };
    if(wallet) init();
  },[wallet]);

const handleInputChange = e => {
  let {name,value} = e.target;

  if(name === "asset")
  {
    const ticker = value;
    value = [nativeAsset, ...tokenAssets].find(asset => asset.ticker === ticker);
    value = value || {ticker};
  }
  if(name === "amount")
  {
    value = value.replaceAll(",","");
  }

  setTransfer({
    ...transfer,
    [name]: value
  });

}

const formatTransferAmount = amount => {
  if(Number(amount) < 1 || amount.indexOf(".") !== -1 && !["1","2","3","4","5","6","7","8","9"].includes(amount.slice(-1)))return amount;
  return (
 new Intl.NumberFormat("en-IN", {
    maximumFractionDigits: transfer.asset.decimals,
  }).format(amount))
};

  return (
    <div className="container-fluid mt-5 d-flex justify-content-center">
      <div id="content" className="row">
        <div id="content-inner" className="col">
          <div className="text-center">
            <h1 id="title" className="fw-bold">H.A.D</h1>
            <p id="subtitle" className="mt-4 fw-bold"><span>Had the H.A.D?</span></p>
          </div>
          {wallet ? (
            <>
              <div className={styles.overview}>
                <p>
                  <Logo asset={nativeAsset} />
                  {nativeAsset.name}
                </p>
                <p className={styles.address}>{wallet.address}</p>
                <p className={styles.balance}>{balance && formatWeiAmount(balance, 18)} ETH</p>
              </div>
              
              <div className={styles.tokens}>
                {tokenAssets.map(token => (
                  <div key={token.id} className={styles.token}>
                    <Logo asset={token} />{`${token.name}: ${token.balance && formatWeiAmount(token.balance, token.decimals)} ${token.ticker}`}
                  </div>
                ))}
              </div>


              <div className={styles.transfer}>
                <div className="form group mb-3">
                  <label>Transfer Asset</label>
                  <input 
                    type="text"
                    className="form-control"
                    placeholder="ETH..."
                    name="asset"
                    value={transfer.asset.ticker}
                    onChange={handleInputChange}
                    />
                </div>
                <div className="form group mb-3">
                  <label>Transfer To</label>
                  <input 
                    type="text"
                    className="form-control"
                    placeholder="0xU8Eo..."
                    name="to"
                    value={transfer.to}
                    onChange={handleInputChange}
                    disabled = {!transfer.asset.id}
                    />
                </div>
                <div className="form group mb-3">
                  <label>Transfer Amount</label>
                  <input 
                    type="text"
                    className="form-control"
                    placeholder="1..."
                    name="amount"
                    value={formatTransferAmount(transfer.amount)}
                    onChange={handleInputChange}
                    disabled = {!transfer.asset.id}
                    />
                </div>
                <button
                      className="btn btn-primary mt-4"
                      onClick={() => setShowTransferModal(true)}
                      disabled={!transfer.asset.id || !transfer.to || !transfer.amount}>
                      Send
                </button>
                {showTransferModal && (
                  <Transfer
                  provider = {provider}
                  wallet={wallet}
                  chain={chain}
                  nativeAsset={nativeAsset}
                  transfer={transfer}
                  setShowTransferModal={setShowTransferModal}
                  />
                )};
              </div>
            </>
          ) : (
            "Loading..."
          )}
        </div>
      </div>
    </div>
  );
}**/






'use client';

import { Contract, JsonRpcProvider, Wallet } from "ethers";
import { useEffect, useState } from "react";
import styles from "./page.module.css";
import { formatWeiAmount } from "./utils.js";
import blockchain from "./blockchain.json";
import Logo from "../components/Logo";
import Transfer from "../components/Transfer";

const initChain = blockchain.chains[0]; // Loads wallet 0 (ending with 2266)
const initNativeAsset = blockchain.assets.find(asset => asset.id === initChain.nativeAssetId);
const initTokenAssets = blockchain.assets.filter(asset => (
  asset.chainId === initNativeAsset.chainId && asset.id !== initNativeAsset.id
));
const initTransfer = {
  to: '0x70997970C51812dc3A010C7d01b50e0d17dc79C8',
  amount: "1",
  asset: initNativeAsset
};

export default function Home() {
  const [provider, setProvider] = useState(undefined);
  const [wallet, setWallet] = useState(undefined);
  const [chain, setChain] = useState(initChain);
  const [balance, setBal] = useState(undefined);
  const [nativeAsset, setNA] = useState(initNativeAsset);
  const [tokenAssets, setTA] = useState(initTokenAssets);
  const [trans, setTrans] = useState(initTransfer);
  const [showTransModel, setShowTransModel] = useState(false);

  useEffect(() => {
    const mnemonic = process.env.NEXT_PUBLIC_MNEMONIC;
    const rpcUrl = process.env.NEXT_PUBLIC_RPC_URL;

    if (!mnemonic) {
      console.error("Mnemonic is missing.");
      return;
    }

    if (!rpcUrl) {
      console.error("RPC URL Missing");
      return;
    }

    if (!wallet) {
      try {
        const provider = new JsonRpcProvider(rpcUrl, {
          chainId: 31337,
          name: "localhost",
          ensAddress: null,
        });

        const wallet = Wallet.fromPhrase(mnemonic).connect(provider);
        setProvider(provider);
        setWallet(wallet);
      } catch (error) {
        console.error("Error initializing wallet:", error);
      }
    }
  }, [wallet]);

  useEffect(() => {
    const init = async () => {
      const calls = tokenAssets.map(token => {
        const tokenContract = new Contract(token.address, blockchain.abis.erc20, wallet);
        return tokenContract.balanceOf(wallet.address);
      });

      calls.push(provider.getBalance(wallet.address));

      const results = await Promise.all(calls);
      const nativeBalance = results.pop();

      const newTokenAssets = tokenAssets.map((token, i) => ({
        ...token,
        balance: results[i]
      }));

      setNA(nativeAsset => ({
        ...nativeAsset,
        balance: nativeBalance
      }));

      setTA(newTokenAssets);
      setBal(nativeBalance);
      console.log("Updated balance:", nativeBalance.toString());
    };

    if (wallet) init();
  }, [wallet]);

  const handleIPChange = e => {
    let { name, value } = e.target;

    if (name === "asset") {
      const ticker = value;
      value = [nativeAsset, ...tokenAssets].find(asset => asset.ticker === ticker);
      value = value || { ticker };
    }
    if (name === "amount") {
      value = value.replaceAll(",", "");
    }

    setTrans({
      ...trans,
      [name]: value
    });
  };

  const formatTransAmt = amount => {
    if (Number(amount) < 1 || (amount.indexOf(".") !== -1 && !/[1-9]/.test(amount.slice(-1)))) return amount;
    return new Intl.NumberFormat("en-IN", {
      maximumFractionDigits: trans.asset.decimals,
    }).format(amount);
  };

  /**return (
    <div className="container-fluid mt-5 d-flex justify-content-center">
      <div id="content" className="row">
        <div id="content-inner" className="col">
          <div className="text-center">
            <h1 id="title" className="fw-bold">H.A.D</h1>
            <p id="subtitle" className="mt-4 fw-bold"><span>Had the H.A.D?</span></p>
          </div>
          {wallet ? (
            <>
              <div className={styles.overview}>
                <p>
                  <Logo asset={nativeAsset} />
                  {nativeAsset.name}
                </p>
                <p className={styles.address}>{wallet.address}</p>
                <p className={styles.balance}>{balance && formatWeiAmount(balance, 18)} ETH</p>
              </div>
              <div className={styles.tokens}>
                {tokenAssets.map(token => (
                  <div key={token.id} className={styles.token}>
                    <Logo asset={token} />{`${token.name}: ${token.balance && formatWeiAmount(token.balance, token.decimals)} ${token.ticker}`}
                  </div>
                ))}
              </div>
              <div className={styles.trans}>
                <div className="form group mb-3">
                  <label>Transfer Asset</label>
                  <input 
                    type="text"
                    className="form-control"
                    placeholder="ETH..."
                    name="asset"
                    value={trans.asset.ticker}
                    onChange={handleIPChange}
                  />
                </div>
                <div className="form group mb-3">
                  <label>Transfer To</label>
                  <input 
                    type="text"
                    className="form-control"
                    placeholder="0xU8Eo..."
                    name="to"
                    value={trans.to}
                    onChange={handleIPChange}
                    disabled={!trans.asset.id}
                  />
                </div>
                <div className="form group mb-3">
                  <label>Transfer Amount</label>
                  <input 
                    type="text"
                    className="form-control"
                    placeholder="1..."
                    name="amount"
                    value={formatTransAmt(trans.amount)}
                    onChange={handleIPChange}
                    disabled={!trans.asset.id}
                  />
                </div>
                <button
                  className="btn btn-primary mt-4"
                  onClick={() => setShowTransModel(true)}
                  disabled={!trans.asset.id || !trans.to || !trans.amount}>
                  Send
                </button>
                {showTransModel && (
                  <Transfer
                    provider={provider}
                    wallet={wallet}
                    chain={chain}
                    nativeAsset={nativeAsset}
                    transfer={trans}
                    setShowTransModel={setShowTransModel}
                  />
                )}
              </div>
            </>
          ) : (
            "Loading..."
          )}
        </div>
      </div>
    </div>
  );
}**/

    return (
      <div className="container-fluid mt-5 d-flex justify-content-center">
        <div id="content" className="row">
          <div id="content-inner" className="col">
            <div className="text-center">
              <h1 id="title" className="fw-bold">H.A.D</h1>
              <p id="subtitle" className="mt-4 fw-bold"><span>Had the H.A.D?</span></p>
            </div>
            {wallet ? (
              <>
                <div className={styles.overview}>
                  <p>
                    <Logo asset={nativeAsset} />
                    {nativeAsset.name}
                  </p>
                  <p className={styles.address}>{wallet.address}</p>
                  <p className={styles.balance}>{balance && formatWeiAmount(balance, 18)} ETH</p>
                </div>
                
                <div className={styles.tokens}>
                  {tokenAssets.map(token => (
                    <div key={token.id} className={styles.token}>
                      <Logo asset={token} />{`${token.name}: ${token.balance && formatWeiAmount(token.balance, token.decimals)} ${token.ticker}`}
                    </div>
                  ))}
                </div>


                <div className={styles.transfer}>
                  <div className="form group mb-3">
                    <label>Transfer Asset</label>
                    <input 
                      type="text"
                      className="form-control"
                      placeholder="ETH..."
                      name="asset"
                      value={trans.asset.ticker}
                      onChange={handleIPChange}
                      />
                  </div>
                  <div className="form group mb-3">
                    <label>Transfer To</label>
                    <input 
                      type="text"
                      className="form-control"
                      placeholder="0xU8Eo..."
                      name="to"
                      value={trans.to}
                      onChange={handleIPChange}
                      disabled = {!trans.asset.id}
                      />
                  </div>
                  <div className="form group mb-3">
                    <label>Transfer Amount</label>
                    <input 
                      type="text"
                      className="form-control"
                      placeholder="1..."
                      name="amount"
                      value={formatTransAmt(trans.amount)}
                      onChange={handleIPChange}
                      disabled = {!trans.asset.id}
                      />
                  </div>
                  <button
                    className="btn btn-primary mt-4"
                    style={{ backgroundColor: "rgba(212, 175, 55)", borderColor: "#D4AF37", color: "white" }}
                    onClick={() => setShowTransModel(true)}
                    disabled={!trans.asset.id || !trans.to || !trans.amount}
                  >
                    Send
                  </button>

                  {showTransModel && (
                    <Transfer
                    provider = {provider}
                    wallet={wallet}
                    chain={chain}
                    nativeAsset={nativeAsset}
                    transfer={trans}
                    setShowTransModel={setShowTransModel}
                    />
                  )}
                </div>
              </>
            ) : (
              "Loading..."
            )}
          </div>
        </div>
      </div>
    );
}
