// frontend/src/lib/executionService.js
import axiosInstance from "./axios.js";

export const executeCode = async (language, code, input = "") => {
  try {
    // Hits the direct Express router endpoint: POST /execute
    const res = await axiosInstance.post("/v1/execute", {
      language,
      code,
      input,
    });

    // Express returns: { success: true/false, output: "...", error: "..." }
    return {
      success: res.data.success,
      output: res.data.output,
      error: res.data.error,
    };
  } catch (error) {
    console.error("Direct Express execution failed:", error);
    return {
      success: false,
      output: "",
      error: error.response?.data?.message || "Could not connect to the code sandbox.",
    };
  }
};