function ChatMessage({
  role,
  content,
  sources = [],
}) {
  const isUser = role === "user"

  return (
    <div
      className={`flex w-full ${
        isUser
          ? "justify-end"
          : "justify-start"
      }`}
    >
      <div
        className={`
          max-w-[80%]
          rounded-2xl
          px-4
          py-3
          text-sm
          leading-6
          ${
            isUser
              ? "bg-zinc-100 text-zinc-900"
              : "bg-zinc-900 text-zinc-200"
          }
        `}
      >
        <div className="whitespace-pre-wrap">
          {content}
        </div>

        {/* Sources */}
        {!isUser && sources.length > 0 && (
          <div className="mt-4 border-t border-zinc-800 pt-3">
            <p className="mb-2 text-xs font-medium text-zinc-500">
              Sources
            </p>

            <div className="flex flex-wrap gap-2">
              {sources.map(
                (source, index) => (
                  <div
                    key={`${source.document_id}-${source.page}-${index}`}
                    className="
                      rounded-lg
                      border
                      border-zinc-800
                      bg-zinc-950
                      px-3
                      py-2
                      text-xs
                    "
                  >
                    <p className="text-zinc-300">
                      {source.document}
                    </p>

                    <p className="mt-1 text-zinc-600">
                      Page {source.page}
                    </p>
                  </div>
                ),
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default ChatMessage