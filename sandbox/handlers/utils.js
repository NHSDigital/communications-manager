import log from "loglevel"

export const write_log = (res, log_level, options = {}) => {
  if (log.getLevel() > log.levels[log_level.toUpperCase()]) {
    return
  }
  let processedOptions;
  if (typeof options === "function") {
    processedOptions = options()
  } else {
    processedOptions = options
  }
  let log_line = {
    timestamp: Date.now(),
    level: log_level,
    correlation_id: res.locals.correlation_id
  }
  if (typeof options === "object") {
    processedOptions = Object.keys(processedOptions).reduce((obj, x) => {
      let val = processedOptions[x];
      if (typeof val === "function") {
        return {
          ...obj,
          val()
        };
      }

      return {
        ...obj,
        val
      };
    }, {});
    log_line = Object.assign(log_line, processedOptions)
  }
  if (Array.isArray(processedOptions)) {
    log_line["log"] = { log: processedOptions.map(x => { return typeof x === "function" ? x() : x }) }
  }

  log[log_level](JSON.stringify(log_line))
};

export function sendError(res, code, message) {
  res.status(code);
  res.json({
    message: message
  });
}

export function hasValidGlobalTemplatePersonalisation(personalisation) {
  if (!personalisation) {
    return false;
  }

  const personalisationFields = Object.keys(personalisation);
  if (personalisationFields.length != 1) {
    return false;
  }

  if (personalisationFields[0] !== "body") {
    return false;
  }
  return true;
}
