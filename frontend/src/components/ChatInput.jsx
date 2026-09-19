import { useState } from "react"

function ChatInput({
  onSend,
  disabled = false,
}) {
  const [value, setValue] = useState("")

  function handleSubmit(event) {
    event.preventDefault()

    const question = value.trim()

    if (!question || disabled) {
      return
    }

    onSend(question)
    setValue("")
  }

  function handleKeyDown(event) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault()
      handleSubmit(event)
    }
  }

  return (
    <div className="border-t border-zinc-800 p-4">
      <form
        onSubmit={handleSubmit}
        className="mx-auto max-w-3xl"
      >
        <div
          className="
            flex
            items-end
            gap-2
            rounded-2xl
            border
            border-zinc-700
            bg-zinc-900
            p-2
            transition
            focus-within:border-zinc-500
          "
        >
          <textarea
            value={value}
            onChange={(event) =>
              setValue(event.target.value)
            }
            onKeyDown={handleKeyDown}
            rows={1}
            disabled={disabled}
            placeholder={
              disabled
                ? "Generating answer..."
                : "Ask about your documents..."
            }
            className="
              min-h-10
              flex-1
              resize-none
              bg-transparent
              px-3
              py-2
              text-sm
              text-zinc-100
              outline-none
              placeholder:text-zinc-600
              disabled:cursor-not-allowed
            "
          />

          <button
            type="submit"
            disabled={
              disabled || !value.trim()
            }
            className="
              flex
              h-10
              w-10
              shrink-0
              items-center
              justify-center
              rounded-xl
              bg-zinc-100
              text-zinc-900
              transition
              hover:bg-white
              disabled:cursor-not-allowed
              disabled:opacity-40
            "
          >
            ↑
          </button>
        </div>

        <p className="mt-2 text-center text-xs text-zinc-600">
          Press Enter to send · Shift + Enter for a
          new line
        </p>
      </form>
    </div>
  )
}

export default ChatInput