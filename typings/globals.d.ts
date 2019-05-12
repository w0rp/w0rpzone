/** A simple interface for higlight.js. */
interface HighlightJS {
  /** Apply highlighting to an HTML element. */
  highlightBlock(element: HTMLElement | Document): void
}

interface IHighlightCode {
  scan(selector?: JQuery): void
}

declare global {
  const hljs: HighlightJS
  const HighlightCode: IHighlightCode

  interface Window {
    HighlightCode: IHighlightCode
  }
}

export {}
