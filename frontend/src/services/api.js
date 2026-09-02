const API_BASE_URL = "http://127.0.0.1:8000/api/v1";


export async function loginUser(
  email,
  password
) {
  const response = await fetch(
    `${API_BASE_URL}/users/login`,
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        email,
        password,
      }),
    }
  );


  if (!response.ok) {
    let errorMessage = "Login failed.";

    try {
      const errorData = await response.json();

      if (typeof errorData.detail === "string") {
        errorMessage = errorData.detail;
      }
    } catch {
      // Keep default error message.
    }

    throw new Error(errorMessage);
  }


  return response.json();
}


export async function sendAIMessage(
  message,
  token
) {
  const response = await fetch(
    `${API_BASE_URL}/ai/chat`,
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`,
      },

      body: JSON.stringify({
        message,
      }),
    }
  );


  if (!response.ok) {
    let errorMessage = "AI request failed.";

    try {
      const errorData = await response.json();

      if (typeof errorData.detail === "string") {
        errorMessage = errorData.detail;
      }
    } catch {
      // Keep default error message.
    }

    throw new Error(errorMessage);
  }


  return response.json();
}


export async function getCurrentUser(
  token
) {
  const response = await fetch(
    `${API_BASE_URL}/users/me`,
    {
      method: "GET",

      headers: {
        "Authorization": `Bearer ${token}`,
      },
    }
  );


  if (!response.ok) {
    throw new Error(
      "Unable to retrieve user information."
    );
  }


  return response.json();
}


export async function getPaperAccount(token) {
  const response = await fetch(
    `${API_BASE_URL}/paper-trading/account`,
    {
      method: "GET",
      headers: {
        "Authorization": `Bearer ${token}`,
      },
    }
  );

  if (!response.ok) {
    let errorMessage = "Unable to retrieve paper trading account.";

    try {
      const errorData = await response.json();

      if (typeof errorData.detail === "string") {
        errorMessage = errorData.detail;
      }
    } catch {
      // Keep default error message.
    }

    throw new Error(errorMessage);
  }

  return response.json();
}


export async function getPaperPositions(token) {
  const response = await fetch(
    `${API_BASE_URL}/paper-trading/positions`,
    {
      method: "GET",
      headers: {
        "Authorization": `Bearer ${token}`,
      },
    }
  );

  if (!response.ok) {
    let errorMessage = "Unable to retrieve paper positions.";

    try {
      const errorData = await response.json();

      if (typeof errorData.detail === "string") {
        errorMessage = errorData.detail;
      }
    } catch {
      // Keep default error message.
    }

    throw new Error(errorMessage);
  }

  return response.json();
}


export async function getPaperPortfolio(token) {
  const response = await fetch(
    `${API_BASE_URL}/paper-trading/portfolio`,
    {
      method: "GET",
      headers: {
        "Authorization": `Bearer ${token}`,
      },
    }
  );

  if (!response.ok) {
    let errorMessage = "Unable to retrieve paper portfolio.";

    try {
      const errorData = await response.json();

      if (typeof errorData.detail === "string") {
        errorMessage = errorData.detail;
      }
    } catch {
      // Keep default error message.
    }

    throw new Error(errorMessage);
  }

  return response.json();
}


export async function getPaperTrades(token) {
  const response = await fetch(
    `${API_BASE_URL}/paper-trading/trades`,
    {
      method: "GET",
      headers: {
        "Authorization": `Bearer ${token}`,
      },
    }
  );

  if (!response.ok) {
    let errorMessage = "Unable to retrieve paper trades.";

    try {
      const errorData = await response.json();

      if (typeof errorData.detail === "string") {
        errorMessage = errorData.detail;
      }
    } catch {
      // Keep default error message.
    }

    throw new Error(errorMessage);
  }

  return response.json();
}


export async function buyStock(
  symbol,
  quantity,
  token
) {
  const response = await fetch(
    `${API_BASE_URL}/paper-trading/buy`,
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`,
      },

      body: JSON.stringify({
        symbol,
        quantity,
      }),
    }
  );

  if (!response.ok) {
    let errorMessage = "Unable to execute buy order.";

    try {
      const errorData = await response.json();

      if (typeof errorData.detail === "string") {
        errorMessage = errorData.detail;
      }
    } catch {
      // Keep default error message.
    }

    throw new Error(errorMessage);
  }

  return response.json();
}


export async function sellStock(
  symbol,
  quantity,
  token
) {
  const response = await fetch(
    `${API_BASE_URL}/paper-trading/sell`,
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`,
      },

      body: JSON.stringify({
        symbol,
        quantity,
      }),
    }
  );

  if (!response.ok) {
    let errorMessage = "Unable to execute sell order.";

    try {
      const errorData = await response.json();

      if (typeof errorData.detail === "string") {
        errorMessage = errorData.detail;
      }
    } catch {
      // Keep default error message.
    }

    throw new Error(errorMessage);
  }

  return response.json();
}