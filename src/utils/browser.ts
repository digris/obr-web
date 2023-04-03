import Bowser from "bowser";

const parser = Bowser.getParser(window.navigator.userAgent);
// const osName = parser.getOSName(true);
const browserName = parser.getBrowserName(true);

const getMediaFormat = () => {
  // returns (best) supported media format
  // either `dash` or `hls`
  if (browserName === "safari") {
    return "hls";
  }
  return "dash";
};

const getStreamMediaFormat = () => {
  // returns (best) supported media format
  // either `hls` or icecast
  // if (osName === "ios") {
  //   return "icecast";
  // }
  return "hls";
};

export { getMediaFormat, getStreamMediaFormat };
