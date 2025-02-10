import { formatUnits } from "ethers";

export const formatWeiAmount = (amount, decimals) => {
  if (!amount || amount === null || amount === undefined) {
    return "Invalid Amount"; // Handle invalid or null amounts gracefully
  }
  
  // Ensure the amount is a valid BigNumber (or a valid BigNumberish)
  try {
    const formattedAmount = formatUnits(amount, decimals);
    return new Intl.NumberFormat("en-US", {
      maximumFractionDigits: decimals,
    }).format(formattedAmount);
  } catch (error) {
    console.error("Error formatting amount:", error);
    return "Error"; // Return a default error value
  }
};
