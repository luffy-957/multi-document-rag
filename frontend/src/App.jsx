import { useEffect, useState } from "react"

import ChatHeader from "./components/ChatHeader"
import ChatInput from "./components/ChatInput"
import ChatMessage from "./components/ChatMessage"
import Sidebar from "./components/Sidebar"

import {
  getConversation,
  getConversations,
  sendChatMessage,
} from "./services/api"


function App() {
  const [messages, setMessages] = useState([])

  const [conversations, setConversations] =
    useState([])

  const [conversationId, setConversationId] =
    useState(null)

  const [isLoading, setIsLoading] =
    useState(false)

  const [isLoadingConversations, setIsLoadingConversations] =
    useState(true)

  const [error, setError] = useState(null)


  // --------------------------------------------------
  // Load conversations when app starts
  // --------------------------------------------------

  useEffect(() => {
    loadConversations()
  }, [])


  async function loadConversations() {
    try {
      setIsLoadingConversations(true)

      const data =
        await getConversations()

      setConversations(data)
    } catch (error) {
      console.error(error)

      setError(
        error.message ||
          "Failed to load conversations.",
      )
    } finally {
      setIsLoadingConversations(false)
    }
  }


  // --------------------------------------------------
  // Send message
  // --------------------------------------------------

  async function handleSend(question) {
    if (isLoading) {
      return
    }

    setError(null)

    const userMessage = {
      id: crypto.randomUUID(),
      role: "user",
      content: question,
      sources: [],
    }

    setMessages((currentMessages) => [
      ...currentMessages,
      userMessage,
    ])

    setIsLoading(true)

    try {
      const result = await sendChatMessage({
        question,
        conversationId,
        documentIds: [],
        k: 4,
      })

      if (!conversationId) {
        setConversationId(
          result.conversation_id,
        )
      }

      const assistantMessage = {
        id: result.message_id,
        role: "assistant",
        content: result.answer,
        sources: result.sources || [],
      }

      setMessages((currentMessages) => [
        ...currentMessages,
        assistantMessage,
      ])
    } catch (error) {
      console.error(error)

      setError(
        error.message ||
          "Something went wrong while generating the answer.",
      )
    } finally {
      setIsLoading(false)
    }
  }


  function handleNewChat() {
    setMessages([])
    setConversationId(null)
    setError(null)
  }


  return (
    <div className="flex h-screen bg-zinc-950 text-zinc-100">

      <Sidebar
        onNewChat={handleNewChat}
      />

      <main className="flex min-w-0 flex-1 flex-col">

        <ChatHeader
          conversationTitle={
            conversationId
              ? "Conversation"
              : "New Conversation"
          }
        />

        {/* Messages */}
        <div className="flex-1 overflow-y-auto">
          <div className="mx-auto flex max-w-3xl flex-col gap-5 px-6 py-8">

            {messages.length === 0 && (
              <div
                className="
                  flex
                  min-h-[60vh]
                  flex-col
                  items-center
                  justify-center
                  text-center
                "
              >
                <div
                  className="
                    mb-5
                    flex
                    h-14
                    w-14
                    items-center
                    justify-center
                    rounded-2xl
                    bg-zinc-800
                    text-xl
                  "
                >
                  ✦
                </div>

                <h2 className="text-2xl font-semibold">
                  Ask your documents
                </h2>

                <p
                  className="
                    mt-2
                    max-w-md
                    text-sm
                    leading-6
                    text-zinc-500
                  "
                >
                  Upload your documents and ask
                  questions about their contents
                  using retrieval-augmented generation.
                </p>
              </div>
            )}

            {messages.map((message) => (
              <ChatMessage
                key={message.id}
                role={message.role}
                content={message.content}
                sources={message.sources}
              />
            ))}

            {/* Loading */}
            {isLoading && (
              <div className="flex justify-start">
                <div
                  className="
                    rounded-2xl
                    bg-zinc-900
                    px-4
                    py-3
                    text-sm
                    text-zinc-500
                  "
                >
                  Thinking...
                </div>
              </div>
            )}

            {/* Error */}
            {error && (
              <div
                className="
                  rounded-xl
                  border
                  border-red-900
                  bg-red-950/30
                  px-4
                  py-3
                  text-sm
                  text-red-300
                "
              >
                {error}
              </div>
            )}

          </div>
        </div>

        <ChatInput
          onSend={handleSend}
          disabled={isLoading}
        />

      </main>
    </div>
  )
}

export default App