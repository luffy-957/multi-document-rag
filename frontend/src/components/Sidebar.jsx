function Sidebar({
  onNewChat,
}) {
  return (
    <aside
      className="
        w-72
        shrink-0
        border-r
        border-zinc-800
        bg-zinc-900
      "
    >
      <div className="flex h-full flex-col">

        {/* Header */}
        <div className="border-b border-zinc-800 p-4">
          <h1 className="text-lg font-semibold">
            MultiDoc RAG
          </h1>

          <p className="mt-1 text-xs text-zinc-500">
            Document Intelligence
          </p>
        </div>

        {/* New Chat */}
        <div className="p-3">
          <button
            onClick={onNewChat}
            className="
              w-full
              rounded-lg
              border
              border-zinc-700
              bg-zinc-800
              px-4
              py-2
              text-sm
              font-medium
              transition
              hover:bg-zinc-700
            "
          >
            + New Chat
          </button>
        </div>

        {/* Conversations */}
        <div className="flex-1 overflow-y-auto px-3">

          <p
            className="
              px-2
              py-2
              text-xs
              font-medium
              uppercase
              tracking-wider
              text-zinc-500
            "
          >
            Conversations
          </p>

          <p className="px-2 py-3 text-xs text-zinc-600">
            Your conversations will appear here.
          </p>
        </div>

        {/* Footer */}
        <div className="border-t border-zinc-800 p-3">
          <p className="text-xs text-zinc-600">
            Multi-Document RAG
          </p>
        </div>

      </div>
    </aside>
  )
}

export default Sidebar