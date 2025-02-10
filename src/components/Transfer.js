"use client";
import { useEffect, useState } from "react";
import styles from "./transfer.module.css";
import { parseUnits, Contract } from "ethers";
import { formatWeiAmount } from "../app/utils";
import Link from "next/link";
import blockchain from "../app/blockchain.json";

export default function Transfer({
  provider,
  wallet,
  chain,
  nativeAsset,
  transfer,
  setShowTransModel,
}) {
  const [txCostEth, setTxCostEth] = useState(null);
  const [txCostINR, setTxCostINR] = useState(null);
  const [sending, setSending] = useState(false);
  const [txHash, setTxHash] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const init = async () => {
      try {
        let estimateGas;
        if (!transfer.asset.address) {
          const txRequest = {
            from: wallet.address,
            to: transfer.to,
            value: parseUnits(transfer.amount, transfer.asset.decimals),
          };
          estimateGas = await wallet.estimateGas(txRequest);
        } else {
          const token = new Contract(
            transfer.asset.address,
            blockchain.abis.erc20,
            wallet
          );
          estimateGas = await token.transfer.estimateGas(
            transfer.to,
            parseUnits(transfer.amount, transfer.asset.decimals)
          );
        }

        const [gasCost, feeData, ethPriceRaw] = await Promise.all([
          estimateGas,
          provider.getFeeData(),
          fetch(
            `https://api.coingecko.com/api/v3/simple/price?ids=${nativeAsset.coingeckoId}&vs_currencies=usd`
          ),
        ]);

        const txCostEth = BigInt(gasCost) * BigInt(feeData.maxFeePerGas);
        const ethPrice = await ethPriceRaw.json();
        const adjustedEthPrice = Math.round(
          ethPrice[nativeAsset.coingeckoId].usd * 100
        );
        const txCostINR =
        (txCostEth * BigInt(adjustedEthPrice) * BigInt(864)) / BigInt(100 * 10);

        setTxCostEth(txCostEth);
        setTxCostINR(txCostINR);
      } catch (error) {
        console.error("Error fetching transaction costs:", error);
        setError("Failed to fetch transaction costs.");
      }
    };
    init();
  }, [provider, wallet, transfer, nativeAsset]);

  const getTransactionFeeString = () => {
    if (txCostINR !== null && txCostEth !== null) {
      return `${formatWeiAmount(
        txCostINR,
        nativeAsset.decimals
      )} INR (${formatWeiAmount(txCostEth, nativeAsset.decimals)}) ${
        nativeAsset.ticker
      }`;
    }
    return "Loading...";
  };

  const getTransactionUrl = (hash) =>
    `${chain.blockchainExplorer}/tx/${hash}`;

  const updateWalletBalance = async () => {
    try {
      const balance = await provider.getBalance(wallet.address);
      // Assuming there's a way to update the wallet balance in the parent component
    } catch (error) {
      console.error("Failed to update wallet balance:", error);
    }
  };

  const send = async () => {
    setSending(true);
    setError(null);
    try { 
      let tx;//
      if(!transfer.asset.address){//
        const txRequest = {
          from: wallet.address,
          to: transfer.to,
          value: parseUnits(transfer.amount, transfer.asset.decimals),
        };
        tx = wallet.sendTransaction(txRequest);
      }
      else{
        const token = new Contract(
          transfer.asset.address,
          blockchain.abis.erc20,
          wallet
        );
        tx = await token.transfer(
          transfer.to,
          parseUnits(transfer.amount, transfer.asset.decimals)
        );
      }

      const txResponse = await tx;
      console.log("Transaction response:", txResponse);

      const txReceipt = await txResponse.wait();
      console.log("Transaction receipt:", txReceipt);

      if (txReceipt.status !== 1) {
        throw new Error("Transaction failed on-chain");
      }

      setTxHash(txReceipt.transactionHash);
      console.log("Transaction successful, hash:", txReceipt.transactionHash);

      await updateWalletBalance();
    } catch (error) {
      console.error("Transaction Error:", error);
      setError(error.message || "Transaction failed unexpectedly");
    } finally {
      setSending(false);
    }
  };

  /**return (
    <div id={styles.overlay}>
      <div id={styles.transfer}>
        <h2 className="fw-bold text-center">Transfer Details</h2>
        <div className="form-group mb-3">
          <label>Network</label>
          <input
            type="text"
            className="form-control mb-3"
            name="network"
            value={chain.name}
            disabled={true}
          />
        </div>
        <div className="form-group mb-3">
          <label>From</label>
          <input
            type="text"
            className="form-control mb-3"
            name="from"
            value={wallet.address}
            disabled={true}
          />
        </div>
        <div className="form-group mb-3">
          <label>To</label>
          <input
            type="text"
            className="form-control mb-3"
            name="to"
            value={transfer.to}
            disabled={true}
          />
        </div>
        <div className="form-group mb-3">
          <label>Amount</label>
          <input
            type="text"
            className="form-control mb-3"
            name="amount"
            value={transfer.amount}
            disabled={true}
          />
        </div>
        <div className="form-group mb-3">
          <label>ASSET</label>
          <input
            type="text"
            className="form-control mb-3"
            name="asset"
            value={transfer.asset.ticker}
            disabled={true}
          />
        </div>
        <div className="form-group mb-3">
          <label>Transaction Fee </label>
          <input
            type="text"
            className="form-control mb-3"
            name="txFee"
            value={getTransactionFeeString()}
            disabled={true}
          />
        </div>
        {sending && (
          <div className="alert alert-info mt-3 mb-3">
            <i className="bi bi-info-circle-fill"></i> Sending...
          </div>
        )}
        {txHash && !sending && !error && (
          <div className="alert alert-info mt-3 mb-3">
            <i className="bi bi-check-circle-fill"></i> Transaction Successful! -{" "}
            <Link href={getTransactionUrl(txHash)}>
              <a target="_blank" rel="noopener noreferrer">
                Transaction Hash
              </a>
            </Link>
          </div>
        )}
        {!sending && error && (
          <div className="alert alert-danger mt-3 mb-3">
            <i className="bi bi-exclamation-triangle-fill"></i> {error}
          </div>
        )}
        <div className="text-right">
          <button 
              className="btn btn-primary me-3" 
              onClick={send} 
              disabled={sending}
            >
              {sending ? "Sending..." : "Send"}
          </button>

          <button
            className="btn btn-secondary"
            onClick={() => setShowTransModel(false)}
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}**/

      return (
        <div id={styles.overlay}>
          <div id={styles.transfer}>
            <h2 className="fw-bold text-center">Transfer Details</h2>
            <div className="form-group mb-3">
              <label>Network</label>
              <input
                type="text"
                className="form-control mb-3"
                name="network"
                value={chain.name}
                disabled={true}
              />
            </div>
            <div className="form-group mb-3">
              <label>From</label>
              <input
                type="text"
                className="form-control mb-3"
                name="from"
                value={wallet.address}
                disabled={true}
              />
            </div>
            <div className="form-group mb-3">
              <label>To</label>
              <input
                type="text"
                className="form-control mb-3"
                name="to"
                value={transfer.to}
                disabled={true}
              />
            </div>
            <div className="form-group mb-3">
              <label>Amount</label>
              <input
                type="text"
                className="form-control mb-3"
                name="amount"
                value={transfer.amount}
                disabled={true}
              />
            </div>
            <div className="form-group mb-3">
              <label>ASSET</label>
              <input
                type="text"
                className="form-control mb-3"
                name="asset"
                value={transfer.asset.ticker}
                disabled={true}
              />
            </div>
            <div className="form-group mb-3">
              <label>Transaction Fee </label>
              <input
                type="text"
                className="form-control mb-3"
                name="txFee"
                value={getTransactionFeeString()}
                disabled={true}
              />
            </div>
            {sending && (
              <div className="alert alert-info mt-3 mb-3">
                <i className="bi bi-info-circle-fill"></i> Sending...
              </div>
            )}
            {txHash && !sending && !error && (
              <div className="alert alert-info mt-3 mb-3">
                <i className="bi bi-check-circle-fill"></i> Transaction Successful! -{" "}
                <Link href={getTransactionUrl(txHash)}>
                  <a target="_blank" rel="noopener noreferrer">
                    Transaction Hash
                  </a>
                </Link>
              </div>
            )}
            {!sending && error && (
              <div className="alert alert-danger mt-3 mb-3">
                <i className="bi bi-exclamation-triangle-fill"></i> {error}
              </div>
            )}
            <div className="text-right">
              <button 
                  className="btn btn-primary me-3" 
                  style={{ backgroundColor: "rgba(212, 175, 55)", borderColor: "#D4AF37", color: "white" }}
                  onClick={send} 
                  disabled={sending}
                >
                  {sending ? "Sending..." : "Send"}
              </button>

              <button
                className="btn btn-secondary"
                
                onClick={() => setShowTransModel(false)}
              >
                Close
              </button>
            </div>
          </div>
        </div>
      );
}