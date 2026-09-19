const API_BASE_URL = "/api"

export async function sendChatMessage({
  question,
  conversationId = null,
  documentIds = [],
  k = 4,
}) {
  const response = await fetch(
    `${API_BASE_URL}/chat/`,
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        question,
        conversation_id: conversationId,
        document_ids: documentIds,
        k,
      }),
    },
  )

  const data = await response.json()

  if (!response.ok) {
    throw new Error(
      data.detail ||
        data.error ||
        "Failed to send message.",
    )
  }

  return data
}