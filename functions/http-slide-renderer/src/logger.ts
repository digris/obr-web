import pino from 'pino'

const isGCP = Boolean(process.env.K_SERVICE)

export const logger = pino({
  level: 'info',
  messageKey: 'message',

  formatters: {
    level(label) {
      return { severity: label.toUpperCase() }
    },
    bindings() {
      return {}
    },
  },

  base: undefined,
  timestamp: isGCP ? false : pino.stdTimeFunctions.isoTime,
})
