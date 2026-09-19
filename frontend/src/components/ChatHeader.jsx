function ChatHeader({
  conversationTitle,
}) {
  return (
    <header
      className="
        flex
        h-14
        shrink-0
        items-center
        border-b
        border-zinc-800
        px-6
      "
    >
      <div>
        <h2 className="text-sm font-semibold">
          {conversationTitle}
        </h2>

        <p className="text-xs text-zinc-500">
          Ask questions about your documents
        </p>
      </div>
    </header>
  )
}

export default ChatHeader